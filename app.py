import streamlit as st
import pytesseract
from PIL import Image, ImageOps

st.set_page_config(page_title="Image to Text", page_icon="📝")

st.title("📝 Image to Text")
st.write("Upload an image to extract English text.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    try:
        image = ImageOps.exif_transpose(
            Image.open(uploaded_file)
        ).convert("RGB")
    except Exception:
        st.error("Unable to open this image. Please try another.")
        st.stop()

    st.image(image, caption="Uploaded image")

    # Clear the previous result when a different image is uploaded.
    image_bytes = uploaded_file.getvalue()

    if st.session_state.get("image_bytes") != image_bytes:
        st.session_state.image_bytes = image_bytes
        st.session_state.pop("extracted_text", None)

    if st.button("Extract text"):
        st.session_state.pop("extracted_text", None)

        try:
            with st.spinner("Extracting text..."):
                text = pytesseract.image_to_string(
                    image,
                    lang="eng",
                    timeout=30
                )
                st.session_state.extracted_text = text.strip()

        except pytesseract.TesseractNotFoundError:
            st.error(
                "Tesseract is not installed. "
                "Include packages.txt when deploying."
            )
        except RuntimeError:
            st.error("Extraction timed out. Try a smaller image.")
        except pytesseract.TesseractError:
            st.error("Could not extract text. Try a clearer image.")

    text = st.session_state.get("extracted_text")

    if text:
        st.text_area("Extracted text", text, height=300)

        st.download_button(
            label="Download text",
            data=text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
    elif text == "":
        st.warning("No text detected. Try a clearer image.")
        