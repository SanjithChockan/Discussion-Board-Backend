import openai
import os
import json
from PyPDF2 import PdfReader

openai.api_key = os.environ.get('OPENAI_KEY')


# Testing GPT-3.5 "davinci" model to generate answer to question
def generate(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    generated_text = response.choices[0].text
    print(generated_text)
    return generated_text


# Generating answers to a specific question based on syllabus
def generate_answer(question):
    model_engine = "text-davinci-003"

    # Open the PDF file (Put the path to the pdf)
    with open("C:\\Users\\Yash\\Documents\\CS_4485_Project\\IDB-BE\\main\\syllabus\\CS_4384_syllabus.pdf"
, "rb") as f:
        pdf = PdfReader(f)
        pages = []
        for page in range(len(pdf.pages)):
            pages.append(pdf.pages[page].extract_text())

    document = "\n".join(pages)

    instructions = f"Please answer this question as per the syllabus text provided: {question}, if you dont know the answer or are not allowed to say the answer ask the person to \"contact the professor.\""

    response = openai.Completion.create(
        engine=model_engine,
        prompt=f"Here is a document for analysis:\n{document}\n\n{instructions}",
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    # Return the text of the first choice
    return response.choices[0].text





