# import requests
# from bs4 import BeautifulSoup
# from googlesearch import search
# from googlescholar import fetch_scholar_data
# from github import score_github_user
# import time
# from prof import *
# from candidate import *
# from googlescholar import *
# from github import *
# from transformers import pipeline
# import csv

# class CandidateDetails:
#     def __init__(self, name, university, degree_type, field_of_study, professor_guide, github_username, h_index):
#         self.name = name
#         self.university = university
#         self.degree_type = degree_type
#         self.field_of_study = field_of_study
#         self.professor_guide = professor_guide
#         self.github_username = github_username
#         self.h_index = h_index

#     def __repr__(self):
#         return f"CandidateDetails(name={self.name}, university={self.university}, degree_type={self.degree_type}, field_of_study={self.field_of_study}, professor_guide={self.professor_guide}, github_username={self.github_username}, h_index={self.h_index})"

# # nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# # def extract_students_from_prof_homepage(url):
# #     response = requests.get(url)
# #     soup = BeautifulSoup(response.text, 'html.parser')
# #     students = []

# #     text_content = ' '.join([p.text.strip() for p in soup.find_all('p')])
# #     nlp_results = nlp(text_content)

# #     # Process the structured sections
# #     for student_section in soup.select('.student-section'):
# #         name = student_section.find('h3').text.strip()
# #         degree_type = student_section.find('p', class_='degree-type').text.strip()
# #         field_of_study = student_section.find('p', class_='field-of-study').text.strip()
# #         students.append((name, degree_type, field_of_study))



# #     return students

# # Example usage
# # if __name__ == "__main__":
# #     url = "http://www.someuniversity.edu/professor-page"
# #     extracted_students = extract_students_from_prof_homepage(url)
# #     for student in extracted_students:
# #         print(student)



# def fetch_candidate_details(name, university, prof,degree_type, field_of_study):
#     scholar_url = get_student_url(name,prof, university)
#     scholar_data = fetch_scholar_data(scholar_url) if scholar_url else {'h_index': 0}
#     github_username = search_github_username(name, university)
#     h_index = scholar_data['h_index']
#     return CandidateDetails(name, university, degree_type, field_of_study,prof, github_username, h_index)

# def search_github_username(name, university):
#     query = f"{name} " "Machine Learning GitHub"
#     for url in search(query, num_results=5):
#         if 'github.com' in url:
#             return url.split('/')[-1]
#     return "nope not found"

# # def main(professors):
# #     all_candidates = []
# #     for university, prof_list in professors.items():
# #         for prof in prof_list:
# #             students = extract_students_from_prof_homepage(prof['webpage'])
# #             for name, degree_type, field_of_study in students:
# #                 candidate = fetch_candidate_details(name, university, degree_type,prof, field_of_study)
# #                 all_candidates.append(candidate)
# #                 time.sleep(1)  
# #     return all_candidates

# # if __name__ == "__main__":
# #     candidates = main(professors)
# #     for candidate in candidates:
# #         print(candidate)
# def main():
#     # Read from CSV
#     students = []
#     with open('filtered_authorss.csv', newline='') as csvfile:
#         #next(csvfile)
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             students.append(row)
    
#     student_details = []
#     for student in students:
#         details = fetch_candidate_details(student['name'],student['professor'], student['university'], student['degree_type'], student['field_of_study'])
#         student_details.append(details)
#         time.sleep(1)  

#     for detail in student_details:
#         print(detail)

# # def main():
# #     prof_name = "Yoshua Bengio"
# #     student_name = "Alexander Tong"
# #     college = "Universaite de Montreale"
# #     edu = "PhD"
# #     deg = "Computer Science"
# #     fetch_candidate_details(student_name,college,prof_name,edu,deg).printcandidate()
    
# if __name__ == "__main__":
#     main()   
    