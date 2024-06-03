```mermaid
graph TD
    subgraph GitHub.py
        A1[Start] --> B1[Get GitHub username]
        B1 --> C1[Fetch repositories for username]
        C1 --> D1[Evaluate project relevance]
        D1 --> E1[Score repositories]
        E1 --> F1[Aggregate scores]
        F1 --> G1[Return total GitHub score and details]
    end

    subgraph UserGitHubDetails.py
        A2[Start] --> B2[Initialize UserGitHubDetails object with username]
        B2 --> C2[Fetch profile details]
        C2 --> D2[Fetch repositories]
        D2 --> E2[Parse and store repository details]
        E2 --> F2[Return UserGitHubDetails object]
    end

    subgraph Normalize.py
        A3[Start] --> B3[Input list of candidates]
        B3 --> C3[Calculate normalized scores for GitHub, university, and h-index]
        C3 --> D3[Sort candidates by overall normalized score]
        D3 --> E3[Return sorted list of candidates]
    end

    subgraph GoogleScholar.py
        A4[Start] --> B4[Get professor name and university]
        B4 --> C4[Search for professor's Google Scholar profile]
        C4 --> D4[Fetch scholar data]
        D4 --> E4[Extract h-index and citations]
        E4 --> F4[Return scholar data]
    end

    subgraph Authors.py
        A5[Start] --> B5[Get professor name and university]
        B5 --> C5[Find Google Scholar URL]
        C5 --> D5[Extract citation links from profile]
        D5 --> E5[Fetch authors from each citation]
        E5 --> F5[Compile list of unique authors]
        F5 --> G5[Return list of authors]
    end

    subgraph Filter.py
        A6[Start] --> B6[Input list of students]
        B6 --> C6[Filter and rank students]
        C6 --> D6[Return filtered list of top students]
    end

    A5 --> B5
    B5 --> C5
    C5 --> D5
    D5 --> E5
    E5 --> F5
    F5 --> G5
    G5 --> B6

    B6 --> C6
    C6 --> D6
    D6 --> E6

'''