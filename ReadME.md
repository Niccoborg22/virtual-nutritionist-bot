<p align="center">
  <img src="https://github.com/Niccoborg22/virtual-nutritionist-bot/assets/114337279/987ad985-2afd-4c93-9d2b-680fb43ce978" alt="Small logo" width="20%">
</p>
<h3 align="center">Fitbot: Nutrition Assistant</h3>

<p align="center"><b>Done by:</b> João André Pinho, Max Heilingbrunner, Niccolò Matteo Borgato, Nicholas Dieke</p>

## TECHONOLOGIES
The technologies used in this application are :
- NLP Conversational Model 
    - Google Dialogflow
- Large Language Model 
    - Google Vertex AI (Palm2)
- Computer Vision Model
    - Roboflow
    - Ultralytics YoloV8
- Web Application
    - Gradio


## ARCHITECTURE
![image](https://github.com/Niccoborg22/virtual-nutritionist-bot/assets/114749413/e9a3f9b0-03be-42f1-adaa-8c88302ed0e6)


## NLP CONVERSATIONAL MODEL
### Goal
---
The goal of the chatbot is to help people increase their nutritional awareness by creating a chatbot experience.

### Technology
---
The NLP Conversational Model has been developed using the following technologies: 
- Google Dialogflow
- Python
- Node.Js

### Persona
---
The persona of this chatbot is anyone that is concerned about his health and wants to have visibility on his eating.

### Future improvements
---
Some further future improvements to be implemented:
- Add identification in the frontend and improve context awareness by having access to previous conversations of the user once this one is identified.
- Have a non-relational database linked to each account to keep track of each account's data.
- Create a Web Application that, upon identification, visualize your data.
- Continuosly store and process the 80% FAQ in order to improve the usefulness and robustness of the conversational model to user's most common prompts.


### Intent architecture
---
The NLP Conversational Model has been developed using Google Dialogflow, the intents have been architected using the following schema: 
![image](https://github.com/Niccoborg22/virtual-nutritionist-bot/assets/114749413/62eae0d8-c5ed-420d-a8f7-d037976171fb)

Some of the answers provided by the chatbot will be returned using Vertex AI and the LLM model offered by Google. In order to do so the interaction between the Conversational Model and Vertex AI has been coded using Python.

**Entities utilized**
In order for the intents to work properly, the following entities have been created:
- @entity_foodtype: Set of all the food types that the computer vision model can recognize
- @entity_gender: Gender types, pre-built entity
- @entity_meal: Type of meal, breakfast, lunch or dinner


## COMPUTER VISION MODEL
### Goal
---
The goal of the Computer Vision Model is to recognize the food in the picture

### Technology
---
The Computer Vision Model has been developed using the following technologies: 
- Roboflow
- Ultralytics YOLOV8
- Python

![image](https://github.com/Niccoborg22/virtual-nutritionist-bot/assets/114337279/98926890-0d4f-4f67-b38e-dddaf2e444c1)

### Future improvements
---
Some further future improvements to be implemented:
- Create a more accurate model by increasing the number and diversity of the train images (i.e., foods from different cultures).
- Design a portion estimator that won't need to ask the user for the total number of grams of the dish.

## WEB APPLICATION
### Goal
---
The goal of the Web Application is to render a chat bot with which the user can interact by text and images

### Technology
---
The Web Application has been developed using the following technologies: 
- Python
- Gradio

### Future improvements
---
Some further future improvements to be implemented:
- Fix the picture upload functionality in order to be processed by the Computer Vision model instead of submitting the image local path.

### Images
---
![image](https://github.com/Niccoborg22/virtual-nutritionist-bot/assets/114749413/ab18161f-a0c5-43aa-82ff-5052b4afdf34)  
![image](https://github.com/Niccoborg22/virtual-nutritionist-bot/assets/114749413/6a4453a1-bda9-4d54-892b-d4a38f4ded83)


