import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from dash import Dash, dcc, html

# Ler o arquivo CSV
df = pd.read_csv("ecommerce_estatistica.csv")

# Inicializar o app Dash
app = Dash(__name__)
app.title = "Dashboard E-commerce"

# --- Gerar gráficos ---

# 1. Histograma
hist_fig = px.histogram(df, x="Nota", nbins=20, title="Histograma das Notas dos Produtos")

# 2. Dispersão: Desconto vs Nota
disp_fig = px.scatter(df, x="Desconto", y="Nota", color="Gênero", title="Dispersão: Desconto vs Nota")

# 3. Mapa de calor (com seaborn salvo como imagem base64)
correlation = df.select_dtypes(include=["float64", "int64"]).corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
buf = io.BytesIO()
plt.savefig(buf, format="png")
plt.close(fig)
buf.seek(0)
heatmap_base64 = base64.b64encode(buf.read()).decode('utf-8')

# 4. Barra: Marcas mais comuns
top_marcas = df['Marca'].value_counts().nlargest(10)
bar_fig = px.bar(x=top_marcas.values, y=top_marcas.index, orientation='h',
                 title="Top 10 Marcas mais Frequentes", labels={'x':'Quantidade', 'y':'Marca'})

# 5. Pizza: Gênero
genero_count = df['Gênero'].value_counts()
pie_fig = px.pie(values=genero_count.values, names=genero_count.index, title="Distribuição por Gênero")

# 6. Densidade: Nota
density_fig = ff.create_distplot([df['Nota'].dropna()], ['Nota'], show_hist=False)
density_fig.update_layout(title="Densidade da Nota dos Produtos")

# 7. Regressão: N_Avaliações vs Nota
reg_fig = px.scatter(df, x="N_Avaliações", y="Nota", trendline="ols", title="Regressão: N° de Avaliações vs Nota")

# --- Layout ---
app.layout = html.Div([
    html.H1("Análise Estatística de E-commerce", style={'textAlign': 'center'}),

    dcc.Graph(figure=hist_fig),
    dcc.Graph(figure=disp_fig),

    html.H3("Mapa de Calor das Correlações"),
    html.Img(src="data:image/png;base64,{}".format(heatmap_base64), style={"width": "100%", "maxWidth": "800px"}),

    dcc.Graph(figure=bar_fig),
    dcc.Graph(figure=pie_fig),
    dcc.Graph(figure=density_fig),
    dcc.Graph(figure=reg_fig),
])

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)

