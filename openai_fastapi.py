from fastapi import FastAPI, Request, File, UploadFile,HTTPException, Depends
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.templating import Jinja2Templates
import openai
import os
from dotenv import load_dotenv
from sql_app.database import SessionLocal, engine
from sql_app.models import UploadedFile
from sql_app import models

models.Base.metadata.create_all(engine)

load_dotenv(override=True)
app = FastAPI()
app.secret_key = os.getenv("OPENAI_SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)
templates = Jinja2Templates(directory="templates")

async def check_api_key(api_key: str = Depends(api_key_header)):
    if api_key != openai.api_key:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return api_key

# Protected route
@app.get("/protected")
async def protected_route(api_key: str = Depends(check_api_key)):
    return {"message": "This is a protected route"}

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "message": "Awaiting Upload ..."})

t=""
@app.post('/')
async def upload_file(request: Request, file: UploadFile = File(...)):
    global t
    text = await file.read()
    content = text.decode("utf-8")
    t = text.decode("utf-8")
    with open("uploads/" + file.filename, "wb") as f:
        f.write(text)

    new_file=UploadedFile(filename=file.filename, content=content)
    db=SessionLocal()

    existing_file = db.query(UploadedFile).filter(UploadedFile.filename == file.filename).first()
    if existing_file:
        return templates.TemplateResponse("home.html",
                                          {"request": request, "message": "File with the same name already exists in db. \n Awaiting new upload ...", "filename": file.filename})
    else:
        db.add(new_file)
        db.commit()
        db.close()
        return templates.TemplateResponse("home.html", {"request": request, "message": "Success ! \n Awaiting new upload ...", "filename": file.filename})


@app.post('/getSummary')
def get_summary():
    global t
    prompt = "from this text supplied here please without any further introduction give a summary of the text with heading SUMMARY :  \n"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    response= completion.choices[0].message["content"]
    response = response.replace('\n', '<br>')
    return response


@app.post('/getQuestionAndAnswer')
def get_question_and_answer():
    global t
    prompt = "Based on the text supplied here, please provide five questions and their answers with without any introduction. For each question and answer set, use the format QUESTION=question ANSWER=answer , and include the marker 'NEW-QUESTION-BEGINS' to start a new question and answer set. 'QUESTION' and 'ANSWER'should be in uppercase letters and always be followed by = (equal to ) sign. NEW LINE AFTER EVERY QUESTION MARK.Provide heading Q&A at the top. Avoid any additional introduction beyond the instructions outlined here. Here is the supplied text:  "
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    response = completion.choices[0].message["content"]
    response = response.replace('\n', '<br>')
    return response



@app.post('/getGlossary')
def get_glossary():
    global t
    prompt = "Please upfront (without any introduction) based on the text supplied here, give a set of five glossary terms and their definitions. For the 1st glossary term, you would respond like TERM=First term DEFINITION: definition of first term. For the 2nd glossary term, you would respond like TERM= 2nd term DEFINITION: Definition of 2nd term and so on. After each term and definition set, please include the marker 'NEW-TERM-BEGINS' to start a new glossary term. Please remember that 'TERM' , 'DEFINITION' and 'NEW-TERM-BEGINS' should always be in uppercase letters. Henceforth your output will be like TERM=First term DEFINITION: definition of first term NEW-TERM-BEGINS TERM= 2nd term DEFINITION: Definition of 2nd term NEW-TERM-BEGINS TERM= 3rd term DEFINITION: Definition of 3rd term and so on . Provide heading GLOSSARY in the starting. "
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    response = completion.choices[0].message["content"]
    response = response.replace('\n', '<br>')
    return response


@app.post('/getQuestionMultipleChoice')
def get_question_multiple_choice():
    global t
    prompt = "Please generate 5 multiple choice questions based on the text provided here. The questions should have 4 options each, and the options should be denoted by A), B), C), and D). Please ensure that each question ends with a question mark (?).Give the answer in the last line after options for every question. For example: Q1) What is the capital of France? A) London B) Paris C) Rome D) Berlin. Begin each question with 'Q' followed by a number, and separate the options with a comma. After each question, please include the marker 'NEW-QUESTION-BEGINS' to start a new question. There should be no additional introduction beyond the instructions outlined here. The supplied text is: "
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "/start"},
            {"role": "user", "content": prompt + str(t)}
        ]
    )
    response = completion.choices[0].message["content"]
    response = response.replace('\n', '<br>')
    return response


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
