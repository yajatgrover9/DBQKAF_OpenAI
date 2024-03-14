from fastapi.testclient import TestClient
from openai_fastapi import *
import os
from dotenv import load_dotenv
load_dotenv()
client = TestClient(app)
api_key=os.getenv("OPENAI_API_KEY")
def test_home():
    response = client.get('/')
    assert response.status_code == 200

def test_protected_route_with_valid_api_key():
    valid_api_key = api_key
    headers = {"X-API-Key": valid_api_key}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200

def test_upload_file():
    with open("TEST1-NeuralNetworks.txt", "rb") as file:
        response = client.post('/', files={"file": ("TEST1-NeuralNetworks.txt", file, "text/plain")})
    assert response.status_code == 200

def test_duplicate_file_upload():
    with open("TEST1-NeuralNetworks.txt", "rb") as file:
        response = client.post('/', files={"file": ("TEST1-NeuralNetworks.txt", file, "text/plain")})
    assert response.status_code == 200

def test_get_summary():
    response = client.post('/getSummary')
    assert response.status_code == 200

def test_get_question_and_answer():
    response = client.post('/getQuestionAndAnswer')
    assert response.status_code == 200

def test_get_glossary():
    response = client.post('/getGlossary')
    assert response.status_code == 200


def test_get_question_multiple_choice():
    response = client.post('/getQuestionMultipleChoice')
    assert response.status_code == 200

