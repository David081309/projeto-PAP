import streamlit as st

TOPICS = {
    "Necessidades vs desejos": (
        "As necessidades são gastos importantes para viver e estudar bem. "
        "Os desejos são gastos opcionais que podem esperar."
    ),
    "Fundo de emergência": (
        "Um fundo de emergência serve para cobrir imprevistos, como uma despesa médica, "
        "reparação ou outra situação urgente."
    ),
    "Compras impulsivas": (
        "Uma compra impulsiva acontece quando compras sem planeamento. "
        "O ideal é parar, pensar e avaliar se precisas mesmo daquilo."
    ),
    "Planeamento financeiro": (
        "Planear o dinheiro ajuda-te a saber quanto entra, quanto sai e quanto podes guardar."
    ),
    "Fraude financeira": (
        "Nunca partilhes códigos, passwords ou dados bancários sem verificar a origem do pedido."
    )
}


def get_topics():
    return list(TOPICS.keys())


def get_topic_text(topic_name):
    return TOPICS.get(topic_name, "Tema não encontrado.")


st.set_page_config(page_title="Temas Financeiros", page_icon="📖", layout="wide")

st.title("📖 Temas de Educação Financeira")
st.caption("Explora os temas ao teu ritmo")

topic = st.selectbox("Escolhe um tema", get_topics())

if topic:
    st.markdown(f"### {topic}")
    st.write(get_topic_text(topic))
