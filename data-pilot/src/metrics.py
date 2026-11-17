"""Metricas: uma funcao por pergunta de negocio. O Python calcula, a IA so explica."""
import pandas as pd

CLEAN = "data/sales_clean.csv"
CONCLUIDO = "concluido"


def carregar(path: str = CLEAN) -> pd.DataFrame:
    return pd.read_csv(path, sep=";", decimal=",", parse_dates=["order_date"])


def _concluidos(df, categoria=None, data_inicio=None, data_fim=None):
    d = df[df["status"] == CONCLUIDO]
    if categoria and categoria != "Todas":
        d = d[d["category"] == categoria]
    if data_inicio:
        d = d[d["order_date"] >= pd.to_datetime(data_inicio)]
    if data_fim:
        d = d[d["order_date"] <= pd.to_datetime(data_fim)]
    return d


def receita_total(df, categoria=None, data_inicio=None, data_fim=None) -> float:
    return round(float(_concluidos(df, categoria, data_inicio, data_fim)["revenue"].sum()), 2)


def total_pedidos(df, categoria=None, data_inicio=None, data_fim=None) -> int:
    return int(_concluidos(df, categoria, data_inicio, data_fim)["order_id"].nunique())


def ticket_medio(df, categoria=None, data_inicio=None, data_fim=None) -> float:
    n = total_pedidos(df, categoria, data_inicio, data_fim)
    return round(receita_total(df, categoria, data_inicio, data_fim) / n, 2) if n else 0.0


def clientes_unicos(df, categoria=None, data_inicio=None, data_fim=None) -> int:
    return int(_concluidos(df, categoria, data_inicio, data_fim)["customer_id"].nunique())


def taxa_cancelamento(df, categoria=None) -> float:
    """Unica metrica que olha TODOS os pedidos (percentual)."""
    d = df if not categoria or categoria == "Todas" else df[df["category"] == categoria]
    return round(float((d["status"] == "cancelado").mean() * 100), 2) if len(d) else 0.0


# --- Melhoria escolhida: receita media por cliente + top cidades + periodo ---
def receita_media_por_cliente(df, categoria=None, data_inicio=None, data_fim=None) -> float:
    n = clientes_unicos(df, categoria, data_inicio, data_fim)
    return round(receita_total(df, categoria, data_inicio, data_fim) / n, 2) if n else 0.0


def receita_por_mes(df, categoria=None) -> pd.DataFrame:
    d = _concluidos(df, categoria)
    out = d.groupby(d["order_date"].dt.to_period("M").astype(str))["revenue"].sum().reset_index()
    return out.rename(columns={"order_date": "mes", "revenue": "receita"})


def top_cidades(df, categoria=None, n: int = 5) -> pd.DataFrame:
    d = _concluidos(df, categoria)
    out = d.groupby("city")["revenue"].sum().nlargest(n).reset_index()
    return out.rename(columns={"city": "cidade", "revenue": "receita"})
