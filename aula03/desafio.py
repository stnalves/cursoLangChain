from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

# Parte 1
runnable_1 = RunnablePassthrough()

# Parte 2
def conta_caracteres(entrada: dict) -> int:
    return len(entrada["input"])

convert_func = RunnableLambda(conta_caracteres)

runnable_2 = RunnablePassthrough.assign(num_caract=conta_caracteres)

# Parte 3
def transforma(entrada: dict) -> str:
    resultado = entrada["input"] + " Conseguiu!"
    return resultado

runnable_3_transfomra_entrada = RunnableLambda(transforma)
runnable_3_passa_para_frente = RunnablePassthrough()

runnable_3 = RunnableParallel({
    "transformar_entrada": runnable_3_transfomra_entrada,
    "passa_parafrente": runnable_3_passa_para_frente
})

# Parte 4
runnable_4 = RunnablePassthrough()


# Unindo tudo
chain = runnable_1 | runnable_2 | runnable_3 | runnable_4

# Invocando
resposta = chain.invoke({"input": "Parabéns Você"})

print('----- RESPOSTA DO DESAFIO ------')
print(resposta)
print('--------------------------------')