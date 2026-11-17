"""Ferramentas que o modelo pode chamar. A descricao guia a escolha do modelo."""
import json
from src import metrics as m

_PARAMS = {
    "categoria": {"type": "string", "description": "Categoria: Eletrônicos, Moda, Casa ou Livros. Omita para todas."},
    "data_inicio": {"type": "string", "description": "Data inicial no formato AAAA-MM-DD (opcional)."},
    "data_fim": {"type": "string", "description": "Data final no formato AAAA-MM-DD (opcional)."},
}


def _tool(name, desc, params):
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object", "properties": {k: _PARAMS[k] for k in params}}}}


TOOLS = [
    _tool("receita_total", "Receita total (soma em R$ das vendas) de pedidos concluídos.", _PARAMS),
    _tool("total_pedidos", "Quantidade de pedidos concluídos.", _PARAMS),
    _tool("ticket_medio", "Ticket médio: receita dividida pelo número de pedidos concluídos.", _PARAMS),
    _tool("clientes_unicos", "Número de clientes distintos com pedidos concluídos.", _PARAMS),
    _tool("receita_media_por_cliente", "Receita média por cliente: receita total dividida pelos clientes únicos.", _PARAMS),
    _tool("taxa_cancelamento", "Percentual de pedidos cancelados sobre todos os pedidos.", ["categoria"]),
    _tool("top_cidades", "As cinco cidades com maior receita de pedidos concluídos.", ["categoria"]),
]

_FUNCS = {
    "receita_total": m.receita_total, "total_pedidos": m.total_pedidos,
    "ticket_medio": m.ticket_medio, "clientes_unicos": m.clientes_unicos,
    "receita_media_por_cliente": m.receita_media_por_cliente,
    "taxa_cancelamento": m.taxa_cancelamento,
    "top_cidades": lambda df, categoria=None: m.top_cidades(df, categoria).to_dict("records"),
}


def executar(nome: str, argumentos: dict, df) -> str:
    if nome not in _FUNCS:
        return json.dumps({"erro": f"ferramenta desconhecida: {nome}"})
    try:
        return json.dumps({"resultado": _FUNCS[nome](df, **argumentos)}, ensure_ascii=False)
    except Exception as e:  # devolve o erro ao modelo em vez de quebrar o app
        return json.dumps({"erro": str(e)})
