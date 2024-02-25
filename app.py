import streamlit as st
import requests
from dotenv import load_dotenv
import os
import base64

# Load environment variables from .env file
load_dotenv()

# Access the loaded environment variables
api_key = os.getenv('Api_Key')


# Function to extract text from an image using OCR.space API
def extract_text(image):
    try:
        # OCR.space API endpoint
        api_url = 'https://api.ocr.space/parse/image'

        # Determine file type based on the image file extension
        file_extension = os.path.splitext(image.name)[1].lower()
        valid_filetypes = ['jpg', 'jpeg', 'png']

        if file_extension[1:] in valid_filetypes:
            # API parameters
            params = {
                'apikey': api_key,
                'filetype': file_extension[1:],  # Use the file extension as the file type
            }

            # Convert the image to bytes
            image_bytes = image.read()

            # Make the API request
            response = requests.post(api_url, files={'file': image_bytes}, data=params)

            # Parse the JSON response
            result = response.json()

            # Check if 'ParsedResults' is in the response
            if 'ParsedResults' in result:
                return result['ParsedResults'][0]['ParsedText']
            else:
                return 'Error in OCR.space API response'
        else:
            return 'Unsupported file type'
    except Exception as e:
        return str(e)


# Main function
def main():
    st.title("📸 Image Text Magician ✨ by Muneeb Wali Khan 🚀")

    # Create an "Instructions" section
    st.markdown("## ℹ️ Instructions")
    st.write(
        """
        Welcome to the Image Text Magician app! 🌟
        
        Follow these steps:
        
        1. Upload an image by clicking on the 'Choose an image' image must be 1 MB or less.
        2. Click on 'Extract Text' to perform text extraction.
        3. The extracted text will be displayed below the button.
        4. If desired, you can save the extracted text to a file using the 'Save Text to File' button.

        Enjoy the magic! ✨
        """
    )

    # File upload
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", width=800)


        # Extract text on button click
        if st.button("Extract Text"):
            # Inform user that text extraction is in progress
            with st.spinner("Extracting text... This may take a moment. ✨"):
                # Extract text using OCR.space API
                extracted_text = extract_text(uploaded_file)

            # Display the extracted text
            st.subheader("Extracted Text:")
            st.text(extracted_text)

            # Save the extracted text to a file
                    # Provide a download button for the user

            download_button = st.download_button(
                label="Download Text File",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime=f"text/plain"
            )
            if download_button:
                try:
                    with open("extracted_text.txt", "w", encoding="utf-8") as file:
                        file.write(extracted_text)
                    st.success("Text saved to 'extracted_text.txt'.")

                except Exception as e:
                    st.error(f"An error occurred while saving the file: {str(e)}")


if __name__ == "__main__":
    main()
