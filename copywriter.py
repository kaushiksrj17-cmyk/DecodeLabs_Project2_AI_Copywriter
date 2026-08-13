import os

from dotenv import load_dotenv
from google import genai

from prompt_engine import (
    build_copywriting_prompt,
    build_tone_transform_prompt
)

# ---------------------------------------------------------
# Environment / API Configuration
# ---------------------------------------------------------

load_dotenv()


def get_api_key():
    """
    Get Gemini API key from:
    1. Environment variable / local .env
    2. Streamlit Cloud Secrets
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    # Streamlit Cloud fallback
    try:
        import streamlit as st

        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]

    except Exception:
        pass

    return None


API_KEY = get_api_key()

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Add GEMINI_API_KEY to your .env file locally "
        "or Streamlit Cloud Secrets."
    )


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(api_key=API_KEY)

# Use the Gemini model that is currently configured for
# your working DecodeLabs project.
MODEL_NAME = "gemini-2.5-flash"


# ---------------------------------------------------------
# Helper: Gemini Generation
# ---------------------------------------------------------

def _generate(prompt, temperature=0.7, top_p=0.9):
    """
    Send a prompt to Gemini and return generated text.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temperature,
            "top_p": top_p,
        }
    )

    if not response:
        raise RuntimeError("Gemini returned an empty response.")

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned no generated text.")

    return text.strip()


# ---------------------------------------------------------
# Generate Marketing Copy
# ---------------------------------------------------------

def generate_copy(
    product_name,
    product_description,
    platform,
    tone,
    audience,
    brand_voice,
    copy_length,
    temperature=0.7,
    top_p=0.9
):
    """
    Generate marketing copy using the dynamic prompt engine.
    """

    prompt = build_copywriting_prompt(
        product_name=product_name,
        product_description=product_description,
        platform=platform,
        tone=tone,
        audience=audience,
        brand_voice=brand_voice,
        copy_length=copy_length
    )

    return _generate(
        prompt,
        temperature=temperature,
        top_p=top_p
    )


# ---------------------------------------------------------
# Transform Existing Copy
# ---------------------------------------------------------

def transform_copy(
    existing_copy,
    target_tone,
    target_platform,
    target_audience,
    brand_voice,
    output_length,
    temperature=0.7,
    top_p=0.9
):
    """
    Transform existing marketing copy into a new
    tone/platform/audience/brand voice.
    """

    prompt = build_tone_transform_prompt(
        existing_copy=existing_copy,
        target_tone=target_tone,
        target_platform=target_platform,
        target_audience=target_audience,
        brand_voice=brand_voice,
        output_length=output_length
    )

    return _generate(
        prompt,
        temperature=temperature,
        top_p=top_p
    )
