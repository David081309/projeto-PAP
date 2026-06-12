import streamlit as st
from db import init_db, get_incomes, get_expenses, get_goals
from auth import init_session, login_user, register_user, logout_user
from utils import calculate_summary, monthly_savings, active_goal_info

st.set_page_config(
    page_title="Orçamento Jovem",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
init_session()

st.title("💸 Orçamento Jovem")
st.caption("Gestão orçamental e educação financeira para jovens")

balance = 0.0
month_save = 0.0
goal_title = "Sem meta"
goal_percent = 0

if st.session_state.logged_in:
    st.success(f"Sessão iniciada como {st.session_state.username}")
    st.info("Usa o menu lateral para navegar pelas páginas.")

    user_id = st.session_state.user_id
    incomes_df = get_incomes(user_id)
    expenses_df = get_expenses(user_id)
    goals_df = get_goals(user_id)

    total_incomes, total_expenses, balance = calculate_summary(incomes_df, expenses_df)
    month_save = monthly_savings(incomes_df, expenses_df)
    if month_save is None:
        month_save = 0.0
    goal_title, goal_percent = active_goal_info(goals_df)

    if st.button("Terminar sessão"):
        logout_user()
        st.rerun()

else:
    tab1, tab2 = st.tabs(["Login", "Registo"])

    with tab1:
        st.subheader("Entrar")
        with st.form("login_form"):
            username = st.text_input("Nome do utilizador")
            password = st.text_input("Palavra-passe", type="password")
            login_btn = st.form_submit_button("Entrar")

            if login_btn:
                if not username or not password:
                    st.warning("Preenche todos os campos.")
                else:
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    with tab2:
        st.subheader("Criar conta")
        with st.form("register_form"):
            new_username = st.text_input("Novo nome de utilizador")
            new_password = st.text_input("Nova palavra-passe", type="password")
            confirm_password = st.text_input("Confirmar palavra-passe", type="password")
            register_btn = st.form_submit_button("Criar conta")

            if register_btn:
                success, message = register_user(new_username, new_password, confirm_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

with st.container():
    col1, col2 = st.columns([1.4, 1], gap="large")
    with col1:
        st.subheader("Controla melhor o teu dinheiro, passo a passo")
        st.write(
            "Esta base foi pensada para servir como ponto de partida do teu projeto PAP. "
            "O objetivo é criar uma app simples, moderna e educativa para ajudar jovens a "
            "registar despesas, acompanhar metas e aprender a tomar melhores decisões financeiras."
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Saldo atual", f"{balance:.2f} €")
        c2.metric("Poupança do mês", f"{month_save:.2f} €")
        c3.metric("Meta ativa", f"{goal_percent}%")

    with col2:
        st.info(
            "Nesta versão base tens apenas a estrutura visual principal. "
            "As funcionalidades podem ser desenvolvidas aos poucos para poderes evoluir como programador."
        )
        st.success("Ideal para começares já e ires melhorando módulo a módulo.")

st.divider()

st.subheader("Áreas principais")
col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    st.markdown("### Dashboard")
    st.write("Resumo mensal com saldo, receitas, despesas e alertas principais.")

with col2:
    st.markdown("### Registos")
    st.write("Página para inserir receitas e despesas de forma simples e organizada.")

with col3:
    st.markdown("### Metas")
    st.write("Acompanhamento de objetivos de poupança e fundo de emergência.")

with col4:
    st.markdown("### Educação")
    st.write("Conceitos de educação financeira explicados de forma prática para jovens.")

st.divider()

left, right = st.columns([1.2, 1], gap="large")
with left:
    st.subheader("O que já podes fazer com esta base")
    st.write("- Mostrar uma homepage mais profissional")
    st.write("- Organizar o projeto em páginas")
    st.write("- Preparar o crescimento da app sem complicar demasiado")
    st.write("- Ir adicionando funcionalidades conforme fores aprendendo")

with right:
    st.subheader("Próximos módulos a desenvolver")
    st.write("1. Ligação à base de dados")
    st.write("2. Registo real de receitas e despesas")
    st.write("3. Cálculo automático do saldo")
    st.write("4. Metas e fundo de emergência")
    st.write("5. Alertas e sugestões educativas")
