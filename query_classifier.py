import requests
from googlesearch import search
from scangit import *
from scangs import *
from filter import *
from prof import *
import sys
def classify_query(query):
    
    github_keywords = [
        "github", "repository", "programmer", "developer", "engineer", "coder",
        "engineers", "programmers", "developers", "gpt", "tensorflow", "pytorch", "keras",
        "jupyter", "notebook", "machine learning", "artificial intelligence", "mlops",
        "deep learning", "neural networks", "data science", "computer vision", "nlp",
        "reinforcement learning", "supervised learning", "unsupervised learning",
        "hackathon", "pull request", "commit", "fork", "issue", "ci/cd", "repo",
        "devops", "docker", "kubernetes", "cloud engineer", "open source", "contributor",
        "tech lead", "github actions", "github stars", "git", "coding challenge",
        "algorithm", "data structures"
    ]

    scholar_keywords = [
        "google scholar", "scholar", "research", "citations", "paper", "publication",
        "h-index", "i10-index", "journal", "conference", "arxiv", "preprint",
        "peer-reviewed", "bibliometrics", "impact factor", "researcher", "academic",
        "professor", "phd", "msc", "postdoc", "research assistant", "principal investigator",
        "lab director", "literature review", "thesis", "dissertation", "research grant",
        "funding", "scholarly article", "review article", "case study", "conference proceedings",
        "scientific paper", "white paper", "abstract", "keywords", "author affiliations",
        "research profile", "research topic", "research gate", "citations per year", "citation metrics"
    ]

    student_keywords = [
        "student", "lab", "labs", "university", "universities", "AI labs", "researcher",
        "undergraduate", "bachelor's", "master's", "phd student", "msc student",
        "bsc student", "graduate student", "postgraduate student", "research intern",
        "internship", "academic program", "coursework", "research project", "academic advisor",
        "faculty advisor", "department", "college", "school", "institution", "campus",
        "student organization", "student club", "honor society", "student research",
        "thesis project", "dissertation project", "research grant", "scholarship", "fellowship",
        "academic conference", "student conference", "graduate school", "graduate studies",
        "academic career", "academic achievement", "academic excellence", "academic transcript",
        "dean's list", "valedictorian", "student body", "student council", "student government",
        "student life", "campus life", "study group"
    ]

    
    locations = [
        "Boston", "California", "Seattle", "Berkeley", "New York", "San Francisco",
        "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
        "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth",
        "Columbus", "Charlotte"
    ]

    classification = {"github": False, "scholar": False, "student": False, "location": None}

    
    words = query.lower().split()
    for word in words:
        if word in locations:
            classification["location"] = word
        if any(keyword in query.lower() for keyword in github_keywords):
            classification["github"] = True
        if any(keyword in query.lower() for keyword in scholar_keywords):
            classification["scholar"] = True
        if any(keyword in query.lower() for keyword in student_keywords):
            classification["student"] = True

    return classification

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

def extract_parameters(query):
    k = 7

    words = query.split()
    for i, word in enumerate(words):
        if word.isdigit():
            k = int(word)
        elif word.lower() == "top" and i < len(words) - 1 and words[i+1].isdigit():
            k = int(words[i+1])
    return k         

def find_colleges(location):
    colleges = []
    for university, details in professors.items():
        for detail in details:
            if detail.get('location',None) == location:
                colleges.append(university)
    return colleges
    
    
# Example usage
query = ' '.join(sys.argv[1:])
categories, location = process_query(query)
k = extract_parameters(query)

for category in categories:
    if category == "github":
        top_k_profiles = fetch_topkgithub(k, location)
        
        for profile in top_k_profiles:
            print(f"GitHub ID: {profile['github_id']}\n Link: https://github.com/{profile['github_id']}\n  Total Score: {profile['total_score']}\n")
    elif category == "scholar":
        top_k_profiles = topk_googlescholar(k, location)
        write_profile_to_csv(top_k_profiles)
        for profile in top_k_profiles:
            print(f"Name: {profile['name']}\n relevance: {profile['relevance_score']}\n citations: {profile['citations']}\n H-index: {profile['h_index']}\n Degree/Institute of Work: {profile['degree_type']}\n Profile Link: {profile['scholar_url']}\n Linkedin Link: {profile['Linkedin']}\n")
    elif category == "student":
        colleges = find_colleges(location)
        for college in colleges:
            remain(college, k)
            time.sleep(2)
