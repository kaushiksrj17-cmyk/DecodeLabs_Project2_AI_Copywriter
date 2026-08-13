import os

from dotenv import load_dotenv
from google import genai

from prompt_engine import (
    build_copywriting_prompt,
    build_tone_transform_prompt
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# GENERATE NEW COPY
# ============================================================

def generate_copy(
    product_name,
    product_description,
    platform,
    tone,
    audience="General Audience",
    brand_voice="Modern",
    copy_length="Medium",
    temperature=0.7,
    top_p=0.9,
    variation_number=None
):
    """
    Generate marketing copy using Gemini.

    Supports:
    - Dynamic prompts
    - Platform optimization
    - Tone
    - Audience
    - Brand voice
    - Length
    - Temperature
    - Top_P
    - Multiple variations
    """

    prompt = build_copywriting_prompt(
        product_name=product_name,
        product_description=product_description,
        platform=platform,
        tone=tone,
        audience=audience,
        brand_voice=brand_voice,
        copy_length=copy_length,
        variation_number=variation_number
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temperature,
            "top_p": top_p
        }
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text.strip()


# ============================================================
# TRANSFORM EXISTING COPY
# ============================================================

def transform_copy(
    original_text,
    target_tone,
    platform,
    audience="General Audience",
    brand_voice="Modern",
    copy_length="Medium",
    temperature=0.7,
    top_p=0.9
):
    """
    Transform existing marketing copy into
    a different tone and platform style.
    """

    prompt = build_tone_transform_prompt(
        original_text=original_text,
        target_tone=target_tone,
        platform=platform,
        audience=audience,
        brand_voice=brand_voice,
        copy_length=copy_length
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temperature,
            "top_p": top_p
        }
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text.strip()
