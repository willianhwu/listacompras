import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Comprar", page_icon="✅")

if "lista_nome" not in st.session_state:
    st.error("Nenhuma lista carregada. Volte para a página inicial.")
    st.stop()

lista_nome = st.session_state["lista_nome"]
filename = f"{lista_nome}.csv"

if not os.path.exists(filename):
    st.error("Arquivo da lista não encontrado.")
    st.stop()

df = pd.read_csv(filename)

st.title(f"✅ Lista de Compras: {lista_nome}")

# Interface de checkboxes
for i, row in df.iterrows():
    checked = st.checkbox(f"{row['Item']} ({row['Quantidade']})", value=row["Comprado"], key=i)
    df.at[i, "Comprado"] = checked

# Botão para salvar alterações
if st.button("Salvar alterações"):
    df.to_csv(filename, index=False)
    st.success("Alterações salvas com sucesso!")
