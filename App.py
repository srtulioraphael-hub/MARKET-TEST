import streamlit as st  
import pandas as pd  
  
# Configuração simples de estado (simulando um banco de dados)  
if 'estoque' not in st.session_state:  
    st.session_state.estoque = pd.DataFrame(columns=['ID', 'Produto', 'Preço', 'Qtd'])  
if 'vendas' not in st.session_state:  
    st.session_state.vendas = []  
  
st.title("🛒 Mini Mercado Pro")  
  
menu = ["PDV (Vendas)", "Estoque", "Relatórios"]  
escolha = st.sidebar.selectbox("Menu", menu)  
  
# ================= ESTOQUE =================  
if escolha == "Estoque":  
    st.subheader("Gerenciar Produtos")  
  
    with st.form("add_form"):  
        nome = st.text_input("Nome do Produto")  
        preco = st.number_input("Preço de Venda", min_value=0.0)  
        qtd = st.number_input("Quantidade Inicial", min_value=0)  
        submit = st.form_submit_button("Cadastrar")  
          
        if submit:  
            novo_item = pd.DataFrame(  
                [[len(st.session_state.estoque) + 1, nome, preco, qtd]],  
                columns=['ID', 'Produto', 'Preço', 'Qtd']  
            )  
            st.session_state.estoque = pd.concat(  
                [st.session_state.estoque, novo_item], ignore_index=True  
            )  
            st.success("Produto cadastrado!")  
  
    st.write(st.session_state.estoque)  
  
# ================= PDV =================  
elif escolha == "PDV (Vendas)":  
    st.subheader("Nova Venda")  
  
    if not st.session_state.estoque.empty:  
        produto_sel = st.selectbox(  
            "Selecione o produto",  
            st.session_state.estoque['Produto']  
        )  
        qtd_venda = st.number_input("Quantidade", min_value=1)  
  
        if st.button("Finalizar Venda"):  
            idx = st.session_state.estoque[  
                st.session_state.estoque['Produto'] == produto_sel  
            ].index[0]  
  
            estoque_atual = st.session_state.estoque.at[idx, 'Qtd']  
            preco_produto = st.session_state.estoque.at[idx, 'Preço']  
  
            if qtd_venda > estoque_atual:  
                st.error("Quantidade maior que o estoque disponível!")  
            else:  
                st.session_state.estoque.at[idx, 'Qtd'] -= qtd_venda  
                total = qtd_venda * preco_produto  
  
                st.session_state.vendas.append({  
                    "Produto": produto_sel,  
                    "Qtd": qtd_venda,  
                    "Preço": preco_produto,  
                    "Total": total  
                })  
  
                st.success(f"Venda de {qtd_venda}x {produto_sel} realizada!")  
                st.info(f"Total: R$ {total:.2f}")  
    else:  
        st.warning("Cadastre produtos no estoque primeiro.")  
  
# ================= RELATÓRIOS =================  
elif escolha == "Relatórios":  
    st.subheader("Relatório de Vendas")  
  
    if st.session_state.vendas:  
        df_vendas = pd.DataFrame(st.session_state.vendas)  
        st.write(df_vendas)  
  
        total_faturado = df_vendas['Total'].sum()  
        st.metric("💰 Faturamento Total", f"R$ {total_faturado:.2f}")  
    else:  
        st.info("Nenhuma venda registrada ainda.")  
