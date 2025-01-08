import os
import logging
from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.integration.aiohttp import BotFrameworkHttpAdapter
from botbuilder.schema import Activity
from dotenv import load_dotenv
from utils import show_privacy_consent
from universal_reasoning import UniversalReasoning, load_json_config
from mybot import MyBot  # Import updated MyBot class
from main_dialog import MainDialog

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Show privacy consent dialog and check user response
if not show_privacy_consent():
    logging.info("User declined data collection and privacy policy. Exiting application.")
    exit()

# Load configuration
config = load_json_config("config.json")
config["azure_openai_api_key"] = os.getenv("AZURE_OPENAI_API_KEY")
config["azure_openai_endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize UniversalReasoning
universal_reasoning = UniversalReasoning(config)

# Create adapter
settings = BotFrameworkAdapterSettings(
    app_id=os.getenv("MICROSOFT_APP_ID"),
    app_password=os.getenv("MICROSOFT_APP_PASSWORD"),
)
adapter = BotFrameworkHttpAdapter(settings)

# Create MemoryStorage, ConversationState, and UserState
memory_storage = MemoryStorage()
conversation_state = ConversationState(memory_storage)
user_state = UserState(memory_storage)

# Create the main dialog
main_dialog = MainDialog("MainDialog")

# Create the bot and pass the universal_reasoning instance
bot = MyBot(conversation_state, user_state, main_dialog, universal_reasoning)

# Listen for incoming requests on /api/messages
async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    return web.Response(status=response.status)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
