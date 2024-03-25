from rest_framework.decorators import api_view
from rest_framework.response import Response
import spacy
import re
from dateutil import parser

nlp = spacy.load("en_core_web_sm")


def clean_text(data):
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


def clean_date(text):
    date_formats = [
        r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}',  # DD/MM/YYYY or similar
        r'\d{4}[./-]\d{1,2}[./-]\d{1,2}',  # YYYY/MM/DD or similar
        r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[, ]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[ ]+\d{1,'
        r'2}(?:st|nd|rd|th)?[,]?[ ]+\d{4}',  # Day, Month DD, YYYY
        r'\d{1,2}(?:st|nd|rd|th)?[ ]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[.,]?[ ]+\d{4}',  # Month YYYY or similar
        r'\d{4}-\d{2}-\d{2}',  # ISO format YYYY-MM-DD
        r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
        r'\d{2}-\d{2}-\d{2}',  # MM-DD-YY
        r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}',  # DD Month YYYY or similar
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}(?:st|nd|rd|th)?, \d{2,4}',  # Month DD, YYYY or similar
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{2,4}',  # Month DD, YYYY or similar
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}',  # Month YYYY or similar
        r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',  # DD Month or similar
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY or similar
    ]
    date_pattern = re.compile('|'.join(date_formats), re.IGNORECASE)
    match = date_pattern.search(text)
    if match:
        date_str = match.group(0)
        try:
            parsed_date = parser.parse(date_str, fuzzy=True)
            return parsed_date.strftime('%Y-%m-%d')  # Standardize date format
        except ValueError:
            return None
    else:
        return None


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
        cleaned_data = clean_text(request.data)
        job_post_data = {
            "title": cleaned_data.get("Title"),
            "salary": cleaned_data.get("Salary"),
            "location": cleaned_data.get("Location"),
            "company": cleaned_data.get("Company"),
            "description": cleaned_data.get("Description"),
            "date": clean_date(cleaned_data.get("Date")),
            "skills": extract_skills(cleaned_data.get("Description"))
        }
        return Response(job_post_data)

