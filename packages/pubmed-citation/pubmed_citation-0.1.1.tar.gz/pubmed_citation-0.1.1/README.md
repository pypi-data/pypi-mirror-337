# Midterm Project
This repo contains our Python package project

## Project Proposal: 
Team Commit To The Git (Armelle Duston, Brandon Spiegel and Shanta Murthy)
The proposal below summarizes is an outline addressing each component of the rubric

### Potential data sources
- We plan to focus on sources with distinct “entries” containing content and metadata that enables forming a network structure and conducting analysis using the content within entries
- This may be sites hosting academic journal articles such as PubMed and ArXiv, or clinical trial information such as clinicaltrials.gov

### Data Scaffolding:
- The above sources have public API’s, so data access will occur in a few steps:
    1) a user interface will enable users to fetch data on the fly.
    2) fetching data will be performed by translating user inputs into API requests
    3) data will be housed on a users local pc (client-side)
- Guardrails will be used to rate-limit user requests
- Separation of concerns between the user interface and the creation of API requests will allow us to limit access to a subset of the data source (eg only articles published in the last X years, or only articles in English)

### Data Navigation:
- One element of interest is to enable users to calculate the “degrees of separation” between any pair of authors by traversing through co-authors on their respective publications. This amounts to calculating the shortest path between two nodes on a graph and will require an algorithm to navigate the data
- We are also considering different ways of “clustering” authors based on similarity metrics, which may include dynamic programming or other algorithms as explored in recent homeworks

### Data Analysis:
- The core analysis task here is an implementation of spectral clustering to group authors into k clusters based on the "closeness" of their coauthorships where k is user-defined This is done in a few key steps: First, create the adjacency and degree matrices and derive the laplacian based on coauthorships. Second, get the smallest k eigenvalues and eigenvectors (skipping over the smallest). Third use a k-means clustering algorithm to form clusters. The key computational element includes use of scipy sparse matrices and scipy sparse eigenvector/value functions to speed up computation, and a timeout in the case of slow convergence. A dictionary from authors to their assigned cluster is returned for use in downstream visualizations.

### Interactive Visualization:
- The above “degrees of separation” idea can be displayed using packages to visualize network data
- Additionally, we can create an interactive map to enable users to learn about the type of research published across different institutions, and overlay networks graphs based on how those institutions are connected as well as show how things change over time
