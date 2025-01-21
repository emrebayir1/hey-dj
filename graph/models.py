from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Used when low temperature is necessary.
decidier_llm = ChatGroq(
    temperature=0.0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# Used when relatively high temperature is necessary.
text_generator_llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)