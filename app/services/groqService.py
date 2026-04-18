from groq import Groq
import os

def extrair_codigo(resposta: str) -> str:
    resposta = resposta.strip()
    if "```python" in resposta:
        resposta = resposta.split("```python")[1]
        resposta = resposta.split("```")[0]
    return resposta.strip()

def gerar_codigo(pergunta: str, colunas: list, tipos: dict, amostra: list) -> str:
    # Client criado aqui dentro — só roda quando a função é chamada,
    # depois do load_dotenv() já ter executado no main.py
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": f"""Você é um gerador de código Pandas.
Regras obrigatórias:
- Retorne APENAS código Python puro, sem markdown, sem explicações
- O DataFrame já existe na variável `df`. NUNCA recrie o df
- NUNCA use import de nenhum tipo
- Sempre salve o resultado final na variável `result`

Informações do DataFrame:
- Colunas: {colunas}
- Tipos: {tipos}
- Amostra: {amostra}"""
        },
        {
            "role": "user",
            "content": pergunta
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return extrair_codigo(response.choices[0].message.content)