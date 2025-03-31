import os

import easyocr
import fitz  # PyMuPDF
import PyPDF2
from google import genai
from langchain.text_splitter import RecursiveCharacterTextSplitter


def doc_loader(filepath):
    """Loads a document and extracts text from it.
    Args:
        filepath (str): Path to the document.
    Returns:
        str: Extracted text from the document.
    """
    dtype = filepath.split(".")[-1]  # extracting the file type
    if dtype.lower() == "pdf":
        reader = PyPDF2.PdfReader(filepath)  # reading the pdf file
        pages = len(reader.pages)
        text = ""
        for i in range(pages):
            text = (
                text + " " + reader.pages[i].extract_text()
            )  # extracting the text from the pdf
        # in case no extracted text through pypdf, use OCR
        if len(text.replace(" ", "")) == 0:
            pdf_file = fitz.open(filepath)
            text = ""
            for i in range(len(pdf_file)):
                print("entering")
                page = pdf_file[i]
                pix = page.get_pixmap()
                pix.save("temp.png")
                # Create an OCR reader object
                reader = easyocr.Reader(["en"])
                # Read text from an image
                result = reader.readtext("temp.png")
                # Print the extracted text
                for detection in result:
                    text = text + " " + detection[1]

    return text


def chunk_text(text, chunk_size=1800, chunk_overlap=0):
    """
    Splits the text into chunks of specified size with a defined overlap.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return chunks


def extract_information_from_chunk(chunk, google_API_version):
    """
    Extracts information from a chunk of text using an LLM.
    """
    try:
        client = genai.Client(api_key=str(google_API_version))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""Analyze the following PDF and extract the most relevant information
            related to the discussed theme. Focus on key details such as landscapes, important
            dates, and any significant contextual elements. Present the extracted information
            in a structured format using bullet points (•) for clarity. Ensure that only the
            most relevant and accurate details are included.

            The provided text chunks are:
            {chunk}""",
        )
        return response.text
    except Exception as error:
        print(f"The error {error} is happening.")
        return None


def result_llm_OCR(pdfs_, result_pdfs_, google_API_version_):
    """Application to extract information from PDF files using LLM and OCR.
    Args:"""
    if not os.path.exists(result_pdfs_):
        os.makedirs(result_pdfs_)

    for file in os.listdir(pdfs_):
        if file.endswith(".pdf"):
            pdf_file = os.path.join(pdfs_, file)
            text_extracted = doc_loader(pdf_file)
            chunks = chunk_text(text=text_extracted, chunk_size=1800, chunk_overlap=0)
            extracted_information = []
            min_ = 100000
            for chunk in chunks:
                info = extract_information_from_chunk(chunk, google_API_version_)
                if info:
                    extracted_information.append(info)
                    if len(info) < min_:
                        min_ = len(info)
            extracted_information = [
                info for info in extracted_information if len(info) != min_
            ]
            if extracted_information:
                combined_results = "\n".join(extracted_information)
                results_llm_OCR_app_path = os.path.join(
                    result_pdfs_, f"{file[:-4]}_llm.json"
                )
                with open(results_llm_OCR_app_path, "w") as f:
                    f.write(combined_results)
                    print(f"Saved '{results_llm_OCR_app_path}'.")
