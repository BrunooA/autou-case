from flask import Flask, render_template, request

app = Flask(__name__)

# --- Classificação simplificada (baseline) ---
def classify_email(text):
    text = text.lower()

    produtivo_keywords = ["status", "requerimento", "anexo", "documento", "suporte", "ajuda", "processo"]
    improdutivo_keywords = ["feliz natal", "bom dia", "obrigado", "parabéns"]

    if any(word in text for word in produtivo_keywords):
        return "Produtivo"
    elif any(word in text for word in improdutivo_keywords):
        return "Improdutivo"
    else:
        return "Produtivo"

# --- Resposta sugerida ---
def suggest_response(category):
    if category == "Produtivo":
        return "Obrigado pelo contato. Sua solicitação será analisada e retornaremos em breve com o status atualizado."
    else:
        return "Agradecemos sua mensagem! Desejamos um ótimo dia."

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    response = None
    if request.method == "POST":
        email_text = request.form["email_text"]
        result = classify_email(email_text)
        response = suggest_response(result)

    return render_template("index.html", result=result, response=response)

if __name__ == "__main__":
    app.run(debug=True)
