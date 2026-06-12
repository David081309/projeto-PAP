import streamlit as st
from auth import require_login, sidebar_user
from db import get_incomes, get_expenses, get_goals
from utils import calculate_summary


def simulate_cut(current_expenses, cut_amount):
    return max(0.0, float(current_expenses) - float(cut_amount))


def simulate_new_savings(balance, extra_saving):
    return float(balance) + float(extra_saving)


def months_to_goal(saved_amount, target_amount, monthly_contribution):
    saved_amount = float(saved_amount)
    target_amount = float(target_amount)
    monthly_contribution = float(monthly_contribution)
    if monthly_contribution <= 0:
        return None
    remaining = max(0.0, target_amount - saved_amount)
    months = int((remaining / monthly_contribution) + (1 if remaining % monthly_contribution > 0 else 0))
    return months


st.set_page_config(page_title="Simulador", page_icon="🧮", layout="wide")

require_login()
sidebar_user()

st.title("🧮 Simulador")

user_id = st.session_state.user_id
incomes_df = get_incomes(user_id)
expenses_df = get_expenses(user_id)
goals_df = get_goals(user_id)

total_incomes, total_expenses, balance = calculate_summary(incomes_df, expenses_df)

st.subheader("Simular corte de despesas")
cut_amount = st.number_input("Quanto queres cortar nas despesas? (€)", min_value=0.0, format="%.2f")
if cut_amount > 0:
    new_expenses = simulate_cut(total_expenses, cut_amount)
    new_balance = total_incomes - new_expenses
    st.info(f"Com um corte de {cut_amount:.2f}€, as tuas despesas passariam para {new_expenses:.2f}€ e o saldo para {new_balance:.2f}€.")

st.divider()
st.subheader("Tempo para atingir uma meta")

if not goals_df.empty:
    goal = goals_df.iloc[0]
    target = float(goal["target_amount"])
    saved = float(goal["saved_amount"])
    st.write(f"Meta ativa: **{goal['title']}** — {saved:.2f}€ de {target:.2f}€ poupados.")
    monthly_contribution = st.number_input("Quanto consegues poupar por mês? (€)", min_value=0.0, format="%.2f")
    if monthly_contribution > 0:
        months = months_to_goal(saved, target, monthly_contribution)
        if months is not None:
            st.success(f"Com {monthly_contribution:.2f}€/mês, atinges a meta em {months} mês(es).")
        else:
            st.warning("Contribuição mensal inválida.")
else:
    st.info("Não tens metas registadas. Vai à página de Metas para criar uma.")
