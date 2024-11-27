import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def summarize_text_with_gpt(text):
    prompt = f"""
    Here is the content of a research paper:
    {text}

    Please provide a detailed summary in very simple English, focusing on the paper's impact.
    Format: 
    Write 5 bullet points explaining the importance of this research.
    Focus on facts and statistics whenever possible.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": prompt,
        }]
    )
    return response.choices[0].message.content.strip()
