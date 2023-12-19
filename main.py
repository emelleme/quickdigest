import os
import pandas as pd
import configparser
import fitz  # PyMuPDF
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def generate_summary(pdf_path):
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Truncate the text if it's too long
    if len(pdf_text) > 1000:
        pdf_text = pdf_text[:1000] + "..."

    # Prepare the conversation prompt for the API
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please summarize this document: \n\n{pdf_text}"}
    ]

    # Call the OpenAI Chat Completions API for a summary
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=conversation)

    # Extract the summary from the response
    summary = response.choices[0].message.content if response.choices else "Summary not available."
    return summary

def create_csv_from_directory(directory, csv_file):
    """Create a CSV file with file names from the specified directory."""
    file_list = [{'file': f} for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    df = pd.DataFrame(file_list)
    df['summary'] = None
    df.to_csv(csv_file, index=False)
    print(f"Created CSV file {csv_file} with file names from {directory}")

def main():
    # Read config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get directives directory and CSV file name from config
    directives_dir = config['Settings']['directives_dir']
    csv_file_name = config['Settings']['csv_file_name']
    csv_file_path = os.path.join(directives_dir, csv_file_name)

    # Check if CSV file exists, if not, create from directory
    if not os.path.exists(csv_file_path):
        create_csv_from_directory(directives_dir, csv_file_path)

    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Process each directive without a summary
    for index, row in df[df['summary'].isna()].iterrows():
        pdf_file = os.path.join(directives_dir, row['file'])
        if os.path.exists(pdf_file):
            summary = generate_summary(pdf_file)
            df.at[index, 'summary'] = summary
        else:
            print(f"File not found: {pdf_file}")

    # Save the updated CSV file
    df.to_csv(csv_file_path, index=False)
    print("CSV file updated with summaries.")

if __name__ == "__main__":
    main()
