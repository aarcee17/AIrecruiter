from github import score_github_user
from googlescholar import *

class Person:
    def __init__(self, name, workuni=None, github=None, scholarurl=None, linkedin=None):
        self.name = name
        self.work = workuni
        self.github = github
        self.scholar = scholarurl
        self.linkedin = linkedin
        self.github_score = score_github_user(self.github)
        
        