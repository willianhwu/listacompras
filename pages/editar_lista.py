import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Editar Lista", page_icon="✏️")

if "lista_nome" not in st.session_state:
    st.error("Nenhuma lista carregada. Volte para a página inicial.")
    st.stop()

lista_nome = st.session_state["lista_nome"]
filename = f"{lista_nome}.csv"

if os.path.exists(filename):
    df = pd.read_csv(filename)
else:
    df = pd.DataFrame(columns=["Item", "Quantidade", "Comprado"])

st.title(f"✏️ Editar Lista: {lista_nome}")

# Formulário para adicionar ou substituir item
with st.form("add_item_form"):
    item = st.text_input("Item").strip().title()
    qtd = st.number_input("Quantidade", min_value=1, step=1)
    submitted = st.form_submit_button("Adicionar / Substituir")

    if submitted and item:
        existing = df["Item"].str.strip().str.lower() == item.lower()
        
        if existing.any():
            idx = df[existing].index[0]
            df.at[idx, "Quantidade"] = qtd
            df.at[idx, "Comprado"] = False
            st.info(f"Item '{item}' atualizado.")
        else:
            df.loc[len(df)] = [item, qtd, False]
            st.success(f"Item '{item}' adicionado.")
        
        df.to_csv(filename, index=False)
        st.rerun()

# Mostrar tabela com botão de excluir item
st.subheader("🗑️ Remover itens")

for i, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    with col1:
        st.markdown(f"**{row['Item']}**")
    with col2:
        st.markdown(f"Qtd: {row['Quantidade']}")
    with col3:
        st.markdown("✅" if row["Comprado"] else "❌")
    with col4:
        if st.button("Excluir", key=f"del_{i}"):
            df.drop(index=i, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.to_csv(filename, index=False)
            st.success(f"Item '{row['Item']}' removido com sucesso!")
            st.rerun()
