import openai
import os
import json
import boto3
from flask import Response

from PyPDF2 import PdfReader
from io import BytesIO

openai.api_key = os.environ.get("OPENAI_KEY")


def generate(prompt):
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, max_tokens=100
    )
    generated_text = response.choices[0].text
    print(generated_text)
    return generated_text


def get_pdf(course_id):
    syllabi = {
        1: "HIST_1301_syllabus.pdf",
        2: "GST_2300_syllabus.pdf",
        3: "ECS_3390_syllabus.pdf",
        4: "CS_4384_syllabus.pdf",
        5: "CS_4348_syllabus.pdf",
        6: "CS_3377_syllabus.pdf",
        7: "CS_2305_syllabus.pdf",
        8: "CS_1336_syllabus.pdf",
    }
    s3 = boto3.client("s3")
    bucket_name = "syllabus212"
    file_name = f"{syllabi[course_id]}"
    file_obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = file_obj["Body"].read()
    return Response(file_content, mimetype="application/pdf")


# Generating answers to a specific question based on syllabus
def generate_answer(question, course_id):
    model_engine = "text-davinci-003"

    # Open the PDF file (Put the path to the pdf)
    with BytesIO(get_pdf(course_id).data) as f:
        pdf = PdfReader(f)
        pages = []
        for page in range(len(pdf.pages)):
            pages.append(pdf.pages[page].extract_text())

    document = "\n".join(pages)

    instructions = f'Please answer this question as per the syllabus text provided: {question}, if you dont know the answer or are not allowed to say the answer ask the person to "Please contact the professor." a very concise response'
    response = openai.Completion.create(
        engine=model_engine,
        prompt=f"Here is a document for analysis:\n{document}\n\n{instructions}",
        temperature=0.7,
        max_tokens=131,
        n=1,
        stop=None,
    )

    # Return the text of the first choice
    return response.choices[0].text
