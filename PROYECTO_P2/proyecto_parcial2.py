import random
import time
from dataclasses import dataclass
from typing import List, Callable, Any

# ==========================================================
# PARTE 1: MODELO DE DATOS Y GENERACIÓN
# ==========================================================
@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    categoria: str
    stock: int
    calificacionPromedio: float

def generar_productos(n: int = 50) -> List[Producto]:
    """Genera una lista de n objetos Producto con datos aleatorios y coherentes."""
    random.seed(42)
    categorias = ["Electrónica", "Ropa", "Libros", "Hogar", "Deportes"]
    adjetivos = ["Nuevo", "Premium", "Económico", "Pro", "Clásico", "Moderno"]
    sustantivos = ["Monitor", "Camiseta", "Novela", "Lámpara", "Balón", "Teclado"]
    
    productos = []
    ids_usados = set()
    
    for _ in range(n):
        while True:
            pid = random.randint(1000, 9999)
            if pid not in ids_usados:
                ids_usados.add(pid)
                break
                
        nombre = f"{random.choice(adjetivos)} {random.choice(sustantivos)}"
        precio = round(random.uniform(10.5, 999.9), 2)
        categoria = random.choice(categorias)
        stock = random.randint(0, 500)
        calificacion = round(random.uniform(1.0, 5.0), 1)
        
        productos.append(Producto(pid, nombre, precio, categoria, stock, calificacion))
    return productos

# ==========================================================
# PARTE 2: ALGORITMOS DE ORDENAMIENTO
# ==========================================================
def insertion_sort(arr: List[Producto], key: Callable[[Producto], Any]) -> None:
    """Ordenamiento por inserción in-place. Complejidad: O(n^2)"""
    for i in range(1, len(arr)):
        actual = arr[i]
        clave_actual = key(actual)
        j = i - 1
        while j >= 0 and key(arr[j]) > clave_actual:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual

def merge_sort(arr: List[Producto], key: Callable[[Producto], Any]) -> List[Producto]:
    """Ordenamiento por mezcla (Divide y Vencerás). Complejidad: O(n log n)"""
    if len(arr) <= 1:
        return arr
    mitad = len(arr) // 2
    izquierda = merge_sort(arr[:mitad], key)
    derecha = merge_sort(arr[mitad:], key)
    
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if key(izquierda[i]) <= key(derecha[j]):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

def quick_sort(arr: List[Producto], key: Callable[[Producto], Any]) -> List[Producto]:
    """Ordenamiento rápido. Complejidad promedio: O(n log n)"""
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    clave_pivote = key(pivote)
    menores = [x for x in arr if key(x) < clave_pivote]
    iguales = [x for x in arr if key(x) == clave_pivote]
    mayores = [x for x in arr if key(x) > clave_pivote]
    return quick_sort(menores, key) + iguales + quick_sort(mayores, key)

# ==========================================================
# PARTE 3: ALGORITMOS DE BÚSQUEDA
# ==========================================================
def busqueda_binaria_id(arr_ordenado: List[Producto], id_objetivo: int) -> bool:
    """Búsqueda binaria por ID. Requiere arreglo ordenado por ID. Complejidad: O(log n)"""
    izquierda, derecha = 0, len(arr_ordenado) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr_ordenado[medio].id == id_objetivo:
            return True
        elif arr_ordenado[medio].id < id_objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return False

def busqueda_lineal_nombre(arr: List[Producto], subcadena: str) -> List[Producto]:
    """Búsqueda lineal por subcadena en nombre. Complejidad: O(n * m)"""
    resultados = []
    sub_lower = subcadena.lower()
    for prod in arr:
        if sub_lower in prod.nombre.lower():
            resultados.append(prod)
    return resultados

# ==========================================================
# EJECUCIÓN Y MEDICIÓN
# ==========================================================
def main():
    productos = generar_productos(50)

    algoritmos = {
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    criterios = [
        ("Precio (Asc)", lambda p: p.precio),
        ("Calificacion (Desc)", lambda p: -p.calificacionPromedio)
    ]

    # Medición de ordenamiento
    print("TABLA DE TIEMPOS DE ORDENAMIENTO (segundos)")
    print(f"{'Algoritmo':<20} | {'Precio (Asc)':<15} | {'Calificacion (Desc)':<20}")
    print("-" * 60)

    tiempos_ord = {}
    for nombre_crit, key_func in criterios:
        tiempos_ord[nombre_crit] = {}
        for nombre_alg, func_alg in algoritmos.items():
            copia = productos.copy()
            inicio = time.perf_counter()
            if nombre_alg == "Insertion Sort":
                func_alg(copia, key_func)
            else:
                copia = func_alg(copia, key_func)
            fin = time.perf_counter()
            tiempos_ord[nombre_crit][nombre_alg] = fin - inicio

    for alg in algoritmos:
        print(f"{alg:<20} | {tiempos_ord['Precio (Asc)'][alg]:<15.8f} | {tiempos_ord['Calificacion (Desc)'][alg]:<20.8f}")

    # Preparación para búsqueda por ID
    productos_ordenados_id = quick_sort(productos.copy(), lambda p: p.id)
    ids_existentes = [productos[i].id for i in range(10)]
    ids_inexistentes = [99990 + i for i in range(10)]

    tiempo_binaria = 0.0
    for pid in ids_existentes + ids_inexistentes:
        inicio = time.perf_counter()
        busqueda_binaria_id(productos_ordenados_id, pid)
        tiempo_binaria += time.perf_counter() - inicio

    print(f"\nTiempo total Búsqueda Binaria por ID (20 consultas): {tiempo_binaria:.8f} s")

    # Preparación para búsqueda por nombre
    subcadenas_con = [productos[i].nombre.split()[0] for i in range(10)]
    subcadenas_sin = ["Xyz", "Qwerty", "123", "ZZZ", "Test", "NoExiste", "Foo", "Bar", "Baz", "Alpha"]

    tiempo_lineal = 0.0
    for sub in subcadenas_con + subcadenas_sin:
        inicio = time.perf_counter()
        busqueda_lineal_nombre(productos, sub)
        tiempo_lineal += time.perf_counter() - inicio

    print(f"Tiempo total Búsqueda Lineal por Nombre (20 consultas): {tiempo_lineal:.8f} s")

if __name__ == "__main__":
    main()