from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Asegúrate de configurarla en Render

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    parameters = req.get("queryResult", {}).get("parameters", {})
    resultado = parameters.get("resultado", "")

    if not resultado:
        return jsonify({
            "fulfillmentText": "Por favor, envíame los resultados médicos en texto para poder analizarlos."
        })

    prompt = f"""Eres un médico neumólogo. Explica de forma clara para un paciente los siguientes resultados médicos:\n\n{resultado}\n\nIncluye observaciones clave y recomendaciones generales."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        ai_response = "Ocurrió un error al procesar los resultados. Intenta más tarde."

    return jsonify({
        "fulfillmentText": ai_response
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)