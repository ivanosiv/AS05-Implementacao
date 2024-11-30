import streamlit as st
from openai import OpenAI

# Exibe o título e a descrição.
st.title("📄 Perguntas sobre documentos")
st.write(
    "Envie um documento abaixo e faça uma pergunta sobre ele – o GPT responderá! "
    "Para usar este aplicativo, você precisa fornecer uma chave de API da OpenAI, que pode ser obtida [aqui](https://platform.openai.com/account/api-keys)."
)

# Solicita ao usuário sua chave de API da OpenAI via `st.text_input`.
# Alternativamente, você pode armazenar a chave de API em `./.streamlit/secrets.toml` e acessá-la
# através de `st.secrets`, veja https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("Chave de API da OpenAI", type="password")
if not openai_api_key:
    st.info("Por favor, insira sua chave de API da OpenAI para continuar.", icon="🗝️")
else:

    # Cria um cliente OpenAI.
    client = OpenAI(api_key=openai_api_key)

    # Permite ao usuário enviar um arquivo via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Envie um documento (.txt ou .md)", type=("txt", "md")
    )

    # Solicita ao usuário uma pergunta via `st.text_area`.
    question = st.text_area(
        "Agora faça uma pergunta sobre o documento!",
        placeholder="Você pode me dar um resumo curto?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Processa o arquivo enviado e a pergunta.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Aqui está um documento: {document} \n\n---\n\n {question}",
            }
        ]

        # Gera uma resposta usando a API da OpenAI.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Transmite a resposta para o app usando `st.write_stream`.
        st.write_stream(stream)
