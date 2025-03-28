import argparse
import json
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pubmed_citation.scaffold import PubMedFetcher
from pubmed_citation.navigate import (
    find_path,
    compute_separation,
    find_all_connecting_papers,
    find_author_clusters,
)
from pubmed_citation.models import Network


def main():
    """Command line interface for the package."""
    parser = argparse.ArgumentParser(
        description="PubMed Citation Network Tool - A tool for collecting citation data from PubMed and analyzing author relationships",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pubmed-citation search "CRISPR gene editing" --max-results 20
  pubmed-citation network "machine learning cancer" --depth 1 --output network.json
  pubmed-citation path --network network.json --author1 "Smith J" --author2 "Johnson T"
  pubmed-citation export --network network.json --output-prefix mydata
        """,
    )

    # Global options with expanded descriptions
    parser.add_argument(
        "--email",
        type=str,
        help="Your email address to include with PubMed API requests (recommended by NCBI to prioritize your requests and contact you if there are issues)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Your NCBI API key for higher rate limits (allows 10 requests/second instead of 3 requests/second)",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="pubmed_cache",
        help="Directory to store cached API results to avoid redundant requests",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching and always fetch fresh data from the PubMed API",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # SEARCH COMMAND
    search_parser = subparsers.add_parser(
        "search",
        help="Search for scientific articles in PubMed",
        description="""
SEARCH COMMAND

Searches PubMed for articles matching the given query and returns the results.

This command translates your query into a PubMed API request, fetches the matching articles,
and displays their basic information (title, authors, journal, etc.).

Examples:
  pubmed-citation search "CRISPR gene editing"
  pubmed-citation search "cancer immunotherapy" --max-results 30 --from-date 2020/01/01
  pubmed-citation search "Smith J[Author]" --output smith_papers.json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    search_parser.add_argument(
        "query",
        type=str,
        help='Search query for PubMed (e.g., "CRISPR gene editing", "cancer immunotherapy", "Smith J[Author]")',
    )
    search_parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum number of search results to return (default: 50, max allowed by PubMed: 100000)",
    )
    search_parser.add_argument(
        "--from-date",
        type=str,
        help='Include only articles published on or after this date (format: YYYY/MM/DD, e.g., "2020/01/01")',
    )
    search_parser.add_argument(
        "--to-date",
        type=str,
        help='Include only articles published on or before this date (format: YYYY/MM/DD, e.g., "2023/12/31")',
    )
    search_parser.add_argument(
        "--output", type=str, help="Save search results to this JSON file (optional)"
    )

    # NETWORK COMMAND
    network_parser = subparsers.add_parser(
        "network",
        help="Build a citation network from PubMed search results",
        description="""
NETWORK COMMAND

Builds a network of articles, authors, and citations starting from search results.

This command:
1. Searches PubMed for your query (similar to the "search" command)
2. For each result, it finds articles that cite it (if depth >= 1)
3. Builds a network of articles, authors, and their relationships
4. Saves this network to a JSON file for later analysis

The network includes:
- Articles (with metadata like title, journal, etc.)
- Authors (with their publications)
- Citation relationships (which articles cite others)
- Co-authorship relationships (which authors have worked together)

Examples:
  pubmed-citation network "CRISPR" --output crispr_network.json
  pubmed-citation network "machine learning cancer" --depth 1 --max-results 30 --output ml_cancer.json
  pubmed-citation network "immunotherapy" --from-date 2020/01/01 --output recent_immuno.json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    network_parser.add_argument(
        "query",
        type=str,
        help='Search query for the initial set of articles (the "seed" articles for the network)',
    )
    network_parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum number of top-level articles to include as starting points for the network (default: 50)",
    )
    network_parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="""How many levels of citations to include:
- 0: only search results
- 1: include articles that cite the search results
- 2: also include articles that cite the citing articles
(default: 1)""",
    )
    network_parser.add_argument(
        "--from-date",
        type=str,
        help="Include only articles published on or after this date (format: YYYY/MM/DD)",
    )
    network_parser.add_argument(
        "--to-date",
        type=str,
        help="Include only articles published on or before this date (format: YYYY/MM/DD)",
    )
    network_parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Save the network to this JSON file (required)",
    )

    # PATH COMMAND
    path_parser = subparsers.add_parser(
        "path",
        help="Find the shortest path between two authors in a network",
        description="""
PATH COMMAND

Analyzes a citation network to find how two authors are connected through co-authorship relationships.

This command:
1. Loads a previously created network from a JSON file
2. Finds the shortest path connecting two authors through their co-authors
3. Displays the degrees of separation and the connecting authors
4. Shows the papers that connect consecutive authors in the path

This is similar to the "degrees of separation" or "Six Degrees of Kevin Bacon" concept,
but for scientific authors based on their publication history.

Examples:
  pubmed-citation path --network crispr_network.json --author1 "Doudna" --author2 "Zhang"
  pubmed-citation path --network ml_network.json --author1 "Hinton G" --author2 "LeCun Y" --algorithm bfs
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    path_parser.add_argument(
        "--network",
        type=str,
        required=True,
        help='Path to a previously saved network JSON file from the "network" command',
    )
    path_parser.add_argument(
        "--author1",
        type=str,
        required=True,
        help="Name of the first author (starting point) - partial names are supported",
    )
    path_parser.add_argument(
        "--author2",
        type=str,
        required=True,
        help="Name of the second author (destination) - partial names are supported",
    )
    path_parser.add_argument(
        "--algorithm",
        type=str,
        choices=["bfs", "dfs"],
        default="bfs",
        help="""Path finding algorithm to use:
- bfs (breadth-first search): Guarantees the shortest path (fewest degrees of separation)
- dfs (depth-first search): May find a different path, sometimes faster on large networks
(default: bfs)""",
    )

    # EXPORT COMMAND
    export_parser = subparsers.add_parser(
        "export",
        help="Export a citation network to CSV files for analysis in other tools",
        description="""
EXPORT COMMAND

Converts a network into CSV files that can be imported into visualization tools like Gephi or Cytoscape.

This command:
1. Loads a previously created network from a JSON file
2. Exports the network data into four CSV files:
   - {prefix}_articles.csv: Article data (PMID, title, journal, etc.)
   - {prefix}_citations.csv: Citation relationships (citing_pmid, cited_pmid)
   - {prefix}_authors.csv: Author information (ID, name, publication count)
   - {prefix}_coauthorship.csv: Co-authorship relationships (author1, author2)

These CSV files can be imported into network visualization and analysis tools for further study.

Examples:
  pubmed-citation export --network crispr_network.json --output-prefix crispr
  pubmed-citation export --network ml_network.json --output-prefix machine_learning
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    export_parser.add_argument(
        "--network",
        type=str,
        required=True,
        help='Path to a previously saved network JSON file from the "network" command',
    )
    export_parser.add_argument(
        "--output-prefix",
        type=str,
        required=True,
        help="Prefix for the output CSV files (creates {prefix}_articles.csv, {prefix}_citations.csv, etc.)",
    )

    # Add spectral clustering subparser
    cluster_parser = subparsers.add_parser(
        "cluster",
        help="Perform spectral clustering on author network",
        description="""
        Cluster authors in a network using spectral clustering.
        
        Example usage:
        pubmed-citation cluster --network network.json -k 3 --output clusters.json
            
        This will load the network from network.json and group authors 
        into 3 clusters based on their coauthorship patterns.
        """
    )
    cluster_parser.add_argument(
        "--network",
        help="Path to network JSON file"
    )
    cluster_parser.add_argument(
        "-k", "--num_clusters",
        type=int,
        required=True,
        help="Number of clusters to create"
    )
    cluster_parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Save the cluster outputs to JSON file",
    )
    cluster_parser.set_defaults(func=run_clustering)

    args = parser.parse_args()

    # Create the fetcher
    fetcher = PubMedFetcher(
        email=args.email, api_key=args.api_key, cache_dir=args.cache_dir
    )

    # Determine which command to run
    if args.command == "search":
        run_search(fetcher, args)
    elif args.command == "network":
        run_network(fetcher, args)
    elif args.command == "path":
        run_path(args)
    elif args.command == "export":
        run_export(args)
    elif args.command == "cluster":
        run_clustering(args)
    else:
        parser.print_help()


def run_search(fetcher, args):
    """Run the search command."""
    logger.info(f"Searching PubMed for: {args.query}")

    articles = fetcher.search_articles(
        query=args.query,
        max_results=args.max_results,
        date_from=args.from_date,
        date_to=args.to_date,
        use_cache=not args.no_cache,
    )

    logger.info(f"Found {len(articles)} articles")

    # Display results
    for i, article in enumerate(articles[:10], 1):
        print(f"{i}. {article.title}")
        print(f"   PMID: {article.pmid}")
        print(f"   Journal: {article.journal}")
        print(f"   Date: {article.date}")
        print(f"   Authors: {', '.join([str(a) for a in article.authors[:3]])}")
        if len(article.authors) > 3:
            print(f"     and {len(article.authors) - 3} more")
        print()

    if len(articles) > 10:
        print(f"...and {len(articles) - 10} more articles")

    # Save to file if requested
    if args.output:
        article_data = [article.to_dict() for article in articles]
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(article_data, f, indent=2)
        logger.info(f"Saved {len(articles)} articles to {args.output}")


def run_network(fetcher, args):
    """Run the network command."""
    logger.info(f"Building citation network for: {args.query}")

    network = fetcher.build_citation_network(
        query=args.query,
        max_results=args.max_results,
        depth=args.depth,
        date_from=args.from_date,
        date_to=args.to_date,
        use_cache=not args.no_cache,
    )

    # Display network stats
    print(f"Network stats:")
    print(f"- Articles: {len(network.articles)}")
    print(f"- Citations: {sum(len(citing) for citing in network.citations.values())}")
    print(f"- Authors: {len(network.authors)}")
    print(
        f"- Co-authorship links: {sum(len(coauthors) for coauthors in network.coauthorships.values()) // 2}"
    )

    # Save to file
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(network.to_dict(), f, indent=2)
    logger.info(f"Saved network to {args.output}")


def _find_author_by_name(network, name):
    """Find an author in the network by name."""
    name_lower = name.lower()

    # Try exact match
    for author_id, author in network.authors.items():
        if author.name.lower() == name_lower:
            return author_id

    # Try partial match
    candidates = []
    for author_id, author in network.authors.items():
        if name_lower in author.name.lower():
            candidates.append((author_id, author))

    if not candidates:
        logger.warning(f"No author found matching '{name}'")
        return None

    if len(candidates) == 1:
        logger.info(f"Found author: {candidates[0][1].name}")
        return candidates[0][0]

    # Multiple matches, ask user to select
    print(f"Multiple authors found matching '{name}':")
    for i, (author_id, author) in enumerate(candidates, 1):
        print(f"{i}. {author.name} ({len(author.articles)} articles)")

    while True:
        try:
            choice = int(input("Enter the number of the correct author: "))
            if 1 <= choice <= len(candidates):
                return candidates[choice - 1][0]
            else:
                print(f"Please enter a number between 1 and {len(candidates)}")
        except ValueError:
            print("Please enter a valid number")


def run_path(args):
    """Run the path finding command."""
    # Load the network
    try:
        with open(args.network, "r", encoding="utf-8") as f:
            network_data = json.load(f)

        network = Network.from_dict(network_data)
        logger.info(f"Loaded network with {len(network.articles)} articles")
    except Exception as e:
        logger.error(f"Failed to load network: {e}")
        return

    # Find the authors
    author1_id = _find_author_by_name(network, args.author1)
    author2_id = _find_author_by_name(network, args.author2)

    if not author1_id or not author2_id:
        return

    # Find the path
    path = find_path(network, author1_id, author2_id, args.algorithm)

    if path is None:
        print(f"No path found between '{args.author1}' and '{args.author2}'")
        return

    # Display the path
    print(f"Found path with {len(path)-1} degrees of separation:")

    for i, author_id in enumerate(path):
        author = network.authors[author_id]
        print(f"{i+1}. {author.name}")

        # Show connection details for consecutive authors
        if i < len(path) - 1:
            next_author_id = path[i + 1]
            shared_papers = find_all_connecting_papers(
                network, author_id, next_author_id
            )

            if shared_papers:
                print(
                    f"   Co-authored {len(shared_papers)} papers with the next author, including:"
                )
                for j, pmid in enumerate(shared_papers[:2], 1):
                    article = network.articles.get(pmid)
                    if article:
                        print(f"   - {article.title}")

                if len(shared_papers) > 2:
                    print(f"   - and {len(shared_papers) - 2} more")

            print()


def run_export(args):
    """Run the export command."""
    # Load the network
    try:
        with open(args.network, "r", encoding="utf-8") as f:
            network_data = json.load(f)

        network = Network.from_dict(network_data)
        logger.info(f"Loaded network with {len(network.articles)} articles")
    except Exception as e:
        logger.error(f"Failed to load network: {e}")
        return

    # Export to CSV
    articles_file = f"{args.output_prefix}_articles.csv"
    citations_file = f"{args.output_prefix}_citations.csv"
    authors_file = f"{args.output_prefix}_authors.csv"
    coauthorship_file = f"{args.output_prefix}_coauthorship.csv"

    network.export_to_csv(
        articles_file=articles_file,
        citations_file=citations_file,
        authors_file=authors_file,
        coauthorship_file=coauthorship_file,
    )

    logger.info(f"Exported network to CSV files with prefix {args.output_prefix}")

def run_clustering(args):
    """Handle spectral clustering command"""    
    logger.info(f"Loading network from {args.network}")
    with open(args.network, 'r') as f:
        network_data = json.load(f)
    
    network = Network.from_dict(network_data)
    
    logger.info(f"Performing spectral clustering with k={args.num_clusters}")
    clusters = network.spectral_clustering(args.num_clusters)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(clusters, f, indent=2)
        logger.info(f"Saved {len(clusters)} author cluster assignments to {args.output}")

if __name__ == "__main__":
    main()
