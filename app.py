from flask import Flask, render_template, request
import openai, json, re, os
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

# --- Configure sua chave ---
openai.api_key = ""

def classify_and_respond(email_text):
    prompt = f"""
Você é um assistente que classifica emails em duas categorias:
1. Produtivo: requer ação ou resposta (solicitações, documentos, dúvidas técnicas)
2. Improdutivo: não requer ação imediata (agradecimentos, felicitações, mensagens sociais)

Exemplos:
- "Oi, parabéns pelo seu trabalho!" -> Improdutivo
- "Obrigado pela atenção." -> Improdutivo
- "Preciso de ajuda para configurar o sistema." -> Produtivo
- "Segue em anexo o contrato solicitado." -> Produtivo

Classifique o email abaixo e sugira uma resposta adequada.
Retorne SOMENTE JSON válido no formato:

{{
  "categoria": "Produtivo ou Improdutivo",
  "resposta": "Texto da resposta sugerida"
}}

Email:
\"\"\"{email_text}\"\"\"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0
        )

        content = response['choices'][0]['message']['content'].strip()

        # Extrai JSON do texto
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("Resposta não contém JSON válido")

        result = json.loads(match.group(0))

        categoria = result.get("categoria", "").strip().capitalize()
        resposta = result.get("resposta", "").strip()

        if categoria not in ["Produtivo", "Improdutivo"]:
            categoria = "Indefinido"

        return categoria, resposta

    except Exception as e:
        print("Erro IA:", e)
        return "Indefinido", "Não consegui classificar este email."


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    response_text = None
    if request.method == "POST":
        email_text = request.form["email_text"]
        result, response_text = classify_and_respond(email_text)
    return render_template("index.html", result=result, response=response_text)


# --- Rota de teste ---
@app.route("/teste")
def teste():
    frases = [
        "Oi, parabéns pelo seu trabalho!",
        "Bom dia, segue em anexo o contrato solicitado",
        "Obrigado pela atenção.",
        "Preciso de ajuda para configurar o sistema."
    ]
    resultados = []
    for frase in frases:
        categoria, resposta = classify_and_respond(frase)
        resultados.append({"email": frase, "categoria": categoria, "resposta": resposta})
    return render_template("teste.html", resultados=resultados)


if __name__ == "__main__":
    app.run(debug=True)
