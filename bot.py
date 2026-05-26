import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
RUBIKA_BOT_TOKEN = os.getenv("RUBIKA_BOT_TOKEN")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_reply(user_text: str) -> str:
    """Generate assistant reply using OpenAI Responses API."""
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You are a helpful Persian assistant for Rubika users.",
            },
            {"role": "user", "content": user_text},
        ],
    )
    return response.output_text.strip()


def send_message_to_rubika(chat_id: str, text: str) -> None:
    """
    Send message to Rubika.

    NOTE:
    You must replace this function with the official Rubika Bot API call used in your deployment.
    This placeholder prints to stdout so you can test end-to-end logic first.
    """
    if not RUBIKA_BOT_TOKEN:
        print(f"[DRY-RUN] chat_id={chat_id} message={text}")
        return

    # TODO: Replace with real Rubika API request.
    print(f"[RUBIKA API TODO] token={RUBIKA_BOT_TOKEN[:6]}... chat_id={chat_id} message={text}")


@app.route("/webhook", methods=["POST"])
def rubika_webhook():
    payload = request.get_json(silent=True) or {}

    # Expected payload (example):
    # {
    #   "chat_id": "12345",
    #   "text": "سلام"
    # }
    chat_id = str(payload.get("chat_id", "")).strip()
    text = str(payload.get("text", "")).strip()

    if not chat_id or not text:
        return jsonify({"ok": False, "error": "chat_id and text are required"}), 400

    try:
        reply = generate_reply(text)
        send_message_to_rubika(chat_id, reply)
        return jsonify({"ok": True})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "rubika-gpt-bot"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
