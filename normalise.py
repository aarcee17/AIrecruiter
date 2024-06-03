import numpy as np
from candidate import Candidate

def normalize_scores(candidates):
    def get_normalized_scores(values):
        mean = np.mean(values)
        std_dev = np.std(values)
        z_scores = [(x - mean) / std_dev for x in values]
        normalized = [50 + (z * 10) for z in z_scores]
        return normalized

    github_scores = [c.github_score for c in candidates]
    uni_scores = [c.uni_score for c in candidates]
    #prof_scores = [c.prof_score for c in candidates]
    h_indices = [c.h_index for c in candidates]

    normalized_github = get_normalized_scores(github_scores)
    normalized_uni = get_normalized_scores(uni_scores)
    #normalized_prof = get_normalized_scores(prof_scores)
    normalized_h_index = get_normalized_scores(h_indices)

    for i, candidate in enumerate(candidates):
        candidate.normalized_scores['github_score'] = normalized_github[i]
        candidate.normalized_scores['uni_score'] = normalized_uni[i]
        #candidate.normalized_scores['prof_score'] = normalized_prof[i]
        candidate.normalized_scores['h_index'] = normalized_h_index[i]
        #candidate.normalized_scores['overall_score'] = (normalized_github[i] + normalized_uni[i] + normalized_prof[i] + normalized_h_index[i]) / 4
        candidate.normalized_scores['overall_score'] = (normalized_github[i] + normalized_uni[i]+ normalized_h_index[i]) / 4
    return candidates

# Example usage
if __name__ == "__main__":
    candidates = [

    Candidate("Alice", "MIT", "PhD", "AI", "Prof. Adams", "aliceai", 45),
    #Candidate("Bob", "Stanford University", "Master", "ML", "Prof. Baker", "bobbaker", 35),
    #Candidate("Charlie", "Harvard University", "PhD", "NLP", "Prof. Charles", "charlienlp", 65),
    Candidate("Diana", "University of California, Berkeley (UC Berkeley)", "Master", "Robotics", "Prof. Dane", "dianarobot", 75),
    #Candidate("Eve", "MIT", "PhD", "AI", "Prof. Eton", "eveai", 80),
    #Candidate("Frank", "Stanford University", "Master", "ML", "Prof. Fawn", "frankml", 28),
    #Candidate("Grace", "Harvard University", "PhD", "NLP", "Prof. Graham", "gracenlp", 55),
    Candidate("Hank", "University of California, Berkeley (UC Berkeley)", "Master", "Robotics", "Prof. Hunt", "hankrobot", 62),
    #Candidate("Ivy", "MIT", "PhD", "AI", "Prof. Ives", "ivygith", 48),
    Candidate("Jack", "Stanford University", "Master", "ML", "Prof. Jules", "jackml", 33),
    Candidate("Kara", "Harvard University", "PhD", "NLP", "Prof. Kite", "karanlp", 70),
    #Candidate("Leo", "University of California, Berkeley (UC Berkeley)", "Master", "Robotics", "Prof. Lane", "leorobot", 74),
    Candidate("Mia", "MIT", "PhD", "AI", "Prof. Moon", "miagit", 77),
    #Candidate("Nick", "Stanford University", "Master", "ML", "Prof. Nile", "nickml", 32),
    # Candidate("Olivia", "Harvard University", "PhD", "NLP", "Prof. Oak", "olivianlp", 60),
    # Candidate("Pete", "University of California, Berkeley (UC Berkeley)", "Master", "Robotics", "Prof. Pine", "peterobot", 63),
    # Candidate("Quinn", "MIT", "PhD", "AI", "Prof. Quill", "quinnai", 47),
    # Candidate("Rachel", "Stanford University", "Master", "ML", "Prof. Ray", "rachelml", 31),
    Candidate("Sam", "Harvard University", "PhD", "NLP", "Prof. Stone", "samnlp", 68),
    # Candidate("Tina", "University of California, Berkeley (UC Berkeley)", "Master", "Robotics", "Prof. Turner", "tinarobot", 76),
    # Candidate("Uma", "MIT", "PhD", "AI", "Prof. Upton", "umaai", 81),
    # Candidate("Victor", "Stanford University", "Master", "ML", "Prof. Vale", "victorml", 29),
    # Candidate("Wendy", "Harvard University", "PhD", "NLP", "Prof. West", "wendynlp", 57),
    # Candidate("Xavier", "University of California, Berkeley (UC Berkeley)", "Master", "Robotics", "Prof. Xavier", "xavierrobot", 61),
    # Candidate("Yara", "MIT", "PhD", "AI", "Prof. Yale", "yaragith", 49)


    ]

    normalized_candidates = normalize_scores(candidates)

    for candidate in normalized_candidates:
        print(f"Candidate: {candidate.name}")
        print(f"Normalized Scores: {candidate.normalized_scores}")
        print()

#     normalized_candidates = normalize_scores(candidates)
# # Sort candidates by normalized score in descending order
#     sorted_candidates = sorted(normalized_candidates, key=lambda x: x.normalized_scores['overall_score'], reverse=True)

#     # Display sorted candidates
#     for candidate in sorted_candidates:
#         print(candidate)
