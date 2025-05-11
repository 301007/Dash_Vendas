import pandas as pd
import plotly.express as px
import streamlit as st 

# Lendo as bases de dados:
df_vendas = pd.read_excel('Vendas.xlsx')
df_produtos = pd.read_excel('Produtos.xlsx')

# Merge:
df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto')

# Criando a colunas:
df['Total Custo'] = df['Custo Unitário'] * df['Quantidade']
df['Lucro'] = df['Valor Venda'] - df['Total Custo']
df['Mês-Ano'] = df['Data Venda'].dt.to_period('M').astype(str)

# Agrupamentos:
produtos_vendidos_marca = df.groupby('Marca')['Quantidade'].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby('Categoria')['Lucro'].sum().reset_index()
lucro_mes_categoria = df.groupby(['Mês-Ano', 'Categoria'])['Lucro'].sum().reset_index()

def main():

    st.title('Análise de Vendas')
    st.image('vendas.png')

    import streamlit as st

def main():
    st.title('Análise de Vendas')
    st.image('vendas.png')

    # Cálculos
    total_custo_valor = df['Total Custo'].sum()
    total_lucro_valor = df['Lucro'].sum()
    total_clientes_valor = df['ID Cliente'].nunique()

    # Formatação de valores
    total_custo = f"R$ {total_custo_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    total_lucro = f"R$ {total_lucro_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    total_clientes = f"{total_clientes_valor:,}".replace(",", ".")

    # Exibição sem '...'
    st.write(f"**Lucro Total:** {total_lucro}")
    st.write(f"**Total de clientes:** {total_clientes}")
    st.write(f"**Total de Custo:** {total_custo}")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Total Custo', total_custo)

    with col2:
        st.metric('Total Lucro', total_lucro)

    with col3:
        st.metric('Total Clientes', total_clientes)

    col1, col2 = st.columns(2)

    fig = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', orientation='h',
                 title='Total Produtos x Marca', text='Quantidade', width=450, height=400)
    col1.plotly_chart(fig)

    fig2 = px.pie(lucro_categoria, values='Lucro', names='Categoria', title='Lucro x Categoria', width=450, height=400)
    col2.plotly_chart(fig2)

    fig3 = px.line(lucro_mes_categoria, x='Mês-Ano', y='Lucro', title='Lucro', color='Categoria', width=1000, height=600)
    st.plotly_chart(fig3)




if __name__ == '__main__':
    main()