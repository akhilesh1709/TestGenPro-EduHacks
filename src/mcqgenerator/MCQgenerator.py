import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import streamlit as st

load_dotenv()

# Access the environment variables
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please check your .env file.")

llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.7)

quiz_generation_template = """
Text: {text}
You are an expert assessment maker, specializing in everything possible. Given the above text, create a quiz of {number} {question_type} questions for {subject} students. 
Ensure the questions are of a {tone} difficulty level, requiring appropriate knowledge and understanding of accounting principles. 
Make sure the questions are not repeated and thoroughly validate each question to ensure it conforms to the text. 
Format your response like RESPONSE_JSON below and use it as a guide. Ensure to make {number} questions.

For Descriptive questions, include both the question and a detailed solution.

### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "question_type", "tone", "response_json"],
    template=quiz_generation_template
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

quiz_evaluation_template = """
You are an expert English grammarian and writer. Given a {question_type} Quiz for {subject} students,
you need to evaluate the complexity of the questions and provide a complete analysis of the quiz. Use a maximum of 50 words for the complexity analysis. 
If the quiz does not match the {tone} difficulty level for the students,
update the quiz questions that need to be changed and adjust the tone so that it perfectly fits the students' abilities.

Quiz:
{quiz}

Please review the quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["question_type", "subject", "tone", "quiz"],
    template=quiz_evaluation_template
)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain], 
    input_variables=["text", "number", "question_type", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"], 
    verbose=True
)
