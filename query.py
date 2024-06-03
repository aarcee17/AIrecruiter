from transformers import pipeline
import re

classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

github_keywords = ["github", "code", "repository", "programmer", "developer", "Llama-3"]
scholar_keywords = ["google scholar", "scholar", "research", "citations", "paper", "publication"]
student_keywords = ["student", "lab", "university", "AI lab", "researcher"]

def classify_query(query):
    categories = []
    if any(keyword in query.lower() for keyword in github_keywords):
        categories.append("github")
    if any(keyword in query.lower() for keyword in scholar_keywords):
        categories.append("scholar")
    if any(keyword in query.lower() for keyword in student_keywords):
        categories.append("student")
    return categories if categories else ["unknown"]


def extract_parameters(query):
    k = 15
    location = None
    words = query.split()
    for i, word in enumerate(words):
        if word.isdigit():
            k = int(word)
        elif word.lower() == "top" and i < len(words) - 1 and words[i+1].isdigit():
            k = int(words[i+1])
        elif word.lower() == "in" and i < len(words) - 1:
            location = words[i+1]
    return k, location

def process_query(query):
    classifications = classify_query(query)
    k, location = extract_parameters(query)
    return classifications, k, location

query = "I want to find top 10 programmer who have worked on Llama-3 in Boston"
classifications, k, location = process_query(query)
print(f"Classifications: {classifications}, k: {k}, location: {location}")

# for classification in classifications:
#     if classification == "github":
        
#         print(f"Fetching top {k} GitHub profiles in {location or 'global'}...")
#         # fetch_github_profiles(k, location)
#     elif classification == "scholar":
#         # Call the function to handle Google Scholar profiles
#         print(f"Fetching top {k} Google Scholar profiles in {location or 'global'}...")
#         # fetch_scholar_profiles(k, location)
#     elif classification == "student":
#         # Call the function to handle student profiles
#         print(f"Fetching top {k} student profiles in {location or 'global'}...")
#         # fetch_student_profiles(k, location)
