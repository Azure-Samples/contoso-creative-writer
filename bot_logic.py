import logging
from botbuilder.core import TurnContext, MessageFactory, ConversationState, UserState
from botbuilder.schema import Activity, ActivityTypes, EndOfConversationCodes
from UniversalReasoning import UniversalReasoning  # Ensure correct import
import os
from dotenv import load_dotenv
from dialog_bot import DialogBot
from main_dialog import MainDialog

# Load environment variables from .env file
load_dotenv()

class MyBot(DialogBot):
    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: MainDialog):
        super(MyBot, self).__init__(conversation_state, user_state, dialog)
        self.context = {}
        self.feedback = []
        config = load_and_validate_config('config.json', 'config_schema.json')
        # Add Azure OpenAI and LUIS configurations to the config
        config['azure_openai_api_key'] = os.getenv('AZURE_OPENAI_API_KEY')
        config['azure_openai_endpoint'] = os.getenv('AZURE_OPENAI_ENDPOINT')
        config['luis_endpoint'] = os.getenv('LUIS_ENDPOINT')
        config['luis_api_version'] = os.getenv('LUIS_API_VERSION')
        config['luis_api_key'] = os.getenv('LUIS_API_KEY')
        setup_logging(config)
        self.universal_reasoning = UniversalReasoning(config)

    async def enhance_context_awareness(self, user_id: str, text: str) -> None:
        """Enhance context awareness by analyzing the user's environment, activities, and emotional state."""
        sentiment = analyze_sentiment_vader(text)
        self.context[user_id].append({"text": text, "sentiment": sentiment})

    async def proactive_learning(self, user_id: str, feedback: str) -> None:
        """Encourage proactive learning by seeking feedback and exploring new topics."""
        self.context[user_id].append({"feedback": feedback})
        self.feedback.append({"user_id": user_id, "feedback": feedback})

    async def ethical_decision_making(self, user_id: str, decision: str) -> None:
        """Integrate ethical principles into decision-making processes."""
        ethical_decision = f"Considering ethical principles, the decision is: {decision}"
        self.context[user_id].append({"ethical_decision": ethical_decision})

    async def emotional_intelligence(self, user_id: str, text: str) -> str:
        """Develop emotional intelligence by recognizing and responding to user emotions."""
        sentiment = analyze_sentiment_vader(text)
        response = self.generate_emotional_response(sentiment, text)
        self.context[user_id].append({"emotional_response": response})
        return response

    def generate_emotional_response(self, sentiment: dict, text: str) -> str:
        """Generate an empathetic response based on the sentiment analysis."""
        if sentiment['compound'] >= 0.05:
            return "I'm glad to hear that! 😊 How can I assist you further?"
        elif sentiment['compound'] <= -0.05:
            return "I'm sorry to hear that. 😢 Is there anything I can do to help?"
        else:
            return "I understand. How can I assist you further?"

    async def transparency_and_explainability(self, user_id: str, decision: str) -> str:
        """Enable transparency by explaining the reasoning behind decisions."""
        explanation = f"The decision was made based on the following context: {self.context[user_id]}"
        self.context[user_id].append({"explanation": explanation})
        return explanation

    async def on_message_activity(self, turn_context: TurnContext) -> None:
        """Handles incoming messages and generates responses."""
        user_id = turn_context.activity.from_property.id
        if user_id not in self.context:
            self.context[user_id] = []
        try:
            message_text = turn_context.activity.text.strip().lower()
            if "end" in message_text or "stop" in message_text:
                await end_conversation(turn_context)
                self.context.pop(user_id, None)
            else:
                self.context[user_id].append(turn_context.activity.text)
                response = await self.generate_response(turn_context.activity.text, user_id)
                await turn_context.send_activity(MessageFactory.text(response))
                await self.request_feedback(turn_context, user_id)
        except Exception as e:
            await handle_error(turn_context, e)

    async def generate_response(self, text: str, user_id: str) -> str:
        """Generates a response using UniversalReasoning."""
        try:
            logging.info(f"Generating response for user_id: {user_id} with text: {text}")
            response = self.universal_reasoning.generate_response(text)
            logging.info(f"Generated response: {response}")
            return response
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "Sorry, I couldn't generate a response at this time."

    async def request_feedback(self, turn_context: TurnContext, user_id: str) -> None:
        """Request feedback from the user about the bot's response."""
        feedback_prompt = "How would you rate my response? (good/neutral/bad)"
        await turn_context.send_activity(MessageFactory.text(feedback_prompt))

    async def handle_feedback(self, turn_context: TurnContext) -> None:
        """Handle user feedback and store it for future analysis."""
        user_id = turn_context.activity.from_property.id
        feedback = turn_context.activity.text.lower()
        if feedback in ["good", "neutral", "bad"]:
            self.feedback.append({"user_id": user_id, "feedback": feedback})
            await turn_context.send_activity(MessageFactory.text("Thank you for your feedback!"))
        else:
            await turn_context.send_activity(MessageFactory.text("Please provide feedback as 'good', 'neutral', or 'bad'."))

async def end_conversation(turn_context: TurnContext) -> None:
    """Ends the conversation with the user."""
    await turn_context.send_activity(
        MessageFactory.text("Ending conversation from the skill...")
    )
    end_of_conversation = Activity(type=ActivityTypes.end_of_conversation)
    end_of_conversation.code = EndOfConversationCodes.completed_successfully
    await turn_context.send_activity(end_of_conversation)

async def handle_error(turn_context: TurnContext, error: Exception) -> None:
    """Handles errors by logging them and notifying the user."""
    logging.error(f"An error occurred: {error}")
    await turn_context.send_activity(
        MessageFactory.text("An error occurred. Please try again later.")
    )
