import streamlit as st
from db import create_user, get_user


def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None


def require_login():
    init_session()
    if not st.session_state.logged_in:
        st.warning("Tens de iniciar sessão primeiro.")
        st.stop()


def sidebar_user():
    if st.session_state.logged_in:
        st.sidebar.success(f"Sessão iniciada: {st.session_state.username}")
        if st.sidebar.button("Terminar sessão"):
            logout_user()
            st.rerun()


def login_user(username, password):
    username = username.strip()
    if not username or not password:
        return False, "Preenche o utilizador e a palavra-passe."
    user = get_user(username, password)
    if user is None:
        return False, "Credenciais inválidas."
    st.session_state.logged_in = True
    st.session_state.user_id = user[0]
    st.session_state.username = user[1]
    return True, "Login efetuado com sucesso."


def logout_user():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None


def register_user(username, password, confirm_password):
    username = username.strip()
    if not username or not password or not confirm_password:
        return False, "Preenche todos os campos."
    if password != confirm_password:
        return False, "As palavras-passe não coincidem."
    if len(password) < 4:
        return False, "A palavra-passe deve ter pelo menos 4 caracteres."
    created = create_user(username, password)
    if not created:
        return False, "Esse nome de utilizador já existe."
    return True, "Conta criada com sucesso."
