from transformers import pipeline
import requests 
from bs4 import BeautifulSoup

nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def fetch_webpage_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text_content = ' '.join(p.text.strip() for p in soup.find_all('p'))
    print(text_content)
    return text_content

def extract_entities(text):
    return nlp(text)

def process_entities(entities):
    students = []
    for entity in entities:
        if entity['entity'] == 'B-PER': 
            students.append(entity['word'])  
    return students

def extract_students(url):
    text = fetch_webpage_text(url)
    entities = extract_entities(text)
    students = process_entities(entities)
    return students

if __name__ == "__main__":
    url = ["https://people.csail.mit.edu/regina/"]
    
   # url = ["https://people.csail.mit.edu/regina/","https://people.csail.mit.edu/tommi/"]
    for u in url:
        
        fetch_webpage_text(u)
        print("\n\n\n\n\n\n\n##############################\n\n\n\n")
    # stud = []
    # for j in extract_entities(fetch_webpage_text(url)):
    #     if j['entity'] == 'I-PER':
    #         stud.append(j['word'])
        print(extract_entities(fetch_webpage_text(u)))        
            
    # student_names = extract_students(url)
    # print("names:", student_names)
