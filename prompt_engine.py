PLATFORM_INSTRUCTIONS = {
    "LinkedIn": """
Create professional LinkedIn content.
Use a business-friendly and informative style.
Focus on value, credibility, and professional engagement.
Avoid excessive emojis.
End with a suitable professional call-to-action.
""",

    "Instagram": """
Create engaging Instagram content.
Keep the opening attention-grabbing.
Use concise paragraphs and natural social-media language.
Use emojis where appropriate.
Include relevant hashtags at the end.
End with an engaging call-to-action.
""",

    "Email": """
Create marketing email content.
Include a compelling subject line.
Create a clear and persuasive email body.
Maintain a professional but engaging style.
End with a clear call-to-action.
"""
}


def build_copywriting_prompt(
    product_name,
    product_description,
    platform,
    tone,
    audience="General Audience",
    brand_voice="Modern",
    copy_length="Medium",
    variation_number=None
):
    """Build a dynamic prompt for new marketing copy."""

    platform_rules = PLATFORM_INSTRUCTIONS.get(
        platform,
        "Create suitable marketing content for the selected platform."
    )

    length_rules = {
        "Short": "Keep the copy concise and impactful.",
        "Medium": "Create a balanced copy with useful detail.",
        "Long": "Create detailed and persuasive marketing copy."
    }

    variation_instruction = ""

    if variation_number:
        variation_instruction = f"""
This is variation {variation_number}.
Make this version meaningfully different in wording,
opening, structure, and persuasive approach from other variations.
"""

    prompt = f"""
You are an expert marketing copywriter.

Your task is to create high-quality marketing content.

================ PRODUCT =================

Product Name:
{product_name}

Product Description:
{product_description}

================ AUDIENCE =================

Target Audience:
{audience}

Brand Voice:
{brand_voice}

================ CONTENT SETTINGS =================

Platform:
{platform}

Tone:
{tone}

Length:
{copy_length}

================ PLATFORM GUIDELINES =================

{platform_rules}

================ INSTRUCTIONS =================

1. Clearly communicate the product's value.
2. Match the requested tone consistently.
3. Match the selected brand voice.
4. Write specifically for the target audience.
5. Optimize the content for the selected platform.
6. Do not invent product features, statistics, claims,
   certifications, or benefits that were not provided.
7. Avoid repetitive wording.
8. Make the content natural and engaging.
9. Follow the requested length.
10. Include an appropriate call-to-action when suitable.

{length_rules.get(copy_length, length_rules["Medium"])}

{variation_instruction}

Return only the final marketing copy.
Do not explain your reasoning.
"""

    return prompt.strip()


def build_tone_transform_prompt(
    original_text,
    target_tone,
    platform,
    audience="General Audience",
    brand_voice="Modern",
    copy_length="Medium"
):
    """Build a dynamic prompt for transforming existing copy."""

    platform_rules = PLATFORM_INSTRUCTIONS.get(
        platform,
        "Adapt the content appropriately for the selected platform."
    )

    prompt = f"""
You are an expert marketing editor and copywriting specialist.

Transform the existing marketing copy below.

================ ORIGINAL COPY =================

{original_text}

================ TRANSFORMATION SETTINGS =================

Target Platform:
{platform}

Target Tone:
{target_tone}

Target Audience:
{audience}

Brand Voice:
{brand_voice}

Copy Length:
{copy_length}

================ PLATFORM GUIDELINES =================

{platform_rules}

================ INSTRUCTIONS =================

1. Preserve the original meaning and factual information.
2. Transform the tone to match: {target_tone}.
3. Optimize the content for {platform}.
4. Make the wording natural and engaging.
5. Do not invent new product claims or features.
6. Improve clarity and readability.
7. Remove unnecessary repetition.
8. Follow the requested length.
9. Add a suitable call-to-action when appropriate.

Return only the transformed marketing copy.
Do not explain your reasoning.
"""

    return prompt.strip()