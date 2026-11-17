"""Gera data/sales.csv: planilha de vendas ficticia, propositalmente 'suja'."""
import random
from pathlib import Path
import pandas as pd

random.seed(42)
cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre", "Salvador", "Recife"]
catalogo = {
    "Eletrônicos": [("Fone Bluetooth", 180), ("Smartwatch", 450), ("Caixa de Som", 220)],
    "Moda": [("Camiseta", 60), ("Tênis", 250), ("Jaqueta", 320)],
    "Casa": [("Panela", 130), ("Luminária", 90), ("Cafeteira", 280)],
    "Livros": [("Romance", 45), ("Técnico", 110), ("HQ", 38)],
}
status_sujos = (["Concluído"] * 12 + ["concluido"] * 4 + [" CONCLUÍDO "] * 2
                + ["Cancelado"] * 2 + ["cancelado"] + ["Pendente"])
rows = []
for i in range(1, 801):
    cat = random.choice(list(catalogo))
    prod, preco = random.choice(catalogo[cat])
    rows.append({
        "order_id": 1000 + i,
        "order_date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=random.randint(0, 364)),
        "customer_id": f"C{random.randint(1, 180):03d}",
        "city": random.choice(cidades),
        "category": cat,
        "product": prod,
        "quantity": random.randint(1, 4),
        "unit_price": preco,
        "status": random.choice(status_sujos),
    })
df = pd.DataFrame(rows)
df = pd.concat([df, df.sample(15, random_state=1)])  # duplicados
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
Path("data").mkdir(exist_ok=True)
df.to_csv("data/sales.csv", index=False)
print(f"{len(df)} linhas geradas em data/sales.csv")
