from rest_framework.decorators import api_view
from rest_framework.response import Response
import spacy

nlp = spacy.load("en_core_web_sm")


def clean_data(data):
    """
    Clean the data fields by removing leading/trailing whitespace and handling empty strings.
    """
    cleaned_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned_data[key] = value.strip()
        else:
            cleaned_data[key] = value
    return cleaned_data


def extract_skills(text):
    """
    Extract skills from the given text using NLP.
    """
    skills = []
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "NOUN":
            skills.append(token.text)
    return list(set(skills))


# create your api here

@api_view(['GET', 'POST'])
def data_pipe(request):
    """Please provide post request. this api is only for practice"""
    if request.method == 'GET':
        return_data = {
            'error': '1',
            'message': 'Please provide Post request.'
        }
        return Response(return_data)

    elif request.method == "POST":
        cleaned_data = clean_data(request.data)
        skills = extract_skills(cleaned_data.get("CleanContent", ""))
        job_post_data = {
            "title": cleaned_data.get("Title"),
            "salary": cleaned_data.get("Salary"),
            "location": cleaned_data.get("Location"),
            "company": cleaned_data.get("Company"),
            "description": cleaned_data.get("Description"),
            "skills": skills
        }

        return Response(job_post_data)
