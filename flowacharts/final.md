```mermaid
graph TD

subgraph Candidate.py
    A1[Define Candidate Class] --> A2[Calculate GitHub Score]
    A2 --> A3[Calculate University Score]
    A3 --> A4[Calculate Professor Score]
    A4 --> A5[Calculate Overall Score]
end

subgraph GitHub Scorer
    B1[github.py] --> B2[Fetch GitHub Repos]
    B2 --> B3[Calculate GitHub Score]
end

subgraph University Scorer
    C1[university.py] --> C2[University Scores Dictionary]
    C2 --> C3[Calculate University Score]
end

subgraph Professor Data
    D1[prof.py] --> D2[Store Professor Data]
end

subgraph Normalization
    E1[normalise.py] --> E2[Normalize Scores]
end

subgraph Google Scholar Scraper
    F1[googlescholar.py] --> F2[Fetch Scholar Data]
    F2 --> F3[Calculate Relevance Score]
end

subgraph Authors Scraper
    H1[authors.py] --> H2[Get Professor URL]
    H2 --> H3[Get Citation Links]
    H3 --> H4[Get Authors from Citations]
end

subgraph Filter Authors
    I1[filter.py] --> I2[Filter Authors List]
    I2 --> I3[Extract Degree Type]
end

subgraph Student Scraper
    J1[student_scrape.py] --> J2[Fetch Candidate Details]
    J2 --> J3[Search GitHub Username]
    J3 --> J4[Create Candidate Objects]
end

subgraph Main Flow
    G1[main.py] --> G2[Scan Professors]
    G2 --> G3[Extract Students]
    G3 --> G4[Create Candidate Objects]
    G4 --> G5[Calculate Scores]
    G5 --> G6[Normalize Scores]
end

A1 --> G1
B1 --> A2
C1 --> A3
D1 --> A4
E1 --> G6
F1 --> A4
H1 --> I1
I1 --> J1
J1 --> G3
'''