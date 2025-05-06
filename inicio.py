import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="LISTA COMPRAS - INICIO",
    page_icon="🛒"
)

st.title("🛒 Lista de Compras")

# Mostra nome da lista já carregada, se houver
if "lista_nome" in st.session_state:
    st.markdown(f"✅ Lista carregada: **{st.session_state['lista_nome']}**")

# Entrada do nome da lista
lista_nome = st.text_input("Digite o nome da lista de compras")

if lista_nome:
    st.session_state["lista_nome"] = lista_nome  # <- salva logo que digita



if lista_nome:
    filename = f"{lista_nome}.csv"

    # Cria ou carrega a lista
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=["Item", "Quantidade", "Comprado"])
        df.to_csv(filename, index=False)
        st.success(f"Nova lista '{lista_nome}' criada!")
    else:
        st.success(f"Lista '{lista_nome}' carregada com sucesso!")

    # Salvar o nome da lista na sessão
    st.session_state["lista_nome"] = lista_nome

    # Botão para ir à página de edição
    if st.button("Editar Lista"):
        st.switch_page("pages/editar_lista.py")
