import openai
from .openai_key import api_key
openai.api_key = api_key

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