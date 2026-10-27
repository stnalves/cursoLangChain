from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

# Criando ChatPromptTemplate
print("-----Exemplo Chain 1 -----")

prompt_template = ChatPromptTemplate([
    ("user", "Escreva um poema em {língua} sobre o tema: {assunto}")
])

# Criando a chain
chain1 = prompt_template | model

#Invoke da chain passando as variáveis
resultado = chain1.invoke({"língua": "pt-br", "assunto": "frutas"})

resposta = "".join(
    bloco["text"]
    for bloco in resultado.content
    if isinstance(bloco, dict) and bloco.get("type") == "text"
)

print(resposta)

# Criando ChatPromptTemplate já com mensagem de sistema
print("-----Exemplo Chain 2 -----")

mensagens = [
    ("system", "Você é um poeta brasileiro famoso e escreve poemas de no máximo {n_versos} versos."),
    ("human", "Escreva para mim um poema sobre {assunto}.")
]

prompt_template = ChatPromptTemplate(mensagens)

# Criando a chain
chain2 = prompt_template | model

# Invoke de chain passando as variáveis
resultado = chain2.invoke({"n_versos": "10", "assunto": "navios"})

resposta = "".join(
    bloco["text"]
    for bloco in resultado.content
    if isinstance(bloco, dict) and bloco.get("type") == "text"
)

print(resposta)