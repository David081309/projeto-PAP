import streamlit as st
from auth import require_login, sidebar_user
from db import get_incomes, get_expenses
from utils import calculate_summary

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

require_login()
sidebar_user()

st.title("📊 Dashboard")

user_id = st.session_state.user_id
incomes_df = get_incomes(user_id)
expenses_df = get_expenses(user_id)

total_incomes, total_expenses, balance = calculate_summary(incomes_df, expenses_df)

c1, c2, c3 = st.columns(3)
c1.metric("Total de receitas", f"{total_incomes:.2f} €")
c2.metric("Total de despesas", f"{total_expenses:.2f} €")
c3.metric("Saldo atual", f"{balance:.2f} €")

st.divider()

if not expenses_df.empty:
    st.subheader("Despesas por categoria")
    category_df = expenses_df.groupby("category")["amount"].sum().reset_index()
    st.bar_chart(category_df.set_index("category"))

    st.subheader("Despesas por tipo")
    kind_df = expenses_df.groupby("kind")["amount"].sum().reset_index()
    st.dataframe(kind_df, use_container_width=True)
else:
    st.info("Ainda não existem despesas suficientes para análise.")
