"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascensión de colinas con reinicio aleatorio.

    Este algoritmo realiza múltiples búsquedas locales de ascensión de colinas,
    reiniciando desde un estado aleatorio cada vez que alcanza un óptimo local.
    """

    def __init__(self, max_restarts: int = 10) -> None:
        """Construye una instancia del algoritmo con reinicio aleatorio.

        Argumentos:
        ==========
        max_restarts: int
            Número máximo de reinicios aleatorios permitidos.
        """
        super().__init__()
        self.max_restarts = max_restarts  # Número máximo de reinicios

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con reinicio aleatorio.

        Argumentos:
        ==========
        problem: OptProblem
            Un problema de optimización
        """
        # Inicio del reloj
        start = time()

        # Variables para almacenar la mejor solución global
        best_tour = None
        best_value = float('-inf')

        for restart in range(self.max_restarts):
            # Reinicio aleatorio o estado inicial
            if restart == 0:
                actual = problem.init
            else:
                actual = problem.random_reset()

            value = problem.obj_val(actual)

            while True:
                # Buscamos la acción que genera el sucesor con mayor valor objetivo
                act, succ_val = problem.max_action(actual)

                # Si estamos en un máximo local, terminamos esta iteración
                if succ_val <= value:
                    break

                # Sino, nos movemos al sucesor
                actual = problem.result(actual, act)
                value = succ_val
                self.niters += 1

            # Actualizamos la mejor solución global si encontramos una mejor
            if value > best_value:
                best_tour = actual
                best_value = value

        # Guardamos la mejor solución global
        self.tour = best_tour
        self.value = best_value
        self.time = time() - start

class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    # COMPLETAR
