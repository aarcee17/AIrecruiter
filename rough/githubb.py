import subprocess
import json
import spacy
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

nlp = spacy.load('en_core_web_sm')

oracle = pipeline("question-answering", model="deepset/roberta-base-squad2")
theta = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

ai_ml_prompts = [
    "LLM",
    "BERT",
    "transformers",
    "AI",
    "machine learning",
    "data science",
    "deep learning"
]

def run_node_script(username):
    result = subprocess.run(
        ['node', 'scraper.js'], 
        input=username, 
        text=True, 
        capture_output=True, 
        check=True
    )
    output = result.stdout.strip().split('\n')
    user_data = json.loads(output[0])['user']
    repos_data = json.loads(output[1])['repos']
    return user_data, repos_data

def fetch_repo_data(username):
    user_data, repos_data = run_node_script(username)
    repo_data = []
    for repo in repos_data:
        reponame = repo['name']
        stars = repo['stargazers_count']
        description = repo['description']
        readme_content = repo['readme'] if 'readme' in repo else ''
        full_text = (description or '') + ' ' + (readme_content or '')
        repo_data.append({
            'name': reponame,
            'stars': stars,
            'description': description,
            'full_text': full_text
        })
    return repo_data

def evaluate_project_relevance(full_text):
    qembed = theta.encode(ai_ml_prompts, normalize_embeddings=True)
    embeddings = theta.encode([full_text], normalize_embeddings=True)
    similarities = [cos_sim(qembed[i], embeddings)[0].item() for i in range(len(ai_ml_prompts))]
    relevance_score = sum(similarities) / len(similarities)
    return relevance_score

def score_repositories(repo_data):
    scores = []
    for repo in repo_data:
        stars_score = repo['stars']  
        project_relevance_score = evaluate_project_relevance(repo['full_text']) * 20 
        total_score = stars_score + project_relevance_score
        scores.append({
            'name': repo['name'],
            'score': total_score,
            'stars': repo['stars'],
            'description': repo['description'],
            'relevance_score': project_relevance_score
        })
    return scores

def aggregate_scores(scores):
    total_score = sum(repo['score'] for repo in scores)
    return total_score

def score_github_user(username):
    repo_data = fetch_repo_data(username)
    scores = score_repositories(repo_data)
    total_score = aggregate_scores(scores)
    return total_score, scores

def main():
    username = input("Enter the GitHub username: ")
    try:
        total_score, detailed_scores = score_github_user(username)
        print(f"Total GitHub Score for {username}: {total_score}")
        print("Detailed Scores:")
        for score in detailed_scores:
            print(f"Repository: {score['name']}, Score: {score['score']}, Stars: {score['stars']}, Description: {score['description']}, Relevance Score: {score['relevance_score']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
