class Nodo:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")


#Aqui se define el arbol de comportamiento, con sus nodos y acciones. es la base de la IA de los vigilantes 

class Selector(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


# El nodo de secuencia ejecuta a sus hijos en orden y solo devuelve True si los hojos devuelven True

class Secuencia(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


#El nodo de accion ejecuta una funcion que se le pasa al crear el nodo

class Accion(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()


# el nodo de invertir devuelve el resultado contrario de su hijo

class Invertir(Nodo):
    def __init__(self, hijo):
        super().__init__()
        self.agregar_hijo(hijo)

    def ejecutar(self):
        if not self.hijos:
            return False
        return not self.hijos[0].ejecutar()


# el nodo de timer ejecuta a su hijo cada cierto tiempo, 

class Timer(Nodo):
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo

            if self.hijos:
                return self.hijos[0].ejecutar()

            return True