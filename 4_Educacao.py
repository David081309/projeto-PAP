import streamlit as st

st.set_page_config(page_title="Educação Financeira", page_icon="📚", layout="wide")

st.title("Educação Financeira")
st.caption("Aprender a gerir dinheiro de forma simples")

st.subheader("Temas que podes incluir")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("### Necessidades vs desejos")
    st.write("Ajuda o utilizador a perceber a diferença entre o que precisa mesmo e o que quer comprar por impulso.")

    st.markdown("### Viver dentro dos meios")
    st.write("Mostra que gastar menos do que se ganha é a base para manter controlo financeiro.")

with col2:
    st.markdown("### Poupança e metas")
    st.write("Explica porque é importante guardar dinheiro para objetivos e imprevistos.")

    st.markdown("### Fraude e segurança")
    st.write("Ensina cuidados básicos com mensagens falsas, links suspeitos e dados bancários.")

st.divider()
st.success("Esta secção pode crescer depois com quizzes, dicas semanais e explicações curtas.")
