import streamlit as st

from copywriter import generate_copy, transform_copy


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Copywriter & Tone Transformer",
    page_icon="✨",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []


if "generated_results" not in st.session_state:
    st.session_state.generated_results = []


# ============================================================
# HEADER
# ============================================================

st.title("✨ AI Copywriter & Tone Transformer")

st.markdown(
    """
    **Generate, transform and optimize marketing copy with Gemini AI.**

    Create platform-specific content or transform existing copy
    into a new tone while controlling Gemini's generation behavior.
    """
)

st.divider()


# ============================================================
# MODE SELECTION
# ============================================================

st.subheader("🚀 Choose Your Mode")

mode = st.radio(
    "What would you like to do?",
    [
        "✨ Create New Copy",
        "🔄 Transform Existing Copy"
    ],
    horizontal=True
)

st.divider()


# ============================================================
# SIDEBAR — AI CONTROLS
# ============================================================

with st.sidebar:

    st.header("🧠 Gemini Controls")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help=(
            "Lower values produce more predictable output. "
            "Higher values increase creative variation."
        )
    )

    top_p = st.slider(
        "Top_P",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.05,
        help="Controls the range of tokens considered during generation."
    )

    st.divider()

    st.subheader("🎛️ Creativity Presets")

    preset = st.selectbox(
        "Choose a preset",
        [
            "Custom",
            "Conservative",
            "Balanced",
            "Creative",
            "Highly Creative"
        ]
    )

    if preset == "Conservative":
        temperature = 0.3
        top_p = 0.7

    elif preset == "Balanced":
        temperature = 0.7
        top_p = 0.9

    elif preset == "Creative":
        temperature = 0.9
        top_p = 0.95

    elif preset == "Highly Creative":
        temperature = 1.0
        top_p = 1.0

    st.caption(
        f"Temperature: {temperature:.2f} | Top_P: {top_p:.2f}"
    )

    st.divider()

    st.subheader("🔧 Developer Mode")

    developer_mode = st.checkbox(
        "Show generation parameters"
    )


# ============================================================
# CREATE NEW COPY MODE
# ============================================================

if mode == "✨ Create New Copy":

    st.subheader("📝 Product Information")

    product_name = st.text_input(
        "Product Name",
        placeholder="Example: SmartStudy AI"
    )

    product_description = st.text_area(
        "Product Description",
        placeholder=(
            "Describe your product, its purpose, "
            "features and benefits..."
        ),
        height=160
    )

    st.subheader("🎯 Marketing Configuration")

    col1, col2, col3 = st.columns(3)

    with col1:

        platform = st.selectbox(
            "Platform",
            [
                "LinkedIn",
                "Instagram",
                "Email"
            ]
        )

    with col2:

        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Friendly",
                "Casual",
                "Formal",
                "Persuasive",
                "Excited",
                "Humorous",
                "Empathetic"
            ]
        )

    with col3:

        audience = st.selectbox(
            "Target Audience",
            [
                "General Audience",
                "Students",
                "Professionals",
                "Developers",
                "Business Owners",
                "Customers"
            ]
        )

    col4, col5 = st.columns(2)

    with col4:

        brand_voice = st.selectbox(
            "Brand Voice",
            [
                "Modern",
                "Professional",
                "Premium",
                "Bold",
                "Trustworthy",
                "Playful",
                "Minimal"
            ]
        )

    with col5:

        copy_length = st.selectbox(
            "Copy Length",
            [
                "Short",
                "Medium",
                "Long"
            ]
        )

    st.divider()

    st.subheader("📊 Generation Options")

    number_of_variations = st.slider(
        "Number of Variations",
        min_value=1,
        max_value=3,
        value=3
    )

    character_limit_enabled = st.checkbox(
        "Enable Character Limit"
    )

    character_limit = None

    if character_limit_enabled:

        character_limit = st.number_input(
            "Maximum Characters",
            min_value=50,
            max_value=5000,
            value=300,
            step=50
        )

    generate_button = st.button(
        "✨ Generate Marketing Copy",
        type="primary",
        use_container_width=True
    )

    # ========================================================
    # GENERATION
    # ========================================================

    if generate_button:

        if not product_name.strip():

            st.warning("Please enter a product name.")

        elif not product_description.strip():

            st.warning("Please enter a product description.")

        else:

            st.session_state.generated_results = []

            progress = st.progress(0)

            try:

                for i in range(number_of_variations):

                    result = generate_copy(
                        product_name=product_name,
                        product_description=product_description,
                        platform=platform,
                        tone=tone,
                        audience=audience,
                        brand_voice=brand_voice,
                        copy_length=copy_length,
                        temperature=temperature,
                        top_p=top_p,
                        variation_number=i + 1
                    )

                    st.session_state.generated_results.append(
                        result
                    )

                    progress.progress(
                        int(((i + 1) / number_of_variations) * 100)
                    )

                st.success(
                    "Marketing copy generated successfully!"
                )

                # Save history
                st.session_state.history.append({
                    "Mode": "Create",
                    "Product": product_name,
                    "Platform": platform,
                    "Tone": tone,
                    "Result": st.session_state.generated_results[0]
                })

            except Exception as e:

                st.error(
                    f"An error occurred while generating copy: {e}"
                )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    if st.session_state.generated_results:

        st.divider()

        st.subheader("📄 Generated Marketing Copy")

        for index, result in enumerate(
            st.session_state.generated_results
        ):

            with st.expander(
                f"✨ Variation {index + 1}",
                expanded=(index == 0)
            ):

                # Character analysis
                character_count = len(result)
                word_count = len(result.split())

                if (
                    character_limit_enabled
                    and character_limit is not None
                    and character_count > character_limit
                ):

                    st.warning(
                        f"⚠️ {character_count} characters — "
                        f"exceeds your {character_limit} character limit."
                    )

                else:

                    st.success(
                        f"Character count: {character_count} | "
                        f"Words: {word_count}"
                    )

                st.write(result)

                st.download_button(
                    label="📥 Download This Copy",
                    data=result,
                    file_name=f"marketing_copy_{index + 1}.txt",
                    mime="text/plain",
                    key=f"download_create_{index}"
                )

        # ====================================================
        # COPY ANALYTICS
        # ====================================================

        st.divider()

        st.subheader("📊 Copy Analytics")

        best_result = st.session_state.generated_results[0]

        characters = len(best_result)
        words = len(best_result.split())
        sentences = max(
            1,
            best_result.count(".")
            + best_result.count("!")
            + best_result.count("?")
        )

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Characters",
            characters
        )

        metric2.metric(
            "Words",
            words
        )

        metric3.metric(
            "Sentences",
            sentences
        )

        # ====================================================
        # DEVELOPER INFORMATION
        # ====================================================

        if developer_mode:

            st.divider()

            st.subheader("🔧 Developer Information")

            st.write(
                f"**Model:** Gemini"
            )

            st.write(
                f"**Temperature:** {temperature}"
            )

            st.write(
                f"**Top_P:** {top_p}"
            )

            st.write(
                f"**Platform:** {platform}"
            )

            st.write(
                f"**Tone:** {tone}"
            )

            st.write(
                f"**Audience:** {audience}"
            )

            st.write(
                f"**Brand Voice:** {brand_voice}"
            )


# ============================================================
# TRANSFORM EXISTING COPY MODE
# ============================================================

else:

    st.subheader("🔄 Tone Transformer")

    st.markdown(
        "Paste existing marketing copy and transform it into "
        "a new tone and platform style."
    )

    original_text = st.text_area(
        "Existing Copy",
        placeholder=(
            "Paste your existing marketing copy here..."
        ),
        height=220
    )

    col1, col2 = st.columns(2)

    with col1:

        target_tone = st.selectbox(
            "Target Tone",
            [
                "Professional",
                "Friendly",
                "Casual",
                "Formal",
                "Persuasive",
                "Excited",
                "Humorous",
                "Empathetic"
            ],
            key="transform_tone"
        )

    with col2:

        transform_platform = st.selectbox(
            "Target Platform",
            [
                "LinkedIn",
                "Instagram",
                "Email"
            ],
            key="transform_platform"
        )

    col3, col4 = st.columns(2)

    with col3:

        transform_audience = st.selectbox(
            "Target Audience",
            [
                "General Audience",
                "Students",
                "Professionals",
                "Developers",
                "Business Owners",
                "Customers"
            ],
            key="transform_audience"
        )

    with col4:

        transform_voice = st.selectbox(
            "Brand Voice",
            [
                "Modern",
                "Professional",
                "Premium",
                "Bold",
                "Trustworthy",
                "Playful",
                "Minimal"
            ],
            key="transform_voice"
        )

    transform_length = st.selectbox(
        "Output Length",
        [
            "Short",
            "Medium",
            "Long"
        ],
        key="transform_length"
    )

    transform_button = st.button(
        "🔄 Transform Copy",
        type="primary",
        use_container_width=True
    )

    if transform_button:

        if not original_text.strip():

            st.warning(
                "Please enter existing copy to transform."
            )

        else:

            with st.spinner(
                "Transforming your copy..."
            ):

                try:

                    transformed = transform_copy(
                        original_text=original_text,
                        target_tone=target_tone,
                        platform=transform_platform,
                        audience=transform_audience,
                        brand_voice=transform_voice,
                        copy_length=transform_length,
                        temperature=temperature,
                        top_p=top_p
                    )

                    st.success(
                        "Copy transformed successfully!"
                    )

                    st.subheader("✨ Transformed Copy")

                    st.write(transformed)

                    character_count = len(transformed)
                    word_count = len(transformed.split())

                    c1, c2 = st.columns(2)

                    c1.metric(
                        "Characters",
                        character_count
                    )

                    c2.metric(
                        "Words",
                        word_count
                    )

                    st.download_button(
                        label="📥 Download Transformed Copy",
                        data=transformed,
                        file_name="transformed_copy.txt",
                        mime="text/plain",
                        key="download_transformed"
                    )

                    # Save history
                    st.session_state.history.append({
                        "Mode": "Transform",
                        "Product": "Existing Copy",
                        "Platform": transform_platform,
                        "Tone": target_tone,
                        "Result": transformed
                    })

                except Exception as e:

                    st.error(
                        f"An error occurred while transforming copy: {e}"
                    )


# ============================================================
# GENERATION HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("📜 Generation History")

    for index, item in enumerate(
        reversed(st.session_state.history)
    ):

        with st.expander(
            f"{index + 1}. {item['Mode']} — "
            f"{item['Platform']} — {item['Tone']}"
        ):

            st.write(
                f"**Mode:** {item['Mode']}"
            )

            st.write(
                f"**Platform:** {item['Platform']}"
            )

            st.write(
                f"**Tone:** {item['Tone']}"
            )

            st.write(item["Result"])