import openai
import re, json

# --- Coloque sua chave aqui ---
openai.api_key = "sua_chave_aqui"

def classify_and_respond(email_text):
    prompt = f"""
Você é um classificador de emails.  
Retorne **somente JSON válido**, no formato:

{{
  "categoria": "Produtivo" ou "Improdutivo",
  "resposta": "Texto da resposta sugerida"
}}

Regras:
- "Produtivo": requer ação ou resposta (ex.: solicitação, dúvidas, documentos).
- "Improdutivo": não requer ação (ex.: agradecimento, parabéns, mensagens sociais).

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

        # Captura só o JSON
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("Resposta não contém JSON válido")

        json_text = match.group(0)
        result = json.loads(json_text)

        categoria = result.get("categoria", "").strip().capitalize()
        resposta = result.get("resposta", "").strip()

        if categoria not in ["Produtivo", "Improdutivo"]:
            categoria = "Indefinido"

        return categoria, resposta

    except Exception as e:
        print("Erro IA:", e)
        return "Indefinido", "Não consegui classificar este email."

# --- Frases de teste ---
frases = [
    "Oi, parabéns pelo seu trabalho!",              # improdutivo esperado
    "Bom dia, segue em anexo o contrato solicitado", # produtivo esperado
    "Obrigado pela atenção.",                       # improdutivo esperado
    "Preciso de ajuda para configurar o sistema."   # produtivo esperado
]

# --- Rodar testes ---
for frase in frases:
    categoria, resposta = classify_and_respond(frase)
    print(f"\nEmail: {frase}")
    print(f"Categoria: {categoria}")
    print(f"Resposta sugerida: {resposta}")
