import os
import pandas as pd
import configparser
import fitz  # PyMuPDF for handling PDF files
import docx  # python-docx for handling DOCX files
from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_document(file_path):
    """Extract text from a document file (PDF or DOCX)."""
    text = ""
    if file_path.endswith('.pdf'):
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def generate_summary(file_path):
    """Generate a summary for the given document."""
    # Extract text from the document
    document_text = extract_text_from_document(file_path)

    # Truncate the text if it's too long
    if len(document_text) > 1000:
        document_text = document_text[:1000] + "..."

    # Prepare the conversation prompt for the API
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please summarize this document: \n\n{document_text}"}
    ]

    # Call the OpenAI Chat Completions API for a summary
    response = client.chat.completions.create(model="gpt-4", messages=conversation)

    # Extract the summary from the response
    summary = response.choices[0].message.content if response.choices else "Summary not available."
    return summary

def create_csv_from_directory(directory, csv_file):
    """Create a CSV file with file names from the specified directory."""
    file_list = [{'file': f} for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and (f.endswith('.pdf') or f.endswith('.docx'))]
    df = pd.DataFrame(file_list)
    df['summary'] = None
    df.to_csv(csv_file, index=False)
    print(f"Created CSV file {csv_file} with file names from {directory}")

def main():
    # Read configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Retrieve directives directory and CSV file name from the configuration
    directives_dir = config['Settings']['directives_dir']
    csv_file_name = config['Settings']['csv_file_name']
    csv_file_path = os.path.join(directives_dir, csv_file_name)

    # Check if CSV file exists, if not, create it from the directory
    if not os.path.exists(csv_file_path):
        create_csv_from_directory(directives_dir, csv_file_path)

    # Load the CSV file containing the file names
    df = pd.read_csv(csv_file_path)

    # Process each file without a summary
    for index, row in df[df['summary'].isna()].iterrows():
        file_path = os.path.join(directives_dir, row['file'])
        if os.path.exists(file_path):
            summary = generate_summary(file_path)
            df.at[index, 'summary'] = summary
        else:
            print(f"File not found: {file_path}")

    # Save the updated CSV file with summaries
    df.to_csv(csv_file_path, index=False)
    print("CSV file updated with summaries.")

if __name__ == "__main__":
    main()
