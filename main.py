from prof import PROFESSORS  
from perplexity_api import PerplexityAPI  
from github import get_github_score  
from university import UNIVERSITY_SCORES
import requests

perplexity_api = PerplexityAPI(api_key="apikey")

def find_students(scrap):
    candidates = []
    for student_data in scrap.get("students", []):
        name = student_data.get("name", "")
        degree_type = student_data.get("degree_type", "")
        field_of_study = student_data.get("field_of_study", "")
        professor_guide = student_data.get("professor_guide", "")
        github_repo = student_data.get("github_repo", "")
        github_score = get_github_score(github_repo) if github_repo else 0
        uni_score = UNIVERSITY_SCORES.get(student_data.get("university", ""), 0)
        prof_score = student_data.get("prof_score", 0)
        h_index = student_data.get("h_index", 0)
        
        candidate = Candidate(
            name=name,
            degree_type=degree_type,
            field_of_study=field_of_study,
            professor_guide=professor_guide,
            github_repo=github_repo,
            github_score=github_score,
            uni_score=uni_score,
            prof_score=prof_score,
            h_index=h_index
        )
        candidates.append(candidate)
    return candidates

def main():
    all_candidates = []
    
    for university, professors in PROFESSORS.items():
        for prof in professors:
            webpage = prof["webpage"]
            try:
                scrap = perplexity_api.scrape_webpage(webpage)
                candidates = find_students(scrap)
                all_candidates.extend(candidates)
            except requests.exceptions.RequestException as e:
                print(f"Failed to scrape {webpage}: {e}")
                continue

    final_list = normaliser(all_candidates)            
    for candidate in all_candidates:
        print(candidate.calculate_overall_score)

if __name__ == "__main__":
    main()
