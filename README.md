# TestGenPro: AI-Powered Learning and Assessment Tool

TestGenPro is an advanced AI-based tool that helps users create assessments, generate study notes, and even convert content into audio podcasts. The app offers multiple features, including automatic generation of multiple-choice, true/false, and descriptive questions, performance tracking, and quiz review functionalities. It is built using Python, Streamlit, and OpenAI's GPT models for text generation.

### Team Name: The Qubits

### Team Members:

1. Akhilesh T S
2. Karthik Sriram V
3. Abhishek Prasanna

### Institute Name: SASTRA University

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [File Structure](#file-structure)
5. [Environment Variables](#environment-variables)
6. [Dependencies](#dependencies)
7. [User Authentication](#user-authentication)
8. [Tabs and Functionalities](#tabs-and-functionalities)
9. [Logging](#logging)
10. [Error Handling](#error-handling)

---

## Features

- **AI-Powered Question Generation**: Automatically generate multiple-choice, true/false, and descriptive questions from uploaded files.
- **Take Assessments**: Users can attempt the generated questions and receive real-time feedback on their performance.
- **Quiz Review**: Users can review the generated quizzes and export them as a PDF file.
- **Performance Tracking**: Users can track their performance over multiple assessments.
- **Generate Study Notes**: Generate concise study notes from text-based files (PDF or TXT).
- **Generate Podcast**: Convert text content into a podcast-like audio format (MP3).
- **User Authentication**: Secure login and user session management using bcrypt hashing.

---

## Installation

Follow these steps to install and run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/testgenpro.git
cd testgenpro
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

Create a `.env` file in the project root directory and add the following environment variables:

```env
OPENAI_API_KEY=<your_openai_api_key>
```

### 5. Run the Application

```bash
streamlit run app.py
```

---

## Usage

Once the application is running, open the URL provided in the terminal (`http://localhost:8501` by default) in a browser. 

You will be greeted by the login page. After authenticating, you will be able to access the various features of TestGenPro, as explained below.

---

## File Structure

```
testgenpro/
│
├── app.py                  # Main Streamlit application file
├── requirements.txt         # List of project dependencies
├── .env                     # Environment variables
├── src/                     # Source folder containing utility scripts
│   ├── mcqgenerator/
│   │   ├── MCQgenerator.py  # Question generation script
│   │   ├── utils.py         # File reading and parsing utilities
│   │   ├── logger.py        # Logging utilities
│   │   └── __init__.py      # Initialization for MCQ generator
│   └── __init__.py          # Initialization for src
├── response_mcqs.json       # JSON template for MCQ generation
├── response_true_false.json # JSON template for True/False questions
├── response_descriptive.json # JSON template for Descriptive questions
└── README.md                # Documentation
```

---

## Environment Variables

The following environment variables need to be set in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key is required for generating text-based questions, notes, and podcasts.

---

## Dependencies

The application uses several Python libraries. You can install all dependencies using the provided `requirements.txt` file.

Key dependencies:
- `streamlit`: Frontend framework to create the user interface.
- `openai`: Used to access GPT models for text and speech generation.
- `bcrypt`: For hashing user passwords securely.
- `fpdf`: To export the generated quizzes as PDF files.
- `base64`: For encoding PDF files for download.
- `dotenv`: To manage environment variables.
- `langchain`: To create and manage the GPT-3/4 prompts and models.
- `traceback`: For debugging and error handling.

---

## User Authentication

TestGenPro includes basic authentication functionality. User credentials (username and password) are stored in a dictionary with bcrypt hashing for secure password management.

- **Login**: The user must enter a valid username and password to access the application.
- **Logout**: Users can log out via a button in the sidebar, which will terminate the session.

For demonstration purposes, a couple of user accounts are hardcoded into the application:

- `user1` / `password1`
- `user2` / `password2`

You can modify the `users` dictionary to add more users if needed.

---

## Tabs and Functionalities

Once logged in, the app displays a navigation bar with the following tabs:

### 1. **Generate Questions**

- **Upload File**: Upload a PDF or TXT file.
- **Select Question Type**: Choose between Multiple Choice, True/False, or Descriptive questions.
- **Question Generation**: Generates questions using OpenAI GPT and JSON templates.
- **Error Handling**: In case of errors, detailed messages are logged and displayed to the user.

### 2. **Take Assessment**

- **Answer Questions**: Users can attempt the generated questions and receive feedback on submission.
- **Results**: Correct answers and scores are displayed after submitting the assessment.
- **Feedback**: Detailed feedback is provided for each question.

### 3. **Review Quiz**

- **Review**: Allows users to view the generated quiz and correct answers.
- **Export as PDF**: Users can export the quiz as a PDF document.

### 4. **Performance Tracking**

- **Track Progress**: Users can view their past assessment scores in a line chart.
- **Average Score**: The average score across all assessments is displayed.

### 5. **Generate Notes**

- **Quick Notes**: Upload a text or PDF file to generate concise notes for study preparation.
- **Note Generation**: Utilizes OpenAI's GPT model to summarize the content and display it on the page.

### 6. **Generate Podcast**

- **Audio File**: Converts uploaded text into a podcast-like audio file.
- **Text-to-Speech (TTS)**: Generates speech from the summarized content and saves it as an MP3 file.
- **Download**: Users can download and listen to the generated podcast.

---

## Logging

TestGenPro uses a logging utility (`src/mcqgenerator/logger.py`) to log important events and errors. These logs help in debugging and tracking performance. Key details such as API token usage, generated tokens, and total cost for OpenAI API calls are logged.

---

## Error Handling

All functionalities in TestGenPro include comprehensive error handling. If any exception occurs (e.g., API failure, file parsing issues), an appropriate error message is logged, and the user is notified with a detailed error message.
