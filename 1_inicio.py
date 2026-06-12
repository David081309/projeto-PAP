import streamlit as st
from auth import require_login, sidebar_user
from db import get_incomes, get_expenses, get_goals
from utils import calculate_summary, financial_message, monthly_savings, active_goal_info

st.set_page_config(page_title="Início", page_icon="🏠", layout="wide")

require_login()
sidebar_user()

st.title("🏠 Início")

user_id = st.session_state.user_id
incomes_df = get_incomes(user_id)
expenses_df = get_expenses(user_id)
goals_df = get_goals(user_id)

total_incomes, total_expenses, balance = calculate_summary(incomes_df, expenses_df)
month_save = monthly_savings(incomes_df, expenses_df)
goal_title, goal_percent = active_goal_info(goals_df)

col1, col2, col3 = st.columns(3)
col1.metric("Receitas", f"{total_incomes:.2f} €")
col2.metric("Despesas", f"{total_expenses:.2f} €")
col3.metric("Saldo", f"{balance:.2f} €")

st.divider()

msg_type, msg_text = financial_message(balance)

if msg_type == "success":
    st.success(msg_text)
elif msg_type == "error":
    st.error(msg_text)
else:
    st.info(msg_text)
