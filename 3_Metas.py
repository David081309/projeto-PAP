import streamlit as st
from datetime import date
from auth import require_login, sidebar_user
from db import add_goal, get_goals

st.set_page_config(page_title="Metas", page_icon="🎯", layout="wide")

require_login()
sidebar_user()

user_id = st.session_state.user_id
username = st.session_state.username

st.title("🎯 Metas de Poupança")
st.write("Cria, acompanha e avalia o progresso das tuas metas.")
st.caption(f"Utilizador autenticado: {username}")

with st.form("goal_form", clear_on_submit=True):
    title = st.text_input("Nome da meta")
    target_amount = st.number_input("Valor objetivo", min_value=0.0, format="%.2f")
    saved_amount = st.number_input("Valor já poupado", min_value=0.0, format="%.2f")
    deadline = st.date_input("Prazo da meta", value=date.today())
    submitted = st.form_submit_button("Guardar meta")

    if submitted:
        if not title.strip():
            st.error("O nome da meta é obrigatório.")
        elif target_amount <= 0:
            st.error("O valor do objetivo tem de ser superior a 0.")
        elif saved_amount < 0:
            st.error("O valor poupado não pode ser negativo.")
        elif saved_amount > target_amount:
            st.error("O valor poupado não pode ser superior ao valor objetivo.")
        else:
            add_goal(
                user_id,
                title.strip(),
                float(target_amount),
                float(saved_amount),
                str(deadline)
            )
            st.success("Meta adicionada com sucesso.")
            st.rerun()

st.markdown("## Metas registadas")

goals_df = get_goals(user_id)

if not goals_df.empty:
    for _, goal in goals_df.iterrows():
        target = float(goal["target_amount"])
        saved = float(goal["saved_amount"])
        progress = 0.0 if target == 0 else min(saved / target, 1.0)

        st.markdown(f"### {goal['title']}")
        st.write(f"Valor objetivo: {target:.2f}€")
        st.write(f"Valor poupado: {saved:.2f}€")
        st.write(f"Prazo: {goal['deadline']}")
        st.progress(progress)

        if progress >= 1:
            st.success("Meta concluída com sucesso.")
        elif progress >= 0.75:
            st.info("Estás muito perto de concluir esta meta.")
        elif progress >= 0.40:
            st.caption("Bom progresso. Continua assim.")
        else:
            st.caption("Meta iniciada. Ainda tens margem para evoluir.")
else:
    st.info("Ainda não tens metas registadas.")
