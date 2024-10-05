import os
import json
import traceback
import bcrypt
from dotenv import load_dotenv
from openai import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
import streamlit as st
from src.mcqgenerator.utils import read_file, get_document_data
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
from fpdf import FPDF
import base64

# Load environment variables
load_dotenv()

# Load JSON templates
with open('response_mcqs.json', 'r') as file:
    MCQ_RESPONSE_JSON = json.load(file)

with open('response_true_false.json', 'r') as file:
    TRUEFALSE_RESPONSE_JSON = json.load(file)

with open('response_descriptive.json', 'r') as file:
    DESCRIPTIVE_RESPONSE_JSON = json.load(file)

# Initialize session state
if 'generated_quiz' not in st.session_state:
    st.session_state['generated_quiz'] = None
    st.session_state['question_type'] = None
if 'user_performance' not in st.session_state:
    st.session_state['user_performance'] = []
if 'generated_notes' not in st.session_state:
    st.session_state['generated_notes'] = None
if 'generated_summary' not in st.session_state:
    st.session_state['generated_summary'] = None
if 'audio_file_path' not in st.session_state:
    st.session_state['audio_file_path'] = None
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Dictionary to store user credentials (username: hashed_password)
users = {
    "user1": bcrypt.hashpw("password1".encode('utf-8'), bcrypt.gensalt()),
    "user2": bcrypt.hashpw("password2".encode('utf-8'), bcrypt.gensalt())
}

# Function to authenticate user
def authenticate_user(username, password):
    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]):
        st.session_state['user'] = username
        st.success(f"Logged in as {username}")
        return True
    else:
        st.error("Invalid username or password")
        return False

# Function to create user (for demonstration purposes, no signup in this example)
def create_user(username, password):
    if username in users:
        st.error("Username already exists")
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password
    st.success(f"Account created successfully for {username}")
    return True

st.title("TestGenPro: AI-Powered Learning and Assessment Tool")

# Authentication
if not st.session_state['user']:
    st.sidebar.title("User Authentication")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        authenticate_user(username, password)

    st.stop()  # Stop the app if not authenticated
else:
    st.sidebar.success(f"Logged in as {st.session_state['user']}")
    if st.sidebar.button("Logout"):
        st.session_state['user'] = None
        st.experimental_rerun()  # Refresh the app

    # Display a greeting message to the authenticated user
    st.write(f"""
        Hello, {st.session_state['user']}👋  
        Welcome to **TestGenPro** — your AI-powered learning and assessment tool!  
        This platform allows you to effortlessly generate quizzes, track your performance, create study notes, and even convert content into engaging audio podcasts. Choose from various interactive features and start exploring today! 🚀
    """)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Generate Questions", "Take Assessment", "Review Quiz", "Performance Tracking", "Generate Notes", "Generate Podcast"])

### Generate Questions Tab ###
with tab1:
    st.header("Generate Questions")
    question_type = st.radio("Select question type:", ["Multiple Choice", "True/False", "Descriptive"])

    with st.form("user_inputs"):
        uploaded_file = st.file_uploader("Upload a PDF or txt file")
        question_count = st.number_input("Number of questions", min_value=3, max_value=50)
        subject = st.text_input("Insert subject", max_chars=50)
        tone = st.text_input("Complexity level of questions", max_chars=50, placeholder="Simple")
        button = st.form_submit_button("Generate Questions")

        if button and uploaded_file is not None and question_count and subject and tone:
            with st.spinner("Generating questions..."):
                try:
                    text = read_file(uploaded_file)
                    
                    if question_type == "Multiple Choice":
                        response_json = MCQ_RESPONSE_JSON
                    elif question_type == "True/False":
                        response_json = TRUEFALSE_RESPONSE_JSON
                    elif question_type == "Descriptive":
                        response_json = DESCRIPTIVE_RESPONSE_JSON
                
                    with get_openai_callback() as cb:
                        response = generate_evaluate_chain({
                            "text": text,
                            "number": question_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(response_json),
                            "question_type": question_type
                        })
                except Exception as e:
                    logging.error(f"Error in generate_evaluate_chain: {str(e)}")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    st.error(f"An error occurred: {str(e)}")
                else:
                    logging.info(f"Total tokens: {cb.total_tokens}")
                    logging.info(f"Prompt tokens: {cb.prompt_tokens}")
                    logging.info(f"Completion tokens: {cb.completion_tokens}")
                    logging.info(f"Total cost: {cb.total_cost}")

                    if isinstance(response, dict):
                        quiz = response.get('quiz', None)
                        if quiz is not None:
                            logging.info(f"Received quiz: {quiz}")
                            quiz = quiz.strip("```").strip()
                            quiz = quiz.replace("### RESPONSE_JSON", "", 1).strip()
                            try:
                                quiz_data = json.loads(quiz)
                                st.session_state['generated_quiz'] = quiz_data
                                st.session_state['question_type'] = question_type
                                st.success("Questions generated successfully!")
                            except json.JSONDecodeError as e:
                                st.error("Failed to parse quiz data. Please try again.")
                                logging.error(f"JSONDecodeError: {str(e)}")
                                logging.error(f"Problematic quiz data: {quiz}")
                        else:
                            st.error("Failed to generate questions. The 'quiz' key is missing from the response.")
                            logging.error(f"Quiz key missing from response: {response}")
                    else:
                        st.error("Unexpected response format. Please try again.")
                        logging.error(f"Unexpected response format: {response}")

### Take Assessment Tab ###
with tab2:
    st.header("Take Assessment")

    if not st.session_state.get('generated_quiz'):
        st.warning("Please generate questions in the 'Generate Questions' tab first.")
    else:
        questions = st.session_state.get('generated_quiz', {})
        user_answers = {}

        for key, q in questions.items():
            st.subheader(f"Question {key}")
            question_text = q.get('question') or q.get('mcq') or 'Question text not found.'

            st.write(question_text)

            if st.session_state['question_type'] == "Multiple Choice":
                choices = q.get('options', {})
                user_answer = st.radio(f"Select an answer for Question {key}", options=list(choices.values()), key=f"q{key}")
                correct_key = [k for k, v in choices.items() if v == user_answer][0] if user_answer else None
            elif st.session_state['question_type'] == "True/False":
                user_answer = st.radio(f"Select an answer for Question {key}", options=["True", "False"], key=f"q{key}")
                correct_key = user_answer.lower() if user_answer else None
            elif st.session_state['question_type'] == "Descriptive":
                user_answer = st.text_area(f"Your answer for Question {key}", key=f"q{key}")
                correct_key = None

            user_answers[key] = {
                "user_answer": user_answer,
                "correct_key": correct_key,
                "correct_answer": q.get('correct', "").lower() if st.session_state['question_type'] != "Descriptive" else q.get('solution', "")
            }

        if st.button("Submit Assessment"):
            total_questions = len(questions)
            correct_answers = 0
            feedback = []

            for key, q in questions.items():
                answer_data = user_answers.get(key, {})
                user_answer = answer_data.get("user_answer", "")
                correct_answer = answer_data.get("correct_answer", "")
                correct_key = answer_data.get("correct_key", "")

                if st.session_state['question_type'] in ["Multiple Choice", "True/False"]:
                    if correct_key and correct_key.lower() == correct_answer:
                        correct_answers += 1
                        feedback.append(f"Question {key}: Correct")
                    else:
                        correct_option = q['options'][q['correct']] if 'options' in q else q['correct']
                        feedback.append(f"Question {key}: Incorrect. The correct answer is {correct_option}")
                elif st.session_state['question_type'] == "Descriptive":
                    feedback.append(f"Question {key}: Your answer - {user_answer}\nSuggested answer - {correct_answer}")

            percentage_score = (correct_answers / total_questions) * 100
            st.subheader("Assessment Results")
            st.write(f"Your score: {correct_answers}/{total_questions} ({percentage_score:.2f}%)")

            st.session_state['user_performance'].append(percentage_score)
            
            st.subheader("Feedback")
            for fb in feedback:
                st.write(fb)

### Review Quiz Tab ###
with tab3:
    st.header("Review Quiz")
    if not st.session_state.get('generated_quiz'):
        st.warning("Please generate questions in the 'Generate Questions' tab first.")
    else:
        questions = st.session_state.get('generated_quiz', {})
        for key, q in questions.items():
            st.subheader(f"Question {key}")
            
            question_text = q.get('question') or q.get('mcq') or 'Question text not found.'
            st.write(question_text)
            
            if st.session_state['question_type'] == "Descriptive":
                st.write(f"**Solution:** {q.get('solution', 'Solution not found.')}")
            else:
                for opt_key, opt_value in q.get('options', {}).items():
                    st.write(f"{opt_key}. {opt_value}")
                st.write(f"**Correct Answer:** {q['correct']}")

        if st.button("Export Quiz as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for key, q in questions.items():
                question_text = q.get('question') or q.get('mcq') or 'Question text not found.'
                pdf.multi_cell(0, 10, f"Question {key}: {question_text}")
                if st.session_state['question_type'] == "Descriptive":
                    pdf.multi_cell(0, 10, f"Solution: {q.get('solution', '')}")
                else:
                    for opt_key, opt_value in q.get('options', {}).items():
                        pdf.multi_cell(0, 10, f"{opt_key}. {opt_value}")
                    pdf.multi_cell(0, 10, f"Correct Answer: {q['options'][q['correct']]}")

            pdf_output = pdf.output(dest="S").encode("latin1")
            b64 = base64.b64encode(pdf_output).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="generated_quiz.pdf">Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("Quiz exported as PDF successfully!")

### Performance Tracking Tab ###
with tab4:
    st.header("User Performance Tracking")
    if not st.session_state['user_performance']:
        st.warning("No assessments taken yet.")
    else:
        st.line_chart(st.session_state['user_performance'])
        avg_score = sum(st.session_state['user_performance']) / len(st.session_state['user_performance'])
        st.write(f"Average Score: {avg_score:.2f}%")

### Generate Notes Tab ###
def generate_notes(text, model, api_key, temperature=0.5, max_tokens=150):
    prompt = f"Please generate concise and useful short notes for study preparation based on the following text:\n\n{text}"
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template=prompt
    )

    chat_model = ChatOpenAI(
        openai_api_key=api_key,
        model_name=model,
        temperature=temperature,
        max_tokens=max_tokens
    )

    chain = LLMChain(llm=chat_model, prompt=prompt_template)
    return chain.run(text=text)

with tab5:
    st.header("Generate Quick Short Notes")
    uploaded_file_notes = st.file_uploader("Upload a PDF or txt file for notes", type=["pdf", "txt"])
    button_notes = st.button("Generate Notes")

    if button_notes and uploaded_file_notes is not None:
        with st.spinner("Generating notes..."):
            try:
                text = read_file(uploaded_file_notes)
                notes = generate_notes(text, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

                if notes:
                    st.session_state['generated_notes'] = notes
                    st.markdown("### Generated Short Notes")
                    st.write(notes)
                else:
                    st.error("Failed to generate notes. The result was empty.")
            except Exception as e:
                logging.error(f"Error generating notes: {str(e)}")
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"An error occurred: {str(e)}")

### Generate Podcast Tab ###
with tab6:
    st.header("Generate Podcast")

    uploaded_file_summary = st.file_uploader("Upload a PDF for summary", type=["pdf"])
    button_summary = st.button("Generate Podcast")

    if button_summary and uploaded_file_summary is not None:
        with st.spinner("Generating summary and podcast..."):
            try:
                text = read_file(uploaded_file_summary)
                openai_api_key = os.getenv("OPENAI_API_KEY")
                model = "gpt-3.5-turbo"

                # Generate summary using the same method as generate notes
                summary = generate_notes(text, model, openai_api_key)
                st.session_state['generated_summary'] = summary

                # Create TTS audio file
                client = OpenAI(api_key=openai_api_key)
                speech_file_path = "speech.mp3"
                response = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=summary
                )
                response.stream_to_file(speech_file_path)
                st.session_state['audio_file_path'] = speech_file_path

                st.success("Podcast generated successfully!")
            except Exception as e:
                logging.error(f"Error generating podcast: {str(e)}")
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"An error occurred: {str(e)}")

    if st.session_state['audio_file_path']:
        audio_file = open(st.session_state['audio_file_path'], 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')