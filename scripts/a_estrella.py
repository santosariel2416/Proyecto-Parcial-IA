#Jesus Ariel Santos
#24-EISN-2-034
import heapq #importamos la libreia heapq para usar una cola de prioridad en la implementacion del algoritmo A*
import time #importamos la libreria time para medir el tiempo de ejecutar el algoritmo A*

#Este script implementa el algoritmo A* para encontrar el camino mas corto entre un estado inicial y un estado final, usando una cola de prioridad
class Nodo:
    def __init__(self, dato, padre=None, h=0):#El nod tiene un dato que representa el estado, un padre que es el nodo anterior en el camino, una heuristica h que es una estimacion del costo restante para llegar al estado final, y un costo g que es el costo acumulado desde el nodo inical hasta el nodo actual
        self.dato = dato
        self.padre = padre
        self.g = 0 if padre is None else padre.g + 1  # Costo acumulado
        self.h = h  # Heurística
        self.f = self.g + self.h  # Costo total

    def __lt__(self, otro):#el metodo __lt__ se usa para comparar dos nodos en la cola de prioridad, se compara el costo total f de cada nodo
        return self.f < otro.f

    def __eq__(self, otro): # el metodo eq se usa para comparar dos nodos, se comparan sus datos, es decir, sus estados
        return self.dato == otro.dato

    def __hash__(self):#el metodo hash se usa para poder usar los nodos en un conjunto, se usa el hash del dato del nodo, es decir, el hash del estado
        return hash(self.dato)


def Astar(estado_inicial, estado_final):#La funcion Astar recibe un estado inicial y un estado final, y devuelve el camino mas corto entre ambos estados, el numero de nodos generados y el tiempo de ejecucion del algoritmo
    totalnodos = 1
    nodo_inicial = Nodo(estado_inicial, None, estado_inicial.Costo(estado_final))

    nodos_generados = []
    nodos_visitados = set()

    heapq.heapify(nodos_generados)#inicializamos la cola de prioridad vacia y el conjuntos de nodos visitados vacios
    heapq.heappush(nodos_generados, nodo_inicial)

    inicio = time.perf_counter()#iniciamos el contador de tiempo para medir el tiempo de ejecucion del algoritmo

    while nodos_generados:#
        nodo_actual = heapq.heappop(nodos_generados)

        if nodo_actual.dato == estado_final:# si el nodo actual es el estado final entonces se ha encontrado el camino mas corto, se sale del ciclo
            break

        if nodo_actual in nodos_visitados:# si el nodo actual ya ha sido visitado entonces se sigue con el siguiente nodo en la cola de prioridad
            continue

        nodos_visitados.add(nodo_actual)

        sucesores = nodo_actual.dato.GenerarSucesores() # se generan los sucesores del nodo actual, es decir, los estados que pueden ser alcanzados desde el estado del nodo actual
        totalnodos += len(sucesores)

        for sucesor in sucesores:
            nuevo_nodo = Nodo(
                sucesor,
                nodo_actual,
                sucesor.Costo(estado_final)
            )

            if nuevo_nodo not in nodos_visitados:
                heapq.heappush(nodos_generados, nuevo_nodo)

    # Reconstrucción del camino
    camino = []
    while nodo_actual: # se reconstruye el camino desde el nodo actual hasta el nodo inicial, agregando los datos de cada nodo al camino
        camino.append(nodo_actual.dato)
        nodo_actual = nodo_actual.padre

    camino.reverse()

    fin = time.perf_counter()# Se detiene el contador de tiempo para medir el tiempo de ejecucion del algoritmo 

    return camino, totalnodos, fin - inicio # se devuelve el camino encontrado , el numero de nodos generados y el tiempo de ejecucion del algoritmo