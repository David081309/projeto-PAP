import streamlit as st
from auth import require_login, sidebar_user
from db import get_incomes, get_expenses, get_goals
from utils import calculate_summary


st.set_page_config(page_title="Alertas", page_icon="🔔", layout="wide")

require_login()
sidebar_user()

st.title("🔔 Alertas")

user_id     = st.session_state.user_id
incomes_df  = get_incomes(user_id)
expenses_df = get_expenses(user_id)
goals_df    = get_goals(user_id)

total_incomes, total_expenses, balance = calculate_summary(incomes_df, expenses_df)

# Despesas recorrentes filtradas da tabela unificada
recurring_df = expenses_df[expenses_df["is_recurring"] == 1] if not expenses_df.empty else expenses_df


# ── Geração de alertas ────────────────────────────────────────────────────────

def generate_alerts(total_incomes, total_expenses, balance, goals_df, recurring_df):
    alerts = []

    if balance < 0:
        alerts.append(("warning", "O teu saldo atual está negativo."))

    if total_incomes > 0 and total_expenses > total_incomes * 0.8:
        alerts.append(("warning", "As tuas despesas já ultrapassam 80% das receitas."))

    if goals_df is not None and not goals_df.empty:
        goal   = goals_df.iloc[0]
        target = float(goal.get("target_amount", 0) or 0)
        saved  = float(goal.get("saved_amount", 0) or 0)
        if target > 0 and saved < target * 0.25:
            alerts.append(("warning", "A tua meta ativa ainda está com pouco progresso."))

    if recurring_df is not None and not recurring_df.empty:
        alerts.append(("info", f"Tens {len(recurring_df)} despesa(s) recorrente(s) ativa(s)."))

    if not alerts:
        alerts.append(("success", "Não existem alertas críticos neste momento. ✅"))

    return alerts


alerts = generate_alerts(total_incomes, total_expenses, balance, goals_df, recurring_df)

for kind, message in alerts:
    if kind == "warning":
        st.warning(message)
    elif kind == "success":
        st.success(message)
    else:
        st.info(message)