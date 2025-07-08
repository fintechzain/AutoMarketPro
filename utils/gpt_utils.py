from dotenv import load_dotenv
from openai import OpenAI
import os
import dotenv as dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_content(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT Error:", e)
        return None



def repurpose_content(original, format_type):
    prompt = f"Repurpose the following content into a {format_type}:\n\n{original}"
    return generate_content(prompt)

def generate_persona(prompt):
    return generate_content(prompt)
