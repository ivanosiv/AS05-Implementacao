import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# Exibe o título e a descrição
st.title("📄 Perguntas sobre documentos")
st.write(
    "Envie um documento abaixo e faça uma pergunta sobre ele – o GPT responderá! "
    "Para usar este aplicativo, você precisa fornecer uma chave de API da OpenAI, que pode ser obtida [aqui](https://platform.openai.com/account/api-keys)."
)

# Solicita ao usuário sua chave de API da OpenAI via `st.text_input`
openai_api_key = st.text_input("Chave de API da OpenAI", type="password")
if not openai_api_key:
    st.info("Por favor, insira sua chave de API da OpenAI para continuar.", icon="🗝️")
else:
    # Cria um cliente OpenAI
    client = OpenAI(api_key=openai_api_key)

    # Permite ao usuário enviar um arquivo via `st.file_uploader`
    uploaded_file = st.file_uploader(
        "Envie um documento (.txt, .md ou .pdf)", type=("txt", "md", "pdf")
    )

    # Inicializa a variável para o conteúdo do documento
    document = ""

    if uploaded_file:
        # Processa arquivos de texto ou Markdown
        if uploaded_file.name.endswith(("txt", "md")):
            document = uploaded_file.read().decode()
        # Processa arquivos PDF
        elif uploaded_file.name.endswith("pdf"):
            pdf_reader = PdfReader(uploaded_file)
            document = ""
            for page in pdf_reader.pages:
                document += page.extract_text()
        
        # Exibe uma prévia do conteúdo
        st.write("### Prévia do conteúdo do documento:")
        st.write(document[:500] + "...")  # Mostra os primeiros 500 caracteres

    # Solicita ao usuário uma pergunta via `st.text_area`
    question = st.text_area(
        "Agora faça uma pergunta sobre o documento!",
        placeholder="Você pode me dar um resumo curto?",
        disabled=not document,
    )

    if document and question:
        # Prepara a mensagem para a API da OpenAI
        messages = [
            {
                "role": "user",
                "content": f"Aqui está um documento: {document} \n\n---\n\n {question}",
            }
        ]

        # Gera uma resposta usando a API da OpenAI
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

            # Transmite a resposta para o app
            st.write("### Resposta:")
            st.write_stream(stream)

        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")
