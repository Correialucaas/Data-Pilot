"""Limpa data/sales.csv e salva data/sales_clean.csv (sep=';', decimal=',')."""
import unicodedata
import pandas as pd

RAW = "data/sales.csv"
CLEAN = "data/sales_clean.csv"


def normalizar_status(valor: str) -> str:
    texto = unicodedata.normalize("NFKD", str(valor).strip().lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def preparar() -> pd.DataFrame:
    df = pd.read_csv(RAW)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["status"] = df["status"].map(normalizar_status)
    df = df.dropna(subset=["order_date"]).drop_duplicates()
    df["revenue"] = df["quantity"] * df["unit_price"]
    df.to_csv(CLEAN, index=False, sep=";", decimal=",")
    return df


if __name__ == "__main__":
    d = preparar()
    print(f"{len(d)} linhas limpas | status: {d['status'].value_counts().to_dict()}")
