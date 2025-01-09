# MyBot

MyBot is an intelligent chatbot built using the BotBuilder framework. It leverages various perspectives to generate insightful responses and enhance user interactions.

## Features

- **Multiple Perspectives**: Generates responses from different perspectives such as Newton, Da Vinci, Human Intuition, Neural Network, Quantum Computing, and more.
- **Sentiment Analysis**: Analyzes user sentiment using VADER and TextBlob.
- **Context Awareness**: Enhances context awareness by analyzing the user's environment, activities, and emotional state.
- **Ethical Decision Making**: Integrates ethical principles into decision-making processes.
- **Transparency and Explainability**: Provides transparency by explaining the reasoning behind decisions.

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/mybot.git
cd mybot
2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the required dependencies:
pip install -r requirements.txt
4. Create a `.env` file and add your environment variables:
AZURE_OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
LUIS_ENDPOINT=your_luis_endpoint
LUIS_API_VERSION=your_luis_api_version
LUIS_API_KEY=your_luis_api_key
5. Run the bot:
python main.py## Usage

- Interact with the bot by sending messages.
- The bot will generate responses from different perspectives and provide insightful answers.
- You can customize the enabled perspectives in the `config.json` file.

## Configuration

The bot uses a configuration file (`config.json`) to manage settings. Ensure that the configuration file is valid by using the provided schema (`config_schema.json`).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
# MyBot

MyBot is an intelligent chatbot built using the BotBuilder framework. It leverages various perspectives to generate insightful responses and enhance user interactions.

## Features

- **Multiple Perspectives**: Generates responses from different perspectives such as Newton, Da Vinci, Human Intuition, Neural Network, Quantum Computing, and more.
- **Sentiment Analysis**: Analyzes user sentiment using VADER and TextBlob.
- **Context Awareness**: Enhances context awareness by analyzing the user's environment, activities, and emotional state.
- **Ethical Decision Making**: Integrates ethical principles into decision-making processes.
- **Transparency and Explainability**: Provides transparency by explaining the reasoning behind decisions.
- **Dialog Management**: Manages conversations using the BotBuilder Dialog framework.

## Installation

1. Clone the repository:
