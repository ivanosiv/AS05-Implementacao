import streamlit as st
from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Configuração inicial do Streamlit
st.set_page_config(page_title="Análise de Documentos e Imagens", page_icon="📄", layout="centered")

# Exibe o título
st.title("📄 Perguntas sobre documentos e análise de imagens")

st.write(
    "Envie um documento ou imagem para análise e faça perguntas relacionadas ao conteúdo. "
    "Certifique-se de fornecer a chave de API do Google Gemini."
)

# Solicita ao usuário a chave de API do Gemini
google_api_key = st.text_input("Chave de API do Google (Gemini)", value=os.getenv("GOOGLE_API_KEY") or "", type="password")

if not google_api_key:
    st.info("Por favor, insira sua chave de API do Google Gemini para continuar.", icon="🗝️")
else:
    # Configurações do Gemini
    genai.configure(api_key=google_api_key)

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
        # Caso o documento tenha sido carregado
        if document:
            st.write("### Resposta baseada no documento:")
            try:
                prompt = f"Aqui está o conteúdo do documento:\n\n{document}\n\nPergunta: {question}"
                response = genai.generate_text(prompt, model="gemini-1.5-flash", temperature=0.5)
                st.write(response.result)
            except Exception as e:
                st.error(f"Erro ao consultar o Gemini: {e}")

        # Caso uma imagem tenha sido carregada
        if image:
            st.write("### Análise baseada na imagem:")
            try:
                prompt = f"Analise a imagem carregada considerando a seguinte pergunta: {question}."
                response = genai.generate_text(prompt, model="gemini-1.5-flash", temperature=0.5)
                st.write(response.result)
            except Exception as e:
                st.error(f"Erro ao consultar o Gemini: {e}")
