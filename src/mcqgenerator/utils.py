import PyPDF2
import json
import logging
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
            
        except Exception as e:
            logging.error(f"Error reading PDF file: {str(e)}")
            raise Exception(f"Error reading PDF file: {str(e)}")
        
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            logging.error(f"Error reading text file: {str(e)}")
            raise Exception(f"Error reading text file: {str(e)}")
    
    else:
        logging.error("Unsupported file format; only PDF and text files supported.")
        raise Exception("Unsupported file format; only PDF and text files supported.")

def get_document_data(quiz_str, question_type):
    try:
        logging.info(f"Received quiz_str: {quiz_str}")
        logging.info(f"Question type: {question_type}")

        if quiz_str.startswith("### RESPONSE_JSON"):
            quiz_str = quiz_str.replace("### RESPONSE_JSON", "", 1).strip()

        quiz_dict = json.loads(quiz_str)
        document_data = ""

        if not quiz_dict:
            logging.warning("quiz_dict is empty")
            return ""

        for index, (key, value) in enumerate(quiz_dict.items(), start=1):
            if question_type == "Multiple Choice":
                question = value.get("mcq", "")
                options = value.get("options", {})
                correct = value.get("correct", "")
                document_data += f"{index}. {question}\n"
                for option, option_value in options.items():
                    document_data += f"\n   {option}. {option_value}\n"
                document_data += f"\n   Correct Answer: {correct}\n\n"

            elif question_type == "True/False":
                question = value.get("question", "")
                correct = value.get("correct", "")
                document_data += f"{index}. {question}\n"
                document_data += f"\n   Correct Answer: {correct}\n\n"

            elif question_type == "Descriptive":
                question = value.get("question", "")
                solution = value.get("solution", "")

                document_data += f"{index}. {question}\n\n"
                document_data += f"\n   Answer:\n{solution}\n\n"
            
        logging.info(f"Generated document data: {document_data}")
        return document_data

    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {str(e)}")
        logging.error(f"Problematic JSON string: {quiz_str}")
        return ""
    
    except Exception as e:
        logging.error(f"Unexpected error in get_document_data: {str(e)}")
        logging.error(f"Problematic quiz_str: {quiz_str}")
        logging.error(traceback.format_exc())
        return ""

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
