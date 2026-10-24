from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.1
)

# Criando a conversa
mensagens = [
    SystemMessage(content="Você é um especialista em astrofísica."),
    HumanMessage(content="Qual é a distância do Sol até a Terra?"),
    AIMessage(content="O Sol está a 149.600.000 km de distância da Terra."),
    HumanMessage(content="E a distância da Terra até Marte?"),
]

# Enviando o histórico de mensagens ao modelo
resposta = model.invoke(mensagens)

print("--------RESPOSTA AIMessage:---------")
print(resposta)
print("-------------------------------------")

resultado = "".join(
    bloco["text"]
    for bloco in resposta.content
    if isinstance(bloco, dict) and bloco.get("type") == "text"
)

print("--------RESPOSTA Somente Texto:------")
print(resultado)
print("-------------------------------------")