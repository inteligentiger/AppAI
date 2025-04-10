import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega chave da OpenAI do arquivo .env
load_dotenv()
print("CHAVE CARREGADA:", os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Gerador de Análises com IA", layout="centered")

st.title("📊 Gerador Inteligente de Análises de Vendas")
st.write("Insira os dados da área comercial para gerar relatório, e-mail e plano de ação com IA.")

# Campos de entrada
meta = st.number_input("Meta (R$)", min_value=0.0, step=1000.0)
vendas = st.number_input("Vendas Realizadas (R$)", min_value=0.0, step=1000.0)
clientes_novos = st.number_input("Novos Clientes", min_value=0)
cancelamentos = st.number_input("Cancelamentos", min_value=0)
feedbacks_negativos = st.number_input("Feedbacks Negativos", min_value=0)

if st.button("🔮 Gerar Análise com IA"):
    dados = f"""
    Meta: R$ {meta}
    Vendas: R$ {vendas}
    Novos clientes: {clientes_novos}
    Cancelamentos: {cancelamentos}
    Feedbacks negativos: {feedbacks_negativos}
    """

    # Etapa 1 – Resumo Executivo
    resumo_prompt = f"""
    Você é um analista executivo. Gere um resumo profissional com os seguintes dados:

    {dados}

    Destaque pontos positivos e negativos. Até 3 parágrafos. Tom objetivo e técnico.
    """
    resumo_resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": resumo_prompt}]
    )
    resumo = resumo_resp.choices[0].message.content
    st.subheader("📄 Resumo Executivo")
    st.markdown(resumo)

    # Etapa 2 – E-mail
    email_prompt = f"""
    Você é um gerente de controladoria.
    Redija um e-mail para o gerente comercial com base neste resumo:

    {resumo}

    O e-mail deve ser respeitoso, objetivo e sugerir melhorias.
    Assine como 'Departamento de Controladoria'.
    """
    email_resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": email_prompt}]
    )
    email = email_resp.choices[0].message.content
    st.subheader("✉️ E-mail Gerado")
    st.markdown(email)

    # Etapa 3 – Plano de Ação
    acao_prompt = f"""
    Com base neste resumo:

    {resumo}

    Proponha até 3 ações com justificativa para melhorar os resultados.
    """
    plano_resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": acao_prompt}]
    )
    plano = plano_resp.choices[0].message.content
    st.subheader("✅ Plano de Ação")
    st.markdown(plano)