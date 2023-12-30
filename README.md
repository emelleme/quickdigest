
# QuickDigest

## Overview

QuickDigest is a Python-based tool designed to automate the summarization of documents into a concise format, ideal for large language models (LLMs) in their information retrieval pipelines. This application scans a specified directory of documents (including both PDF and `.docx` files), generates summaries for each using OpenAI's GPT model, and compiles these into a CSV file.

## Features

-   Automated document summarization for PDF and `.docx` files.
-   Compilation of summaries in a CSV file for easy access.
-   Configurable directory and output file settings.
-   User-friendly and efficient for batch processing of documents.

## Prerequisites

-   Python 3.x
-   Pip (Python package installer)

## Installation

1.  Clone or download the QuickDigest repository to your local machine.
    
2.  Navigate to the QuickDigest folder in your terminal or command prompt.
    
3.  Install the necessary dependencies by running:
    
    Copy code
    
    `pip install -r requirements.txt` 
    
4.  Ensure you have set your OpenAI API key in your environment variables.
    

## Configuration

Edit the `config.ini` file in the QuickDigest directory to specify:

-   `directives_dir`: Directory containing the documents to be summarized.
-   `csv_file_name`: Name of the CSV file to be generated.

## Usage

1.  Place your documents (PDF and `.docx`) in the specified directory.
    
2.  Run the application using:
    
    cssCopy code
    
    `python main.py` 
    
3.  The application will create a CSV file in the specified directory, containing summaries of each document.
    

## .gitignore File

The `.gitignore` file is preconfigured to ignore common Python and development environment files. Modify it as needed to suit your project requirements.

## Contributing

Contributions to QuickDigest are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

QuickDigest is released under the MIT License.
