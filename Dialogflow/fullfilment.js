"use strict";

const functions = require("firebase-functions");
const { WebhookClient } = require("dialogflow-fulfillment");
const { Card, Suggestion } = require("dialogflow-fulfillment");

process.env.DEBUG = "dialogflow:debug"; // enables lib debugging statements

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(
  (request, response) => {
    const agent = new WebhookClient({ request, response });
    console.log(
      "Dialogflow Request headers: " + JSON.stringify(request.headers)
    );
    console.log("Dialogflow Request body: " + JSON.stringify(request.body));

    function nutrition_info(agent) {
      agent.context.set("intent_nutrition_info_question", 1);
    }

    function handleUserInput(agent) {
      // Get user's input
      const userInput = agent.query;

      // Handle the user's input
      agent.add(`Handling user's input: ${userInput}`);
    }

    let intentMap = new Map();
    intentMap.set("intent_nutrition_info", nutrition_info);
    intentMap.set("intent_nutrition_info_question", handleUserInput); // Corrected event name
    agent.handleRequest(intentMap);
  }
);