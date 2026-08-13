import os
import streamlit as st

from dotenv import load_dotenv
from google import genai

from prompt_engine import (
    build_copywriting_prompt,
    build_tone_transform_prompt
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to your .env file locally or Streamlit Secrets."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"
