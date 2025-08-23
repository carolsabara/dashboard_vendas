import streamlit as st
import pandas as pd  
import yfinance as yf  
import numpy as np 
import plotly.express as px


st.set_page_config(
    page_title= "Análise de ações",
    page_icon="📈",
    layout="wide"
)
 #faturamento por unidade
 #tipo de produto mais vendido
 #DEsempenho das forma de pagamentos 
 #Como estão as avaliações das filiais?

#carregar o arquivo 
df= pd.read_csv('supermarket_sales.csv', sep=';', decimal=',')

#transfromar a coluna de data que está em objeto para datetime
df['Date']= pd.to_datetime(df["Date"])

#ordenar o dataframe nesse caso foi pela data
df= df.sort_values('Date')

df['Month'] = df['Date'].apply(lambda x: str(x.year) + '-' + str(x.month))

month = st.sidebar.selectbox('Mês', df['Month'].unique())

#Filtrar dataframe com os meses selecionados
df_filtered = df[df['Month'] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

#criando um gráfico de barras
fig_date = px.bar(df_filtered, 
    x='Date', 
    y= 'Total',
    title='Faturamento por dia',
    labels={'Date': 'Data', 'Total': 'Total de Vendas'},
    color='City',
    barmode='stack',
    color_discrete_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#17becf"]


)

#Adicionando o gráfico de barras ao Streamlit de forma interativa
col1.plotly_chart(fig_date, use_container_width=True) 

fig_prod= px.bar(df_filtered, 
    x='Date', 
    y= 'Product line',
    title='Faturamento por tipo de produto',
    labels={'Date': 'Data', 'Total': 'Total de Vendas por Produto'},
    color='City',
    orientation='h',
    barmode='stack',
    color_discrete_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#17becf"]

)
#removendo as bordas
fig_prod.update_traces(marker_line_width=0)
col2.plotly_chart(fig_prod, use_container_width=True) 

city_total = df_filtered.groupby('City')[['Total']].sum().reset_index()
fig_city= px.bar(city_total, 
    x='City',
    y= 'Total',
    title='Faturamento por filial',
    labels={'City': 'City','Total': 'Total de Vendas'},
    color='City',
    barmode='stack',
    color_discrete_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#17becf"]
)

fig_prod.update_traces(marker_line_width=0)
col3.plotly_chart(fig_city, use_container_width=True)


fig_kind= px.pie(df_filtered, 
    values='Total',
    names= 'Payment',
    title='Faturamento por tipo de pagamento',
    labels={'Payment': 'Tipo de pagamento','Total': 'Total de Vendas'},
    color_discrete_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#17becf"]
)

col4.plotly_chart(fig_kind)

city_total = df_filtered.groupby('City')[['Rating']].mean().reset_index()
fig_rating= px.bar(city_total, 
    x='Rating',
    y= 'City',
    title='Avaliação',
    labels={'City': 'City','Rating': 'Avaliação'},
    color='City',
    barmode='stack',
    color_discrete_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#17becf"]
)

fig_rating.update_traces(marker_line_width=0)
col5.plotly_chart(fig_rating, use_container_width=True)

