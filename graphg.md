
```mermaid
graph TD

subgraph Query Classifier
    A1[query_classifier.py] --> B1[scangit.py]
    A1 --> C1[scangs.py]
    A1 --> D1[filter.py]
end

subgraph GitHub Scorer
    B1 --> B2[github.py]
    B2 --> B3[UserGitHubDetails]
end

subgraph Google Scholar Scraper
    C1 --> C2[googlescholar.py]
end

subgraph Filter Authors
    D1 --> D2[prof.py]
    D2 --> D3[authors.py]
end

A1 --> B1
A1 --> C1
A1 --> D1
B1 --> B2
B2 --> B3
C1 --> C2
D1 --> D2
D2 --> D3

