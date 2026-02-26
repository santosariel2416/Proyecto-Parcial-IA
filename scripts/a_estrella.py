#Jesus Ariel Santos
#24-EISN-2-034 
import heapq
import time

class Nodo:#clse nodo para representar cada estado en la busqueda del algoritmo A*
    def __init__(self, dato, padre=None, h=0):#Este es el costructor del nodo, recibe el estado (dato), el nodo padre y la heuristica
        self.dato = dato #estado del nodo en este caso es un estado del mapa con la posicion del vigilante y el jugador 
        self.padre = padre #nodo padre para poder reconstruir el camino al final
        self.g = 0 if padre is None else padre.g + 1 # Costo acumulado desde el inicio
        self.h = h # Esta es la heuristica, que se calcula al crear el nodo y se pasa como parametro, esta se calcula usando la funcion costo del estado actual al estado final que es el jugador 
        self.f = self.g + self.h #costo total 

    def __lt__(self, otro): # Este metodo es necesario para que el heapq pueda comparar nodos y ordenarlos por su costo total f 
        return self.f < otro.f

    def __eq__(self, otro):# este es el metodo de igualdad, se usa para comparar nodos y saber si ya hemos visitado un nodo o no
        # Compara el estado (EstadoMapa) dentro del nodo
        return self.dato == otro.dato

    def __hash__(self):# Este metodo es necesario para que el nodo pueda ser agregado a un set de nodos visitados 
        return hash(self.dato)


def Astar(estado_inicial, estado_final): #funcion que implmenta el algoritmo A*, recibe el estado inicial y el estado final, en este caso el estado inicial es la posicion del vigilante y el estado final es la posicion del jugador 
    # Si el inicio y el final son el mismo, no hay nada que buscar
    if estado_inicial == estado_final:# si el estado inicial es igual al estado final 
        return [estado_inicial]

    nodoactual = Nodo(
        estado_inicial,
        None,
        estado_inicial.Costo(estado_final)
    ) #cree el nodo inicial con el estado inicial, sin padre y con la heuristica calculadora usando la funcion costo del estado inicial al estado final

    nodosgenerado = [] #Esta es la lista de nodos generados que se usara como una cola de prioridad para el algoritmo A*, 
    heapq.heapify(nodosgenerado) # 
    heapq.heappush(nodosgenerado, nodoactual)

    # Usare set para que la búsqueda de nodos visitados sea ultra rápida
    nodosvisitados = set()

    while nodosgenerado: #este ciclo se ejecuta mientras haya nodos generados por revisar 
        nodoactual = heapq.heappop(nodosgenerado) #

        # Si llegamos al destino, reconstruimos el camino
        if nodoactual.dato == estado_final: # si el estado del nodo actual es igual al estado final, hemos encontrado el camino 
            camino = []
            while nodoactual:
                camino.append(nodoactual.dato)
                nodoactual = nodoactual.padre
            camino.reverse()
            return camino # Retornamos solo el camino para el vigilante

        nodosvisitados.add(nodoactual) # Agregamos el nodo actual a los nodos visitados para no revisarlo de nuevo 

        sucesores = nodoactual.dato.GenerarSucesores() #Aqui generamos los sucesores del nodo actual usando el metodo GenerarSucesores del estado 

        for sucesor in sucesores:#este ciclo se ejecuta para cada sucesor generado por el nodo actual 
            nuevo_nodo = Nodo(
                sucesor,
                nodoactual,
                sucesor.Costo(estado_final)
            )

            if nuevo_nodo in nodosvisitados: # Aqui revisamos si el nuevo nodo ya ha sido visitado, si es asi lo ignoramos y seguimos con el siguiente sucesor 
                continue

            heapq.heappush(nodosgenerado, nuevo_nodo) #si el nuevo nodo no ha sido visitado, lo agregamos a la lista de nodos generados para ser revisado en el futuro 

    return [] # Si no hay camino, devolvemos lista vacía