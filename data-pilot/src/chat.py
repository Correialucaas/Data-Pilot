"""Chat com OpenRouter: o modelo escolhe a ferramenta, o Python executa."""
import json
import os
import requests
from dotenv import load_dotenv
from src.tools import TOOLS, executar

load_dotenv()
URL = "https://openrouter.ai/api/v1/chat/completions"
SYSTEM = ("Você é o Data Pilot, assistente de análise de vendas. Responda em português. "
          "NUNCA invente números: para qualquer valor, chame uma ferramenta e use apenas o resultado. "
          "Valores monetários em R$.")


def _chamar(messages):
    chave = os.getenv("OPENROUTER_API_KEY")
    if not chave:
        raise RuntimeError("Defina OPENROUTER_API_KEY no arquivo .env")
    resp = requests.post(
        URL, timeout=60,
        headers={"Authorization": f"Bearer {chave}"},
        json={"model": os.getenv("OPENROUTER_MODEL", "openrouter/free"),
              "messages": messages, "tools": TOOLS})
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]


def responder(pergunta: str, df, tentativas: int = 2) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": pergunta}]
    erro = "erro desconhecido"
    for _ in range(tentativas + 1):  # modelo gratuito falha as vezes
        try:
            for _ in range(4):  # limite de rodadas de ferramentas
                msg = _chamar(messages)
                if not msg.get("tool_calls"):
                    return msg.get("content") or "Sem resposta do modelo."
                messages.append(msg)
                for call in msg["tool_calls"]:
                    args = json.loads(call["function"].get("arguments") or "{}")
                    messages.append({"role": "tool", "tool_call_id": call["id"],
                                     "content": executar(call["function"]["name"], args, df)})
        except RuntimeError as e:
            return str(e)
        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            erro = e
    return f"Não consegui responder agora ({erro}). Tente novamente."
