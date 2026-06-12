from datetime import datetime
import pandas as pd


ALL_CATEGORIES = [
    "Alimentação",
    "Transportes",
    "Lazer",
    "Estudos",
    "Saude",
    "Outros"
]

EXPENSE_KINDS = [
    "Necessária",
    "Opcional",
    "Impulsiva"
]

FREQUENCIES = [
    "Semanal",
    "Mensal",
    "Anual"
]


def safe_numeric_series(df, column_name):
    if df is None or df.empty or column_name not in df.columns:
        return pd.Series(dtype="float64")
    return pd.to_numeric(df[column_name], errors="coerce").fillna(0.0)


def calculate_summary(incomes_df, expenses_df):
    total_incomes = float(safe_numeric_series(incomes_df, "amount").sum())
    total_expenses = float(safe_numeric_series(expenses_df, "amount").sum())
    balance = total_incomes - total_expenses
    return total_incomes, total_expenses, balance


def monthly_savings(incomes_df, expenses_df):
    current_month = datetime.today().strftime("%Y-%m")
    month_incomes = 0.0
    month_expenses = 0.0

    if incomes_df is not None and not incomes_df.empty:
        temp = incomes_df.copy()
        if "income_date" in temp.columns and "amount" in temp.columns:
            temp["income_date"] = temp["income_date"].astype(str)
            temp["amount"] = pd.to_numeric(temp["amount"], errors="coerce").fillna(0.0)
            month_incomes = float(temp[temp["income_date"].str.startswith(current_month)]["amount"].sum())

    if expenses_df is not None and not expenses_df.empty:
        temp = expenses_df.copy()
        if "expense_date" in temp.columns and "amount" in temp.columns:
            temp["expense_date"] = temp["expense_date"].astype(str)
            temp["amount"] = pd.to_numeric(temp["amount"], errors="coerce").fillna(0.0)
            month_expenses = float(temp[temp["expense_date"].str.startswith(current_month)]["amount"].sum())

    return month_incomes - month_expenses


def active_goal_info(goals_df):
    if goals_df is None or goals_df.empty:
        return "Sem meta", 0
    goal = goals_df.iloc[0]
    title = str(goal.get("title", "Sem meta"))
    target = pd.to_numeric(pd.Series([goal.get("target_amount", 0)]), errors="coerce").fillna(0.0).iloc[0]
    saved = pd.to_numeric(pd.Series([goal.get("saved_amount", 0)]), errors="coerce").fillna(0.0).iloc[0]
    if target <= 0:
        return title, 0
    percent = int(min(100, round((saved / target) * 100)))
    return title, percent


def financial_status(balance):
    if balance > 0:
        return "positivo", "Tens um saldo positivo. Continua assim."
    if balance < 0:
        return "negativo", "Estás em saldo negativo. Convém rever as despesas."
    return "neutro", "O teu saldo está equilibrado neste momento."


def financial_message(balance):
    status, text = financial_status(balance)
    if status == "positivo":
        return "success", text
    if status == "negativo":
        return "error", text
    return "info", text


def sidebar_user():
    import streamlit as st
    if st.session_state.get("logged_in"):
        st.sidebar.success(f"Sessão iniciada: {st.session_state.username}")
        if st.sidebar.button("Terminar sessão"):
            from auth import logout_user
            logout_user()
            st.rerun()


def category_breakdown(expenses_df):
    if expenses_df is None or expenses_df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    temp_df = expenses_df.copy()
    if "category" not in temp_df.columns or "amount" not in temp_df.columns:
        return pd.DataFrame(columns=["category", "amount"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"], errors="coerce").fillna(0.0)
    return (
        temp_df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def kind_breakdown(expenses_df):
    if expenses_df is None or expenses_df.empty:
        return pd.DataFrame(columns=["kind", "amount"])
    temp_df = expenses_df.copy()
    if "kind" not in temp_df.columns or "amount" not in temp_df.columns:
        return pd.DataFrame(columns=["kind", "amount"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"], errors="coerce").fillna(0.0)
    return (
        temp_df.groupby("kind", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )