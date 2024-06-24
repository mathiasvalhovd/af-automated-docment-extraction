from openai import OpenAI
api_key=" "

def embed_txt(text, model):
    client = OpenAI(api_key)
    response = client.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding