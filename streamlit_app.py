import streamlit as st
import os
import google.generativeai as genai
from pathlib import Path

# Configuração inicial do Streamlit
st.set_page_config(page_title="Resumidor de PDFs", page_icon="📄", layout="centered")

# Exibe o título
st.title("📄 Resumidor de PDFs")

st.write(
    "Envie um ou mais documentos PDF e faça perguntas relacionadas ao conteúdo. "
    "Certifique-se de fornecer a chave de API do Google Gemini."
)

# Solicita ao usuário a chave de API do Gemini
google_api_key = st.text_input("Chave de API do Google (Gemini)", value=os.getenv("GOOGLE_API_KEY") or "", type="password")

if not google_api_key:
    st.info("Por favor, insira sua chave de API do Google Gemini para continuar.", icon="🗝️")
else:
    # Configurações do Gemini
    genai.configure(api_key=google_api_key)

    # Upload de múltiplos documentos
    uploaded_files = st.file_uploader(
        "Envie um ou mais documentos PDF para análise", type=("pdf"), accept_multiple_files=True
    )

    # Processa os documentos enviados
    if uploaded_files:
        st.write("### Prévia dos documentos enviados:")
        uploaded_pdfs = []

        for uploaded_file in uploaded_files:
            # Salva o arquivo PDF localmente
            temp_path = Path(uploaded_file.name)
            temp_path.write_bytes(uploaded_file.getvalue())
            uploaded_pdfs.append(temp_path)
            st.write(f"✔️ {uploaded_file.name} carregado com sucesso!")

        # Campo para pergunta
        question = st.text_area(
            "Faça uma pergunta ou solicite um resumo dos documentos!",
            placeholder="Exemplo: Qual o resumo dos documentos enviados?",
        )

        if question:
            st.write("### Respostas baseadas nos documentos:")
            try:
                combined_responses = []
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Faz o upload de cada PDF e gera respostas
                for pdf_path in uploaded_pdfs:
                    sample_pdf = genai.upload_file(pdf_path)
                    response = model.generate_content([question, sample_pdf])
                    combined_responses.append(f"**{pdf_path.name}:** {response.text}")

                # Exibe as respostas combinadas
                for response_text in combined_responses:
                    st.write(response_text)

            except Exception as e:
                st.error(f"Erro ao processar os documentos no Gemini: {e}")
            finally:
                # Remove os arquivos temporários
                for pdf_path in uploaded_pdfs:
                    pdf_path.unlink()
