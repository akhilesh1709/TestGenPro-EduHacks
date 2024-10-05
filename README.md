# Question Generator

This project is a Streamlit-based application that generates different types of questions (Multiple Choice, True/False, and Descriptive) from a text document. It uses the OpenAI API to generate questions based on the content of uploaded PDF or text files, and allows users to specify the number of questions, the subject, and the complexity level.

## Features

- **Multiple Choice Questions**: Generates MCQs with specified complexity and tone.
- **True/False Questions**: Generates True/False questions.
- **Descriptive Questions**: Generates descriptive questions that are more detailed and require explanation.
- **File Upload**: Supports uploading of PDF and text files to extract content for question generation.
- **Customization**: Users can specify the number of questions, subject, and tone of the generated questions.

## Setup

### Prerequisites

- Python 3.7 or later
- Streamlit
- OpenAI API Key
- Required Python packages listed in `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/question-generator.git
   cd question-generator
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```plaintext
   OPENAI_API_KEY=your-openai-api-key
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload File**: Upload a PDF or text file containing the content from which you want to generate questions.
2. **Select Question Type**: Choose from "Multiple Choice", "True/False", or "Descriptive".
3. **Input Details**: Specify the number of questions, subject, and tone (complexity level) of the questions.
4. **Generate Questions**: Click the "Generate Questions" button to start the process. The app will display the generated questions in the selected format.
