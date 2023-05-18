from fastapi import FastAPI, HTTPException,Body,File,Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import asyncio
import uvicorn
from pdf_search import *
from add_remove_pdf import *

app =FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/")
# async def helloW():
#     return {"hello":"world"}

# @app.post("/search")
# async def query_pdf(json_data: dict = Body(...)):
#     value = json_data.get("query")
#     response = qa_result(value,"refine")
#     # print(response)
#     return response

# @app.post("/upload")
# async def upload_pdf(file: bytes = File(...), api_key: str = Form(...), text: str = Form(...)):
#     # Process the uploaded file, API key, and text
#     # Save the file, manipulate it, or perform any required operations

#     # Print the file name
#     file_name = file.filename
#     print("Uploaded file name:", file_name)

#     # Example: Save the file
#     with open("uploaded_file.pdf", "wb") as f:
#         f.write(file)

#     return {"message": "PDF file uploaded successfully"}


@app.post("/search")
async def upload_pdf(file: UploadFile = File(...), api_key: str = Form(...), text: str = Form(...)):
   
    file_path= await save_pdf(file)
    print(file_path)

    # Print the file name
    file_name = file.filename
    print("Uploaded file name:", file_name)
    openAi_api=api_key
    query=text
    response = qa_result(openAi_api,query,file_name,"refine")
    rem_pdf(file_path)
    print(response)
    return response
