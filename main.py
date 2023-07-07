# Environment variables
import os
# NLP Conversational Model
from google.cloud import dialogflow
import uuid
from google.oauth2 import service_account
import time
# Large Language Model
from google.oauth2 import service_account
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import aiplatform
# Computer Vision Model
from roboflow import Roboflow
# Web Application
import gradio as gr

service_account_key = os.getenv('service_account_key')
credentials = service_account.Credentials.from_service_account_file(service_account_key)

session_id = uuid.uuid4().hex
# Load the variables to access the databases
project_id = os.getenv('project_id')
language_code = 'en'

# Create the session with the appropriate credentials
session_client = dialogflow.SessionsClient(credentials=credentials)

session = session_client.session_path(project_id, session_id)

region = os.getenv('region')
aiplatform.init(project=project_id, location=region)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key

parameters = {
    "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
    "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
}

model = TextGenerationModel.from_pretrained("text-bison@001")

api_key = os.getenv('roboflow_api_key')
rf = Roboflow(api_key=api_key)

project = rf.workspace().project("food_detection-cxap6")
vision_model = project.version(1).model

# Function to request an answer to our dialogflow agent according to a text 
def dialogflow_request(text, language_code):
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    response_message = str(response.query_result.fulfillment_messages[0].text.text[0])
    # If statement to connect to the LLM model in specific cases
    if "<<<llmquestion" in response_message:
        llm_response = model.predict((response_message.split("<<<llmquestion:")[1][:-3]), **parameters)
        return llm_response.text
    else:
        return response_message


def image_recognition(imagePath):
    try:
        results = vision_model.predict(imagePath, confidence=40, overlap=30).json()
        if results['predictions'] == []:
            prediction = 'Not found'
        else:
            prediction = results['predictions'][0]['class']
    except Exception as e:
        prediction = 'Error: ' + str(e)
    return prediction

# Web Application functions to allow the front-end to interact with the user
def respond(message, chat_history):
    if len(chat_history) > 1 and (chat_history[-2][-1] == "Sure, please provide an image for the computer vision model to recognize" or chat_history[-1][-1] == "No food detected. Please provide another image path." or chat_history[-1][-1] == "Invalid path. Please provide another image path."):
        prediction = image_recognition(message)
        print(prediction)
        if "No such file or directory" in prediction:
            chat_history.append((None, "Invalid path. Please provide another image path."))
        elif prediction == "Not found":
            chat_history.append((None, "No food detected. Please provide another image path."))
        else:
            bot_message = dialogflow_request(''.join(prediction.split()).replace("'", ""), 'en')
            chat_history.append((None, bot_message))
    elif isinstance(message, str):
        # If the message is a string, treat it as a text input
        bot_message = dialogflow_request(message, 'en')
        chat_history.append((message, bot_message))

    else:
        bot_message = "Invalid input"
        chat_history.append((message, bot_message))
    
    time.sleep(1)
    return "", chat_history

# Function to add a file
def add_file(history, file):
    history.append(((file.name,), None))
    respond(file.name, history)
    return history


with gr.Blocks(css=".gradio-container {background-color: #0E2C4B}") as demo:
    disclaimer_agreed = gr.State(False)
    def conditions_met(newValue):
        disclaimer_agreed.value = newValue
    
    gr.Markdown("""
            <h1 style="text-align: center; color:white;" >FitBot</h1>
            <h4 style="text-align: center; color:white">Your personal food and health assistant</h4>
            """)

    with gr.Row():
        with gr.Column(scale=4):
            # Create a chatbot component and a model component
            chatbot = gr.Chatbot([], elem_id="chatbot", label="FitBot").style()
        with gr.Column(scale=1):
            gr.Markdown("""
            <h2 style="color:white" >Disclaimer</h2>
            <p style="color:white">The following bot is not meant following any regulatory health practice. All the information that is presented to you
            is generated from Vertex AI, the generative AI developed by Google. If you are interested in knowing more about the project and how this model
            was built, please refer to the following <a href="https://github.com/Niccoborg22/virtual-nutritionist-bot" style="color:white">Github link</a></p>
            """)

    with gr.Row():
        # Create a textbox component
        with gr.Column(scale=8):
            msg = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
        with gr.Column(scale=1, min_width=0):
            # Create an upload button component to add images
            btn = gr.UploadButton("📁", file_types=["image"])

    with gr.Row(scale=0.7):
        clear_btn = gr.Button(value="🗑️  Clear")

    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False)
    clear_btn.click(lambda: None, None, chatbot, queue=False)

    

# launch the application
if __name__ == "__main__":
    demo.launch(share=True)