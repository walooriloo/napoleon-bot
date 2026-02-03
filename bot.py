import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import anthropic

# Charger les tokens
load_dotenv()

# Initialiser Slack et Claude
app = App(token=os.environ["SLACK_BOT_TOKEN"])
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Contexte du bot Napoleon Saga
SYSTEM_PROMPT = """Tu es un assistant expert du jeu de plateau Napoleon Saga: Waterloo.
Tu aides les joueurs à comprendre les règles, la stratégie et les mécaniques du jeu.
Tu réponds en français de manière claire et pédagogique.
Si on te pose une question hors sujet, ramène gentiment la conversation vers Napoleon Saga."""

def ask_claude(question):
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}]
    )
    return message.content[0].text

# Répondre aux mentions @NapoleonBot
@app.event("app_mention")
def handle_mention(event, say):
    text = event["text"]
    response = ask_claude(text)
    say(response)

# Répondre aux messages directs
@app.event("message")
def handle_message(event, say):
    if event.get("channel_type") == "im":
        text = event["text"]
        response = ask_claude(text)
        say(response)

# Lancer le bot
if __name__ == "__main__":
    print("🎖️ NapoleonBot est prêt ! En attente de messages...")
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()


