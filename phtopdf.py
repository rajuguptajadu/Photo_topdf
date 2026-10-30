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
    st.subheader("Uploaded Preview & Adjustments")
    images_bytes_list = []

    # Process each uploaded image
    for index, uploaded_file in enumerate(uploaded_files):
        # Open image using PIL
        image = Image.open(uploaded_file)
        
        # Unique key identifier for widget instances
        unique_key = f"rotate_{index}_{uploaded_file.name}"
        
        # Add rotation option per individual image
        rotation_angle = st.radio(
            f"Rotate {uploaded_file.name}:",
            options=[0, 90, 180, 270],
            format_func=lambda x: f"{x}°",
            horizontal=True,
            key=unique_key
        )
        
        # Apply the chosen rotation angle if needed
        if rotation_angle != 0:
            # expand=True prevents corners from getting cut off during rotation
            image = image.rotate(-rotation_angle, expand=True)

        # Display updated live preview in Streamlit
        st.image(image, caption=f"{uploaded_file.name} (Rotated {rotation_angle}°)", use_container_width=True)

        # Convert PIL image to RGB if it has an alpha channel (PNG transparency)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Save adjusted PIL image to an in-memory byte buffer as JPEG
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        images_bytes_list.append(img_byte_arr.getvalue())

    # Convert the list of final image bytes to a PDF using img2pdf
    st.write("---")
    if st.button("Generate PDF", type="primary"):
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
