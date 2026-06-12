import streamlit as st
from datetime import date
from auth import require_login, sidebar_user
from db import add_income, get_incomes, add_expense, get_expenses, delete_expense
from utils import ALL_CATEGORIES, EXPENSE_KINDS, FREQUENCIES


st.set_page_config(page_title="Registos", page_icon="💸", layout="wide")

require_login()
sidebar_user()

user_id  = st.session_state.user_id
username = st.session_state.username

st.title("💸 Registos Financeiros")
st.write("Regista receitas e despesas pontuais ou recorrentes.")
st.caption(f"Utilizador autenticado: {username}")

tab1, tab2, tab3 = st.tabs(["Receitas", "Despesas", "Histórico"])


# ── Tab 1: Receitas ───────────────────────────────────────────────────────────

with tab1:
    st.subheader("Adicionar receita")
    with st.form("income_form", clear_on_submit=True):
        description = st.text_input("Descrição da receita")
        amount      = st.number_input("Valor (€)", min_value=0.0, format="%.2f")
        income_date = st.date_input("Data", value=date.today())
        submit      = st.form_submit_button("Guardar receita")

        if submit:
            if not description.strip():
                st.error("A descrição é obrigatória.")
            elif amount <= 0:
                st.error("O valor tem de ser superior a 0.")
            else:
                add_income(user_id, description.strip(), str(amount), str(income_date))
                st.success("Receita adicionada com sucesso.")
                st.rerun()


# ── Tab 2: Despesas ───────────────────────────────────────────────────────────

with tab2:
    st.subheader("Adicionar despesa")

    # Checkbox FORA do form — reage imediatamente ao clique
    is_recurring = st.checkbox("É uma despesa recorrente?", key="is_recurring_check")

    with st.form("expense_form", clear_on_submit=True):
        description  = st.text_input("Descrição da despesa")
        category     = st.selectbox("Categoria", ALL_CATEGORIES)
        kind         = st.selectbox("Tipo de despesa", EXPENSE_KINDS)
        amount       = st.number_input("Valor (€)", min_value=0.0, format="%.2f", key="exp_amount")
        expense_date = st.date_input("Data", value=date.today(), key="exp_date")

        frequency = None
        next_date = None

        # Só aparecem se o checkbox estiver ativo
        if is_recurring:
            frequency = st.selectbox("Frequência", FREQUENCIES)
            next_date = st.date_input("Próxima data de pagamento", value=date.today())

        submit = st.form_submit_button("Guardar despesa")

        if submit:
            if not description.strip():
                st.error("A descrição é obrigatória.")
            elif amount <= 0:
                st.error("O valor tem de ser superior a 0.")
            else:
                add_expense(
                    user_id,
                    description.strip(),
                    category,
                    kind,
                    float(amount),
                    str(expense_date),
                    is_recurring=int(is_recurring),
                    frequency=frequency,
                    next_date=str(next_date) if next_date else None
                )
                st.success("Despesa adicionada com sucesso.")
                st.rerun()


# ── Tab 3: Histórico ──────────────────────────────────────────────────────────

with tab3:
    st.subheader("Histórico financeiro")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Receitas")
        incomes_df = get_incomes(user_id)
        if not incomes_df.empty:
            st.dataframe(
                incomes_df[["description", "amount", "income_date"]],
                use_container_width=True
            )
        else:
            st.info("Ainda não existem receitas registadas.")

    with col2:
        st.markdown("### Despesas")
        expenses_df = get_expenses(user_id)
        if not expenses_df.empty:
            st.dataframe(
                expenses_df[["id", "description", "category", "kind",
                             "amount", "expense_date", "is_recurring"]]
                .rename(columns={"is_recurring": "Recorrente"}),
                use_container_width=True
            )

            st.markdown("#### Eliminar despesa")
            with st.form("delete_expense_form"):
                record_id     = st.number_input("ID da despesa a eliminar", min_value=1, step=1)
                delete_submit = st.form_submit_button("Eliminar despesa")

                if delete_submit:
                    if int(record_id) not in expenses_df["id"].tolist():
                        st.error("O ID indicado não existe.")
                    else:
                        delete_expense(record_id, user_id)
                        st.success("Despesa eliminada com sucesso.")
                        st.rerun()
        else:
            st.info("Ainda não existem despesas registadas.")