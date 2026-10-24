from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.1
)

# O ChatModel é um componente LangChain, enttão possui o método invoke

resposta = model.invoke(
    "Olá, como você está e o que você é capaz de fazer?"
)

print("--------RESPOSTA AIMessage:---------")
print(resposta)
print("-------------------------------------")

print("--------RESPOSTA Somente Texto:------")
print(resposta.content)
print("-------------------------------------")