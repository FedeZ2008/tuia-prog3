from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        node.estimated_distance = AStarSearch.heuristic(grid.start, grid.end)


        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = node.cost
        

        # Initialize the frontier with the initial node
        # In this example, the frontier is a priority queue
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost + node.estimated_distance)


        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            current_node = frontier.pop()

            if current_node.state == grid.end:
                return Solution(current_node, explored)

            # A*
            successors = grid.get_neighbours(current_node.state)

            # Itera sobre el diccionario succesors y desempaqueta cada par clave/valor
            for key, value in successors.items():
                
                #get cost
                new_cost = current_node.cost + grid.get_cost(value)
                # Get the successor
                new_state = value

                # Check if the successor is not reached
                if new_state not in explored or new_cost < explored[new_state]:

                    # Initialize the son node
                    new_node = Node("", state=new_state,
                                    cost=new_cost,
                                    parent=current_node, action=key)
                    new_node.estimated_distance = AStarSearch.heuristic(value, grid.end)

                    # Mark the successor as reached
                    explored[new_state] = new_cost

                    # Add the new node to the frontier
                    frontier.add(new_node, new_node.cost + new_node.estimated_distance)

    @staticmethod
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        """Calcula la distancia Manhattan entre dos puntos.
        Puedes experimentar con otras heurísticas como la distancia euclídea.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Otra heurística posible (distancia euclídea):
        # return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)