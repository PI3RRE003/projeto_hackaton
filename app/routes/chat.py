from flask import Blueprint, request, jsonify
from openai import OpenAI
import os

chat_bp = Blueprint("chat", __name__)

# Configurar o cliente OpenAI (coloque sua API Key no .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    paciente_message = data.get("message")

    if not paciente_message:
        return jsonify({"error": "Mensagem não enviada"}), 400

    try:
        # Chamada ao GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # pode trocar por outro modelo
            messages=[
                {"role": "system", "content": "Você é um assistente útil e responde em português."},
                {"role": "user", "content": paciente_message},
            ],
            max_tokens=200
        )

        gpt_reply = response.choices[0].message.content

        return jsonify({
            "user": paciente_message,
            "assistant": gpt_reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
