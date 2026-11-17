# Data-Pilot

data-pilot
Painel de vendas em Python que também conversa: você pergunta em português e um agente de IA responde com as métricas que o código calculou. Regra central: o Python calcula, a IA só explica — o modelo escolhe uma ferramenta, o app executa e o modelo traduz o resultado em texto, sem inventar número.

Dados
data/sales.csv é uma planilha de vendas fictícia (800 pedidos de 2025, 4 categorias, 7 cidades), gerada por src/generate_sample_data.py com sujeira proposital: status em formatos diferentes ("Concluído", "concluido", " CONCLUÍDO ") e 15 linhas duplicadas. Para usar dados reais, substitua o sales.csv mantendo as colunas order_id, order_date, customer_id, city, category, product, quantity, unit_price, status.

Como rodar
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # edite e coloque sua chave do OpenRouter
python -m src.prepare_data  # gera data/sales_clean.csv
streamlit run app.py        # use streamlit run, não python app.py
Chave gratuita em https://openrouter.ai. No .env: OPENROUTER_API_KEY e OPENROUTER_MODEL=openrouter/free. Se trocar de modelo, confirme que ele suporta chamada de ferramentas.

Estrutura
app.py — Streamlit com dois menus: Painel e Conversa com os dados
src/prepare_data.py — limpeza com pandas (datas, status, duplicados, coluna revenue); salva com ; e vírgula decimal
src/metrics.py — uma função por pergunta de negócio
src/tools.py — descrição das ferramentas (nome, descrição, parâmetros) e execução pelo nome
src/chat.py — chamada ao OpenRouter com laço de ferramentas e novas tentativas
src/generate_sample_data.py — gera os dados de exemplo
Ferramentas do modelo
Todas calculam sobre pedidos concluídos, exceto a taxa de cancelamento (olha todos os pedidos).

Ferramenta	Parâmetros
receita_total	categoria, data_inicio, data_fim
total_pedidos	categoria, data_inicio, data_fim
ticket_medio	categoria, data_inicio, data_fim
clientes_unicos	categoria, data_inicio, data_fim
receita_media_por_cliente	categoria, data_inicio, data_fim
taxa_cancelamento	categoria
top_cidades	categoria
Melhorias escolhidas
Métrica nova: receita média por cliente, no painel e como ferramenta do chat.
Gráfico novo: top 5 cidades por receita.
Parâmetro de período (data_inicio/data_fim) nas ferramentas, para perguntas como "qual a receita entre março e maio?".
Conferência
Com os dados de exemplo, painel e chat mostram os mesmos valores (receita total R$ 303.130,00; 651 pedidos; ticket médio R$ 465,64), pois usam as mesmas funções de src/metrics.py.
