# AI Recruiter Project

## Overview

This project is an AI-driven recruitment tool designed to scrape and analyze GitHub and Google Scholar profiles to identify top candidates for AI and ML roles. The tool classifies input queries, fetches profile details, and ranks candidates based on their GitHub repositories and Google Scholar citations.

## File Structure

# Workflow, code structure


```mermaid
graph TD

subgraph Query Classifier
    A1[query_classifier.py] --> B1[scangit.py]
    A1 --> C1[scangs.py]
    A1 --> D1[scanauth.py]
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
```


### `candidate.py`

Defines the `Candidate` class and methods to calculate scores based on GitHub activity, university, and other criteria.

### `github.py`

Fetches GitHub repositories, calculates repository scores, and aggregates them to provide an overall GitHub score for a user.

### `prof.py`

Stores professor data, including names, universities, and homepage URLs.

### `normalise.py`

Normalizes the scores of candidates and sorts them based on the overall normalized score.

### `googlescholar.py`

Fetches data from Google Scholar, calculates relevance scores, and provides citation information for profiles.

### `authors.py`

Scrapes co-authors from Google Scholar citations and returns a list of potential students and collaborators.

### `scanauth.py`

Filters out professors from the list of authors and classifies remaining individuals based on their roles and degree types.

### `requirements.txt`

Lists all the required Python libraries for the project, ensuring all dependencies are installed.

## Requirements

To set up the project environment, ensure you have Python installed and then install the required libraries using `requirements.txt`.

## Usage

### Setting Up

1. Clone the repository.
2. Create a virtual environment and activate it:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>sh</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copy code</button></span></div></div><div class="overflow-y-auto p-4 text-left undefined" dir="ltr"><code class="!whitespace-pre hljs language-sh">python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   </code></div></div></pre>
3. Install the dependencies:
4. <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>sh</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copy code</button></span></div></div><div class="overflow-y-auto p-4 text-left undefined" dir="ltr"><code class="!whitespace-pre hljs language-sh">pip install -r requirements.txt 
   </code></div></div></pre>

### Running the Project

1. **Extracting Student Details:**
   Run 'app.py' and click on the dynamic link generated to launch the web app.( Can use ctrl+Click on windows and Commans+Click on MacOS on the link to open it in a new tab)

   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>sh</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copy code</button></span></div></div><div class="overflow-y-auto p-4 text-left undefined" dir="ltr"><code class="!whitespace-pre hljs language-sh">python app.py
   </code></div></div></pre>
2. **Processing Queries:**
   To classify input queries and fetch top profiles, run the query processing script: app.py **This is the most relevant one and should be the only one of the user's concern. It calls other scripts and returns the suitable databse of candidates.**

   **Example usage query:**
   #Please pick one of Boston, California, Seattle, Berkeley.
   #Sample queries:
   #"Find top 6 students who have worked on TensorFlow and have a strong GitHub presence in Boston."
   #"Recruit top 5 students in California who have worked on computer vision projects."
   #"Find top 8 programmers in Seattle who have worked on GPT-3 and have published papers on NLP."
   #"Recruit top 3 scholars in Boston ."
   #top 8 people who have worked in AI labs in Boston.
