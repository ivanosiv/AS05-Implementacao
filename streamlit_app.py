import streamlit as st
from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from PIL import Image
from pathlib import Path

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

    # Processa o documento se enviado
    if uploaded_file:
        st.write("### Prévia do documento:")
        if uploaded_file.name.endswith("pdf"):
            # Salva o arquivo PDF localmente
            temp_path = Path("temp.pdf")
            temp_path.write_bytes(uploaded_file.getvalue())

            try:
                # Faz o upload do PDF para o Gemini
                sample_pdf = genai.upload_file(temp_path)
                st.write("Arquivo enviado ao Gemini com sucesso!")

                # Campo para pergunta
                question = st.text_area(
                    "Faça uma pergunta sobre o documento!",
                    placeholder="Exemplo: Qual o resumo do documento?",
                )

                if question:
                    st.write("### Resposta baseada no documento:")
                    # Gera resposta usando o modelo Gemini
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([question, sample_pdf])
                    st.write(response.text)

            except Exception as e:
                st.error(f"Erro ao processar o documento no Gemini: {e}")
            finally:
                # Remove o arquivo temporário após o upload
                temp_path.unlink()

        else:
            st.error("Atualmente, apenas arquivos PDF são suportados para envio ao Gemini.")

    # Processa a imagem se enviada
    if uploaded_image:
        st.image(uploaded_image, caption="Imagem carregada", use_column_width=True)

        # Campo para pergunta
        question = st.text_area(
            "Faça uma pergunta sobre a imagem!",
            placeholder="Exemplo: Quais são os ingredientes na imagem?",
        )

        if question:
            st.write("### Resposta baseada na imagem:")
            try:
                # Gera resposta para a imagem
                prompt = f"Analise a imagem e responda: {question}"
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([prompt])
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao processar a imagem no Gemini: {e}")
