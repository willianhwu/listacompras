import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="LISTA COMPRAS - INICIO", page_icon="🛒")
st.title("🛒 Lista de Compras")

# Diretório dos arquivos
lista_dir = "."
listas_existentes = [f[:-4] for f in os.listdir(lista_dir) if f.endswith(".csv")]

# Controle da exclusão
if "confirmar_exclusao" not in st.session_state:
    st.session_state.confirmar_exclusao = False

# Interface principal
opcao = st.radio("Escolha uma opção:", ["Selecionar lista existente", "Criar nova lista"])

if opcao == "Selecionar lista existente":
    if listas_existentes:
        lista_selecionada = st.selectbox("Selecione a lista:", listas_existentes)
        if lista_selecionada:
            st.session_state["lista_nome"] = lista_selecionada
            st.success(f"Lista '{lista_selecionada}' carregada!")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✏️ Editar Lista"):
                    st.switch_page("pages/editar_lista.py")
            with col2:
                if st.button("✅ Marcar Compras"):
                    st.switch_page("pages/comprar.py")
            with col3:
                if st.button("🗑️ Excluir Lista"):
                    st.session_state.confirmar_exclusao = True

            # Confirmação de exclusão com formulário
            if st.session_state.confirmar_exclusao:
                with st.form("confirmar_exclusao_form"):
                    st.warning(f"Tem certeza que deseja excluir a lista **{lista_selecionada}**? Esta ação não pode ser desfeita.")
                    col_conf, col_cancel = st.columns(2)
                    with col_conf:
                        confirmar = st.form_submit_button("✔️ Confirmar Exclusão")
                    with col_cancel:
                        cancelar = st.form_submit_button("❌ Cancelar")

                    if confirmar:
                        filename = os.path.join(lista_dir, f"{lista_selecionada}.csv")
                        os.remove(filename)
                        st.success(f"Lista '{lista_selecionada}' excluída com sucesso!")
                        del st.session_state["lista_nome"]
                        st.session_state.confirmar_exclusao = False
                        st.rerun()
                    elif cancelar:
                        st.session_state.confirmar_exclusao = False
                        st.rerun()
    else:
        st.info("Nenhuma lista encontrada. Crie uma nova.")

# Criar nova lista
else:
    nova_lista = st.text_input("Digite o nome da nova lista")
    if nova_lista:
        filename = os.path.join(lista_dir, f"{nova_lista}.csv")
        if os.path.exists(filename):
            st.warning("Essa lista já existe! Escolha outro nome ou use a opção de selecionar.")
        else:
            df = pd.DataFrame(columns=["Item", "Quantidade", "Comprado"])
            df.to_csv(filename, index=False)
            st.session_state["lista_nome"] = nova_lista
            st.success(f"Lista '{nova_lista}' criada com sucesso!")
            if st.button("Ir para edição"):
                st.switch_page("pages/editar_lista.py")
