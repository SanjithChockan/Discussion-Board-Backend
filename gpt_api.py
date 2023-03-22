import openai
openai.api_key = "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"

# Testing GPT-3.5 "davinci" model to generate answer to question
prompt = "What is the most important aspect of discrete math?"
response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=100
)
generated_text = response.choices[0].text
print(generated_text)