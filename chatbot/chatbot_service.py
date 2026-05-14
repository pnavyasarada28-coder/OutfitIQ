import os
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Use find_dotenv to correctly locate .env in the parent directory
load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

prompt = ChatPromptTemplate.from_template(
    """
You are an elite AI Fashion Stylist for 'OutfitIQ'. Your goal is to provide highly personalized, trend-aware, and aesthetic fashion advice.
You understand color theory, body types, seasonal trends, and modern streetwear, casual, and formal aesthetics.
Your tone should be friendly, highly professional, and inspiring.
If asked about things outside of fashion, gently guide the user back to clothing and styling.

User Question:
{query}

Respond in a concise, stylish, and easily readable manner.
"""
)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

def get_chatbot_response(user_query):
    if not user_query or not str(user_query).strip():
        return "Please enter a fashion question or outfit request!"

    if not isinstance(user_query, str):
        return "I can only process text input. Please try again."

    user_query = user_query.strip()
    if len(user_query) > 300:
        return "Your question is a bit too long! Please keep it under 300 characters for the best styling advice."

    try:
        response = chain.invoke({"query": user_query})
        return response
    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "429" in error_msg:
            return "Our AI stylist is currently helping too many customers. Please try again in a few moments!"
        print("Chatbot Error:", e)
        return "I'm having a little trouble connecting to my fashion database right now. Please try again later!"