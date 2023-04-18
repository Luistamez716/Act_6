import os
import random
import time
import matplotlib.pyplot as plt

def leer_instancia(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    n, capacidad = map(int, lineas[0].strip().split())
    items = [tuple(map(float, linea.strip().replace(',', '.').split())) for linea in lineas[1:-1]]  
    valor_optimo = float(lineas[-1].strip().split()[1].replace(',', '.')) 
    return capacidad, items, valor_optimo



def greedy_randomizado(items, capacidad, alpha):
    solucion = [0] * len(items)
    peso_actual = 0
    valor_actual = 0

    items_candidatos = list(enumerate(items))
    random.shuffle(items_candidatos)

    while items_candidatos:
        items_candidatos = sorted(items_candidatos, key=lambda x: x[1][1] / x[1][0], reverse=True)
        max_indice = int(alpha * (len(items_candidatos) - 1))
        item_seleccionado = random.randint(0, max_indice)
        idx, (peso, valor) = items_candidatos[item_seleccionado]

        if peso_actual + peso <= capacidad:
            solucion[idx] = 1
            peso_actual += peso
            valor_actual += valor

        del items_candidatos[item_seleccionado]

    return solucion, valor_actual

def grasp(items, capacidad, alpha, max_iteraciones):
    mejor_solucion = None
    mejor_valor = 0

    for _ in range(max_iteraciones):
        solucion_actual, valor_actual = greedy_randomizado(items, capacidad, alpha)
        if valor_actual > mejor_valor:
            mejor_solucion = solucion_actual
            mejor_valor = valor_actual

    return mejor_solucion, mejor_valor

instancias = 'instancias'
archivos = [f for f in os.listdir(instancias) if f.endswith('.txt')]
alpha = 0.5
max_iteraciones = 100

archivos_lista = []
tiempos_ejecucion = []
valores_soluciones = []

for archivo in archivos:
    ruta_archivo = os.path.join(instancias, archivo)
    capacidad, items, valor_optimo = leer_instancia(ruta_archivo)

    start_time = time.time()
    mejor_solucion, mejor_valor = grasp(items, capacidad, alpha, max_iteraciones)
    end_time = time.time()
    
    tiempo_ejecucion = end_time - start_time
    
    archivos_lista.append(archivo)
    tiempos_ejecucion.append(tiempo_ejecucion)
    valores_soluciones.append(mejor_valor)

    print(f"Archivo: {archivo}")
    print(f"Valor óptimo: {valor_optimo}")
    print(f"Mejor solución encontrada: {mejor_solucion}")
    print(f"Valor de la mejor solución encontrada: {mejor_valor}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f}\n")
    print("---------------------------------------------------------\n")
    
    # Gráfico de caja para los tiempos de ejecución
plt.boxplot(tiempos_ejecucion)
plt.xticks(range(1, len(archivos_lista) + 1), archivos_lista)
plt.xlabel("Instancias")
plt.ylabel("Tiempo de ejecución (segundos)")
plt.title("Boxplot - Tiempos de ejecución")
plt.show()

# Gráfico de barras para los valores de las soluciones encontradas
x = range(len(archivos_lista))
plt.bar(x, valores_soluciones)
plt.xticks(x, archivos_lista)
plt.xlabel("Instancias")
plt.ylabel("Valor de la mejor solución encontrada")
plt.title("Gráfico de barras - Valores de las soluciones encontradas")
plt.show()
