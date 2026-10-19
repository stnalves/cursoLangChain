from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel

""" RunnableLambda """

def add_one(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one)

# Transformando a função genérica em um Runnable de LangChain, ou seja, ele implementa automaticamente os métodos. Ex: invoke, etc
resposta = runnable.invoke(1)

print('----- RESPOSTA DO INVOKE - RunnableLambda -----')
print(resposta)
print('-----------------------------------------------')

# ==================================================================================

""" RunnableSequence """

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)

# Criando a cadeia sequencial
sequence = runnable_1 | runnable_2

resposta = sequence.invoke(1)

print('----- RESPOSTA DO INVOKE - RunnableSequence -----')
print(resposta)
print('-------------------------------------------------')

# ==================================================================================

""" RunnableParallel """

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

def mul_three(x: int) -> int:
    return x * 3

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
runnable_3 = RunnableLambda(mul_three)

# O dicionário é entendido como 'RunnableParallel'

# Opção 1
sequence = runnable_1 | {
    "mul_two": runnable_2,
    "mul_three": runnable_3,
}

# Opção 2
sequence = runnable_1 | RunnableParallel(
    {"mul_two": runnable_2, 'mul_tree':runnable_3}
)

# Opção 3
sequence = runnable_1 | RunnableParallel(
    mul_two=runnable_2,
    mul_three=runnable_3,
)

resposta = sequence.invoke(1)

print('----- RESPOSTA DO INVOKE - RunnableParallel -----')
print(resposta)
print('-------------------------------------------------')

# ==================================================================================

""" RunnablePassthrough """

chain = RunnablePassthrough() | RunnablePassthrough() | RunnablePassthrough()

# Independente de quantas vezes você "passar o resultado para frente", a entrada não é alterada.

resposta = chain.invoke("Olá")

print('----- RESPOSTA DO INVOKE - RunnablePassthrough -----')
print(resposta)
print('----------------------------------------------------')

# ==================================================================================

""" RunnablePassthrough + RunnableLambda """

def entrada_para_letras_maiusculas(entrada: str):
    saida = entrada.upper()
    return saida

chain = RunnablePassthrough() | RunnableLambda(entrada_para_letras_maiusculas) | RunnablePassthrough()

# Neste caso, vamos receber a entrada do usuário, passar para a função 'entrada_para_letras_maiusculas', transformar olá -> OLÁ e passar para frente.

resposta = chain.invoke('olá')

print('----- RESPOSTA DO INVOKE - RunnablePassthrough + RunnableLambda -----')
print(resposta)
print('---------------------------------------------------------------------')

# ==================================================================================

""" Operador Assign """

runnable = RunnablePassthrough() | RunnablePassthrough.assign(multiplica_3=lambda x: x["num"] * 3)

resposta = runnable.invoke({"num": 1})

print('----- RESPOSTA DO INVOKE - Operador Assign -----')
print(resposta)
print('------------------------------------------------')