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
        

        # Initialize the frontier with the initial node
        # In this example, the frontier is a priority queue
        frontier = PriorityQueueFrontier()
        frontier.add(node)


        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            current_node = frontier.pop()

            if current_node.state == grid.end:
                return Solution(current_node, explored)

            # UCS
            successors = grid.get_neighbours(current_node.state)

            # Iterate over the dictionary `successors` and unpack each key/value pair
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

                    # Mark the successor as reached
                    explored[new_state] = new_cost

                    # Add the new node to the frontier
                    frontier.add(new_node)