import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64

# Configuração inicial do Streamlit
st.set_page_config(page_title="Análise de Documentos e Imagens", page_icon="📄", layout="centered")

# Exibe o título
st.title("📄 Perguntas sobre documentos e análise de imagens")

st.write(
    "Envie um documento ou imagem para análise e faça perguntas relacionadas ao conteúdo."
)

# Solicita ao usuário as chaves de API
openai_api_key = st.text_input("Chave de API da OpenAI", type="password")
google_api_key = st.text_input("Chave de API do Google (Gemini)", value=os.getenv("GOOGLE_API_KEY") or "", type="password")

if not openai_api_key or not google_api_key:
    st.info("Por favor, insira suas chaves de API para continuar.", icon="🗝️")
else:
    # Configurações das APIs
    genai.configure(api_key=google_api_key)
    openai_client = OpenAI(api_key=openai_api_key)

    # Upload do documento
    uploaded_file = st.file_uploader(
        "Envie um documento (.txt, .md ou .pdf)", type=("txt", "md", "pdf")
    )

    # Upload de imagens para análise
    uploaded_image = st.file_uploader("Carregar uma imagem de refeição ou ingredientes:", type=["png", "jpg", "jpeg"])

    # Variáveis para conteúdo do documento e imagem
    document = ""
    image = None

    if uploaded_file:
        if uploaded_file.name.endswith(("txt", "md")):
            document = uploaded_file.read().decode()
        elif uploaded_file.name.endswith("pdf"):
            pdf_reader = PdfReader(uploaded_file)
            document = "".join([page.extract_text() for page in pdf_reader.pages])

        st.write("### Prévia do documento:")
        st.write(document[:500] + "...")  # Mostra os primeiros 500 caracteres do documento

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Imagem carregada", use_column_width=True)

    # Campo para pergunta
    question = st.text_area(
        "Faça uma pergunta sobre o documento ou solicite uma análise da imagem!",
        placeholder="Exemplo: Qual o resumo do documento? Ou analise os ingredientes desta imagem.",
        disabled=not (document or image),
    )

    if question:
        # Verifica se o prompt deve ser enviado ao GPT ou Gemini
        if document:
            st.write("### Resposta do GPT:")
            messages = [
                {
                    "role": "user",
                    "content": f"Aqui está um documento: {document} \n\n---\n\n {question}",
                }
            ]
            try:
                stream = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    stream=True,
                )
                st.write_stream(stream)
            except Exception as e:
                st.error(f"Erro ao consultar GPT: {e}")

        if image:
            st.write("### Análise da Imagem com Gemini:")
            prompt = (
                f"Analise a imagem carregada considerando as seguintes informações: {question}. "
            )
            try:
                st.write_stream(
                    genai.GenerativeModel(model_name="gemini-1.5-flash")
                    .generate_content(contents=[{"role": "user", "parts": [prompt]}], stream=True)
                )
            except Exception as e:
                st.error(f"Erro ao consultar Gemini: {e}")
