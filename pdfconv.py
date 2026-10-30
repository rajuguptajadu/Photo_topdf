import io
import img2pdf
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Photo to PDF Converter", page_icon="📄")

st.title("Convert Photos to PDF")
st.write("Upload one or more images (JPG, JPEG, PNG) to merge them into a single PDF.")

# File uploader widget
uploaded_files = st.file_uploader(
    "Choose images", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if uploaded_files:
  st.subheader("Uploaded Preview")
  images_bytes_list = []

  # Process each uploaded image
  for uploaded_file in uploaded_files:
    # Open image using PIL
    image = Image.open(uploaded_file)

    # Display image in Streamlit
    st.image(image, caption=uploaded_file.name, use_container_width=True)

    # Convert PIL image to RGB if it has an alpha channel (PNG transparency)
    if image.mode in ("RGBA", "P"):
      image = image.convert("RGB")

    # Save PIL image to an in-memory byte buffer as JPEG
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    images_bytes_list.append(img_byte_arr.getvalue())

  # Convert the list of image bytes to a PDF using img2pdf
  if st.button("Generate PDF"):
    pdf_bytes = img2pdf.convert(images_bytes_list)

    st.success("PDF generated successfully!")

    # Provide a download button for the generated PDF
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name="converted_photos.pdf",
        mime="application/pdf",
    )
    # --- Footer Design ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #888888;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-weight: 500;
        z-index: 100;
    }
    </style>
    <div class="footer">
        <p>Design and Developed by <b>RK Gupta</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)
