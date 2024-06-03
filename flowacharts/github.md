```mermaid
graph TD
    A[Start] --> B[Get GitHub username]
    B --> C[Fetch repositories for username]
    C --> D[Evaluate project relevance]
    D --> E[Score repositories]
    E --> F[Aggregate scores]
    F --> G[Return total GitHub score and details]
'''