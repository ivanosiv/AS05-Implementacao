# 📄 **Resumidor de PDFs - AS05 Implementação**

Este projeto é uma aplicação construída com **Streamlit** para análise de múltiplos arquivos PDF. Utilizando a API do **Google Gemini**, o aplicativo gera resumos e responde a perguntas sobre o conteúdo dos documentos enviados.

---

## 🚀 **Funcionalidades**
- **Envio de múltiplos PDFs**:
  - Suporte ao upload de vários arquivos PDF simultaneamente.
  - Exibição de uma prévia dos documentos carregados.

- **Resumos e Respostas Automatizadas**:
  - Resumos gerados automaticamente para cada PDF.
  - Respostas personalizadas baseadas nas perguntas feitas sobre os documentos enviados.

- **Integração com o Google Gemini**:
  - Usa a API do Google Gemini para processar e interpretar o conteúdo dos PDFs.

---

## 🛠️ **Configuração e Execução**

### 1. **Pré-requisitos**
- **Python 3.8+** instalado.
- **Chave de API do Google Gemini**:
  - Crie ou acesse sua chave no [Google Cloud Console](https://console.cloud.google.com/).

### 2. **Clone o Repositório**
```bash
git clone https://github.com/ivanosiv/AS05-Implementacao.git
cd AS05-Implementacao
```

### 3. **Instale as Dependências**
Certifique-se de instalar todas as dependências do projeto:
```bash
pip install -r requirements.txt
```

### 4. **Configuração da Chave de API**
Crie um arquivo `.env` no diretório do projeto e adicione sua chave de API do Google Gemini:
```plaintext
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

### 5. **Execute o Aplicativo**
Inicie o aplicativo com o comando:
```bash
streamlit run streamlit_app.py
```

---

## 📝 **Como Usar**
1. **Envie Múltiplos PDFs**:
   - Carregue um ou mais arquivos PDF no campo de upload disponível.

2. **Faça uma Pergunta ou Solicite um Resumo**:
   - Insira uma pergunta ou solicitação no campo de texto fornecido.

3. **Receba Respostas**:
   - As respostas geradas serão exibidas para cada arquivo carregado, com base no conteúdo processado.

---

## 📂 **Estrutura do Projeto**
```
AS05-Implementacao/
│
├── streamlit_app.py    # Código principal do aplicativo Streamlit
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação do projeto
```

---

## 📦 **Dependências**
As principais bibliotecas utilizadas são:
- **Streamlit**: Para criar a interface do usuário.
- **PyPDF2**: Para processar e extrair texto de PDFs.
- **google-generativeai**: Para integração com a API do Google Gemini.

Para instalar todas as dependências, use:
```bash
pip install -r requirements.txt
```

---

## 🛡️ **Licença**
Este projeto é distribuído sob a licença MIT. Você pode utilizá-lo e modificá-lo conforme necessário.

---

## 📧 **Contato**
Se você tiver dúvidas, sugestões ou problemas, entre em contato:
- **GitHub**: [Ivanosiv](https://github.com/ivanosiv)

---
