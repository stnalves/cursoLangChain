from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage

print("=========== Exemplo 1 ===========")

prompt_template = PromptTemplate.from_template("Gere para mim um poema sobre: {assunto}. Escreva em {língua}")
retorno = prompt_template.invoke({"assunto": "navegação", "língua": "pt-br"})

print(retorno)


print("=========== Exemplo 2 ===========")

prompt_template = ChatPromptTemplate(
    [
        "Gere para mim um poema sobre: "
    ]
)


# print("=========== Exemplo 2 - Alternativa 1 ===========")



# print("=========== Exemplo 2 - Alternativa 2 ===========")


# print("=========== Exemplo 3 ===========")



# print("=========== Exemplo 3 - Alternativa 1 ===========")