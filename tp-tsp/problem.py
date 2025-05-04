"""Este modulo define la clase OptProblem.

OptProblem representa un problema de optimizacion general (de maximización).
La subclase TSP de OptProblem representa al Problema del Viajante.

Formulacion de estado completo para el Problema del Viajante:

* Estados:
    Consideramos n ciudades enumeradas del 0 al n-1.
    Cada estado es de la forma [0] ++ permutacion(1,n-1) ++ [0].
    Total de estados: (n-1)! pues la primera ciudad del tour ya esta fija.
    Ejemplo con n = 4: [0,1,2,3,0], [0,1,3,2,0], etc.

* Estado inicial.
    Consideramos el estado inicial [0,1,2,...,n-1,0].
    Pero cualquier estado puede ser inicial.

* Acciones.
    Consideramos como accion el intercambio de dos aristas del tour.
    Esta familia de acciones se conoce como 2-opt, mas info en:
    https://en.wikipedia.org/wiki/2-opt
    Cada accion se puede representar de la siguiente forma.
    (i,j): intercambiar la i-esima arista con la j-esima arista,
    con 0 <= i <= n-3, i+2 <= j <= n-1.
    Notar que las aristas elegidas no deben ser adyacentes.

* Resultado.
    resultado([v_0,...,v_n], (i,j)) =
        [v_0,...,v_i] ++ [v_j,...,v_i+1] ++ [v_j+1,...,v_n]
    Notar que [v_j,...,v_i+1] es el reverso de [v_i+1,...,v_j]

* Funcion objetivo:
    obj_val([v_0,v_1,...,v_n-1,v_n]) =
        - dist[v_0][v_1] - ... - dist[v_n-1][v_n]
    El objetivo es minimizar la distancia, es decir,
    maximizar el opuesto de las distancias.
"""

from __future__ import annotations
from typing import TypeVar
from random import shuffle
from networkx import Graph

State = TypeVar('State')
Action = TypeVar('Action')


class OptProblem:
    """Clase que representa un problema de optimizacion general (de maximización)."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.init = None

    def actions(self, state: State) -> list[Action]:
        """Determina la lista de acciones que se pueden aplicar a un estado."""
        raise NotImplementedError

    def result(self, state: State, action: Action) -> State:
        """Determina el estado resultado de aplicar una accion a un estado."""
        raise NotImplementedError

    def obj_val(self, state: State) -> float:
        """Determina el valor objetivo de un estado."""
        raise NotImplementedError

    def max_action(self, state: State) -> tuple[Action, float]:
        """Determina la accion que genera el sucesor con mayor valor objetivo para un estado dado.

        La idea es que este metodo este optimizado y sea mas eficiente que generar cada
        estado sucesor por separado y calcular su valor objetivo con self.obj_val().
        """
        raise NotImplementedError

    def random_reset(self) -> State:
        """Retorna un estado generado al azar. 
        
        Este método será necesario para implementar el reinicion aleatorio.
        """
        raise NotImplementedError


class TSP(OptProblem):
    """Subclase que representa al Problema del Viajante (TSP).

    Un estado es una lista de enteros: list[int].
    Una accion es un par de enteros: tuple[int,int].
    """

    def __init__(self, G: Graph) -> None:
        """Construye una instancia de TSP.

        Argumentos:
        ==========
        G: Graph
            grafo con los datos del problema
            los nodos del grafo se enumeran de 1 a n, ¡cuidado!
        """
        super().__init__()
        self.G = G
        self.init = list(range(0, G.number_of_nodes()))
        self.init.append(0)

    def actions(self, state: list[int]) -> list[tuple[int, int]]:
        """Determina la lista de acciones que se pueden aplicar a un estado.

        Argumentos:
        ==========
        state: list[int]
            un estado

        Retorno:
        =======
        act: list[tuple[int, int]]
            lista de acciones
        """
        act = []
        for i in range(0, self.G.number_of_nodes() - 2):
            for j in range(i + 2, self.G.number_of_nodes()):
                if (j + 1) % self.G.number_of_nodes() != i:
                    act.append((i, j))
        return act

    def result(self, state: list[int], action: tuple[int, int]) -> list[int]:
        """Determina el estado que resulta de aplicar una accion a un estado.

        Argumentos:
        ==========
        state: list[int]
            un estado
        action: tuple[int, int]
            una accion de self.acciones(state)

        Retorno:
        =======
        succ: list[int]
            estado sucesor
        """
        succ = list(state)  # copy of the current state
        i, j = action
        succ[i + 1: j+1] = state[i + 1: j+1][::-1]  # reverse
        return succ

    def obj_val(self, state: list[int]) -> float:
        """Determina el valor objetivo de un estado.

        Argumentos:
        ==========
        state: list[int]
            un estado

        Retorno:
        =======
        value: float
            valor objetivo
        """
        value = 0
        for i in range(0, self.G.number_of_nodes()):
            u = state[i]+1  # origen
            v = state[i+1]+1  # destino
            value -= self.G.get_edge_data(u, v)['weight']
        return value

    def max_action(self, state: list[int], tabu_list: list[tuple[int, int]] = []) -> tuple[tuple[int, int], float]:
        """Determina la accion que genera el sucesor con mayor valor objetivo para un estado dado.
        
        Se encuentra optimizada y por razones de eficiencia no se generan los sucesores y 
        tampoco se llama a self.obj_val().

        Argumentos:
        ==========
        state: list[int]
            un estado

        Retorno:
        =======
        max_act: tuple[int, int]
            accion que genera el sucesor con mayor valor objetivo
        max_val: float
            valor objetivo del sucesor que resulta de aplicar min_act
        """
        value = self.obj_val(state)
        max_act = None
        max_val = float("-inf")
        for a in self.actions(state):
            if a in tabu_list:
                continue  # Ignorar acciones que estén en la lista tabú
            i, j = a
            v1 = state[i]+1  # origen de i
            v2 = state[i+1]+1  # destino de i
            v3 = state[j]+1  # origen de j
            v4 = state[j+1]+1  # destino de j
            distl1l2 = self.G.get_edge_data(v1, v2)['weight']
            distl3l4 = self.G.get_edge_data(v3, v4)['weight']
            distl1l3 = self.G.get_edge_data(v1, v3)['weight']
            distl2l4 = self.G.get_edge_data(v2, v4)['weight']
            succ_value =  value + distl1l2 + distl3l4 - distl1l3 - distl2l4
            if succ_value > max_val:
                max_act = a
                max_val = succ_value
        return max_act, max_val

    def random_reset(self) -> list[int]:
        """Devuelve un estado del TSP con un tour aleatorio.
        
        Retorno:
        =======
        state: list[int]
            un estado
        """
        state = [i for i in range(1, self.G.number_of_nodes())]
        shuffle(state)  # mezclar la lista
        state.append(0)  # agregar a 0 como inicio del tour
        state.insert(0, 0)  # agregar a 0 como fin del tour
        return state
