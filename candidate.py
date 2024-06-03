from university import *
from github import *

class Candidate:
    def __init__(self, name,uni, degree_type, field_of_study, professor_guide, github_username, h_index):
        self.name = name
        self.uni = uni
        self.degree_type = degree_type
        self.field_of_study = field_of_study
        self.professor_guide = professor_guide
        self.github_username = github_username
        self.github_score = self.calculate_github_score()
        self.uni_score = self.calculate_uni_score()
        #self.prof_score = self.calculate_prof_score()
        self.h_index = h_index
        self.overall_score = self.calculate_overall_score()
        self.normalized_scores = {}
    def calculate_github_score(self):
        total_score = 0
        username = self.github_username
        try:
            total_score, user_profile, detailed_scores = score_github_user(username)
            print(f"Total GitHub Score for {username}: {total_score}")
            # print("User Profile:")
            # print(user_profile)
            # print("Detailed Scores:")
            #for score in detailed_scores:
               # print(f"Repository: {score['name']}, Score: {score['score']}, Stars: {score['stars']}, Description: {score['description']}, Relevance Score: {score['relevance_score']}")
        except Exception as e:
            print(f"Error: {e}")
        return total_score
    def printcandidate(self):
        print(f"Candidate: {self.name}, Uni: {self.uni}, Degree: {self.degree_type}, Field of Study: {self.field_of_study}, Prof Guide: {self.professor_guide}, GitHub Score: {self.github_score}, Uni Score: {self.uni_score}, H-Index: {self.h_index}, Overall Score: {self.overall_score}")
    def calculate_uni_score(self):
        return UNIVERSITY_SCORES[self.uni]
    
    # def calculate_prof_score(self):
        
    #     return 0
    
    def calculate_overall_score(self):
        return self.github_score + self.uni_score + self.h_index
    def __repr__(self):
        return f"Candidate({self.name}, Overall Score: {self.overall_score})"

# if __name__ == "__main__":
#     candidate = Candidate(
#         name="raj",
#         uni = "MIT",
#         degree_type="PhD",
#         field_of_study="AI",
#         professor_guide="MIT",
#         github_username="aarcee17",
#         h_index=50
#     )
#     print(candidate)
