from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = node.cost
        
        # Return if the node contains a goal state
        #if node.state == grid.end:
         #   return Solution(node, explored)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = PriorityQueueFrontier()
        frontier.add(node)


        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            # BFS
            successors = grid.get_neighbours(node.state)

            # Itera sobre el diccionario succesors y desempaqueta cada par clave/valor
            for key, value in successors.items():
                
                #get cost
                new_cost = grid.get_cost(value) + grid.get_cost(node)
                # Get the successor
                new_state = value

                # Check if the successor is not reached
                if new_state not in explored or new_cost < explored[new_state]:

                    # Initialize the son node
                    new_node = Node("", new_state,
                                    new_cost,
                                    parent=node, action=value)

                    # Mark the successor as reached
                    explored[new_state] = new_cost

                    # Return if the node contains a goal state
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    #if new_state == grid.end:
                     #   return Solution(new_node, explored)

                    # Add the new node to the frontier
                    #if grid.get_cost(new_node.state) <= node.cost:
                    frontier.add(new_node, new_cost)
                    #else:
                        #frontier.add(new_node)
                    


