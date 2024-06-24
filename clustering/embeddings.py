def embed_txt(text, model):
    client = OpenAI(api_key="sk-proj-UBVzZbqQLamBsQQNWlsjT3BlbkFJdOHw9uCEA6QFdvZpCxu7")
    response = client.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding