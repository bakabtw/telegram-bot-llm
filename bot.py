import json
import os

from telethon import TelegramClient, events
from models.gemini import GeminiModel


class SimpleTelegramBot:
    def __init__(self, api_id, api_hash, bot_token, gemini_token):
        """Initialize the bot with API credentials and a bot token."""
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.client = TelegramClient('bot', self.api_id, self.api_hash).start(bot_token=self.bot_token)

        # Define a list of intents
        intents = [
            {"intent": "Greeting", "description": "User is saying hello or initiating a conversation."},
            {"intent": "Order Status", "description": "User is asking about the status of their order."},
            {"intent": "Product Inquiry",
             "description": "User is asking about a product's details, availability, or price."},
            {"intent": "Complaint", "description": "User is expressing dissatisfaction or reporting an issue."},
            {"intent": "Goodbye", "description": "User is ending the conversation."}
        ]

        intent_prompt = (
                "Classify the user input into one of the following intents:\n\n" +
                "\n".join([f"- {intent['intent']}: {intent['description']}" for intent in intents]) + "\n" +
                "Reply in format {\"intent\": \"user's intent\"}"
        )

        model_prompt = "You're a regular chatbot."

        self.model = GeminiModel(api_key=gemini_token,
                                 prompt=model_prompt)
        self.intent_model = GeminiModel(api_key=gemini_token,
                                        prompt=intent_prompt)

    def register_handlers(self):
        """Register event handlers for the bot."""

        # Handle /start command
        @self.client.on(events.NewMessage(pattern='/start'))
        async def handle_start(event):
            await event.reply('Hello! I am your bot. How can I assist you today?')

        # Handle /change-system command
        @self.client.on(events.NewMessage(pattern='/change-system'))
        async def handle_change_system(event):
            print(event.text[len("/change-system") + 1:])
            await self.model.change_system_prompt(event.text[len(event.text) + 1:])
            await event.reply(event.text)

        # Handle any new message
        @self.client.on(events.NewMessage)
        async def handle_message(event):
            intent_request = await self.intent_model.generate_content(event.text)

            try:
                intent = json.loads(intent_request)['intent']

                if intent == 'Product Inquiry':
                    message = "I cannot tell you the price right now"
                else:
                    message = await self.model.generate_content(event.text)
            except Exception as e:
                message = f"Error: {e}"

            await event.reply(message)

    def run(self):
        """Run the bot until it is disconnected."""
        self.register_handlers()
        print("Bot is running...")
        self.client.run_until_disconnected()


if __name__ == "__main__":
    API_ID = os.environ.get('API_ID')
    API_HASH = os.environ.get('API_HASH')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    GEMINI_TOKEN = os.environ.get('GEMINI_TOKEN')

    # Create and run the bot
    bot = SimpleTelegramBot(API_ID, API_HASH, BOT_TOKEN, GEMINI_TOKEN)
    bot.run()
