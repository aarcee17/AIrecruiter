from transformers import pipeline
from scangit import *
from scangs import *
from filter import *
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
nlp = pipeline("ner", model="dslim/bert-base-NER")
from prof import *
import sys
def classify_query(query):
    entities = nlp(query)
    #print(entities)
    classification = {"github": False, "scholar": False, "student": False, "location": None}
    # k = 15  

    github_keywords = [
        "github", "repository", "programmer", "developer", 
        "llama", "llama-2", "llama-3", "gpt", "gpt-3", "gpt-4", "openai",
        "tensorflow", "pytorch", "keras", "jupyter", "notebook", 
        "machine learning", "artificial intelligence", "mlops", "deep learning",
        "neural networks", "data science", "computer vision", "nlp", 
        "reinforcement learning", "supervised learning", "unsupervised learning", 
        "hackathon", "pull request", "commit", "fork", "issue", 
        "ci/cd", "repo", "devops", "docker", "kubernetes", 
        "cloud engineer", "open source", "contributor", "tech lead", 
        "github actions", "github stars", "git", "coding challenge",
        "algorithm", "data structures"
    ]

    scholar_keywords = [
    "google scholar", "scholar", "research", "citations", "paper", 
    "publication", "h-index", "i10-index", "journal", "conference", 
    "arxiv", "preprint", "peer-reviewed", "bibliometrics", "impact factor",
    "researcher", "academic", "professor", "phd", "msc", "postdoc", 
    "research assistant", "principal investigator", "lab director",
    "literature review", "thesis", "dissertation", "research grant",
    "funding", "scholarly article", "review article", "case study",
    "conference proceedings", "scientific paper", "white paper",
    "abstract", "keywords", "author affiliations", "research profile",
    "research topic", "research gate", "citations per year", "citation metrics"
    ]
    student_keywords = [
    "student", "lab", "labs", "university", "universities", "AI labs", 
    "researcher", "undergraduate", "bachelor's", "master's", "phd student", 
    "msc student", "bsc student", "graduate student", "postgraduate student", 
    "research intern", "internship", "academic program", "coursework", 
    "research project", "academic advisor", "faculty advisor", "department",
    "college", "school", "institution", "campus", "student organization",
    "student club", "honor society", "student research", "thesis project",
    "dissertation project", "research grant", "scholarship", "fellowship",
    "academic conference", "student conference", "graduate school", "graduate studies",
    "academic career", "academic achievement", "academic excellence", 
    "academic transcript", "dean's list", "valedictorian",  "student body", 
    "student council", "student government", "student life", "campus life", "study group"
    ]



    for entity in entities:
        word = entity['word'].lower()
        if entity['entity'] == 'B-LOC':
            classification["location"] = entity['word']
        # if entity['entity'] == 'B-NUM':
        #     k = int(entity['word'])


    if any(keyword in query.lower() for keyword in github_keywords):
        classification["github"] = True
    if any(keyword in query.lower() for keyword in scholar_keywords):
        classification["scholar"] = True
    if any(keyword in query.lower() for keyword in student_keywords):
        classification["student"] = True

    return classification

def find_colleges(location):
    colleges = []
    for university, details in professors.items():
        for detail in details:
            if detail.get('location',None) == location:
                colleges.append(university)
    return colleges

def process_query(query):
    classification = classify_query(query)

    categories = []
    if classification["github"]:
        categories.append("github")
    if classification["scholar"]:
        categories.append("scholar")
    if classification["student"]:
        categories.append("student")
    location = classification["location"]
    
    return categories, location

def write_git_to_csv(topk_profiles):
    with open('git_profiles.csv', 'w', newline='') as csvfile:
        fieldnames = ['GitHub ID', 'Link', 'Total Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for profile in topk_profiles:
            writer.writerow({
                'GitHub ID': profile['github_id'],
                'Link': f"https://github.com/{profile['github_id']}",
                'Total Score': profile['total_score']
            })

def extract_parameters(query):
    k = 7

    words = query.split()
    for i, word in enumerate(words):
        if word.isdigit():
            k = int(word)
        elif word.lower() == "top" and i < len(words) - 1 and words[i+1].isdigit():
            k = int(words[i+1])
    return k         
# Example usage
#print("\n\nWelcome to AIrecruiter\n\n")
query = ' '.join(sys.argv[1:])
# query = "I want to find top 10 programmer who have worked on Llama-3 in Boston"
categories, location = process_query(query)
k = extract_parameters(query)
#print(f"Categories: {categories}, k: {k}, location: {location}")


for category in categories:
    if category == "github":
        #print(f"Fetching top {k} GitHub profiles in {location or 'global'}...")
        top_k_profiles = fetch_topkgithub(k, location)
        write_git_to_csv(top_k_profiles)
        for profile in top_k_profiles:
            print(f"GitHub ID: {profile['github_id']}\n Link: https://github.com/{profile['github_id']}\n  Total Score: {profile['total_score']}\n")
            # for repo in profile['detailed_scores']:
            #     print(f"  Repo: {repo['name']}, Score: {repo['score']}, Stars: {repo['stars']}, Relevance Score: {repo['relevance_score']}")

        # fetch_github_profiles(k, location)
    elif category == "scholar":
        #print(f"Fetching top {k} Google Scholar profiles in {location or 'global'}...")
        top_k_profiles = topk_googlescholar(k, location)
        write_profile_to_csv(top_k_profiles)
        for profile in top_k_profiles:
            print(f"Name: {profile['name']}\n relevance: {profile['relevance_score']}\n citations: {profile['citations']}\n H-index: {profile['h_index']}\n Degree/Institute of Work: {profile['degree_type']}\n Profile Link: {profile['scholar_url']}\n Linkedin Link: {profile['Linkedin']}\n")

    elif category == "student":
        #college = input("What college do you want to recruit from?: ")
        colleges = find_colleges(location)
        for college in colleges:
           # print(f"College: {college[0]['name']}")
            #print(f"Fetching top {k} student profiles from {college} ...")
            remain(college, k)
            time.sleep(2)
#Please pick one of Boston, Caliofornia, Seattle, Berkeley. 
#Sample queries:
#"Find top 6 students who have worked on TensorFlow and have a strong GitHub presence in Boston."
#"Recruit top 5 students in California who have worked on computer vision projects."
#"Find top 8 programmers in Seattle who have worked on GPT-3 and have published papers on NLP."
#"Recruit top 3 scholars in Boston ."
#top 8 people who have worked in AI labs in Boston.