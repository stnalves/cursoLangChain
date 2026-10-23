from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

## Chatmodel
model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash", 
    temperature=0.1
)

conversa = [
    SystemMessage(content="Você é um assistente útil que responde ao usuário com detalhes e exemplos.")
]

while True:
    entrada = input("Entrada Usuário (digite 'q' para parar.): ")
    if entrada.lower() == "q":
        break

    conversa.append(HumanMessage(content=entrada))

    resultado = model.invoke(conversa)
    resposta = resultado.content
    conversa.append(AIMessage(content=resposta))

    print(f"Resposta IA: {resposta}")

print("---- Histórico Completo ----")
print(conversa)