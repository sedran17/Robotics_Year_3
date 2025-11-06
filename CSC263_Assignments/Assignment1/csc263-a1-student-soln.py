from typing import List, Dict, Tuple, Optional, Callable
class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        name (str): The label or identifier of the vertex.
        children (Dict[str, Tuple[str, str, float]]): 
            A mapping between child vertex names and edges.
            Each edge is represented as a tuple:
                (source vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None):
        """
        Initializes a Vertex.

        Args:
            name (str): The label or identifier of the vertex.
            children (Optional[Dict[str, Tuple[str, str, float]]]): 
                A mapping between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """
        Returns all edges from this vertex.

        Returns:
            List[Tuple[str, str, float]]: The list of edges from this vertex.
        """
        kids = []
        keys = []
        for key in self.children:
            keys.append(key)
        for i in range(len(self.children)):
            kids.append(self.children[keys[i]])

        return kids

class Graph:
    """
    Represents a graph consisting of multiple vertices.

    Attributes:
        vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """
        Initializes a Graph.
        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """
        Returns all vertices in the graph.

        Returns:
            List[Vertex]: The list of vertices in the graph.
        """
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """
        Checks if vertex v_name is a child of vertex u_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the potential child vertex.

        Returns:
            bool: True if the vertex v_name is a child of the vertex u_name, False otherwise.
        """
        kids = []
        for i in range(len(self.vertices)):
            #print(self.get_vertices()[i].name)
            if self.get_vertices()[i].name == u_name:
                kids = self.get_vertices()[i].get_children()
                #print(kids)

                for kid in kids:
                    if kid[1] == v_name:
                        return True
        return False

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """
        Retrieves the edge between u_name and v_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the child vertex.

        Returns:
            Optional[Tuple[str, str, float]]: The edge if it exists,
            or None if no such edge is found.
        """
        if not self.is_child(u_name, v_name):
            return None
        kids = []
        for i in range(len(self.vertices)):
            if self.get_vertices()[i].name == u_name:
                kids = self.get_vertices()[i].get_children()

                for kid in kids:
                    if kid[1] == v_name:
                        return kid


class Device(Vertex):
    """
    Represents a network device, extending the Vertex class with
    device-specific functionality.

    Attributes:
        name (str): The label or identifier of the device.
        children (Dict[str, Tuple[str, str, float]]):
            A mapping between child device names and nearby devices.
        network (Graph): A graph representing this device's discovered network.
    """

    def __init__(self, name: str):
        """
        Initializes a Device.

        Args:
            name (str): The label or identifier of the device.
        """
        self.name = name
        self.children = {}
        self.network = Graph([self])

    def discover_network(self, find_devices_fn: Callable[[List[str]], List[Tuple[str, str, float]]]) -> None:
        """
        Discovers the surrounding network starting from this device. Once this
        function is called, self.network should contain a representation of the
        device's discovered network.

        Args:
            find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]):
                A function that takes an ordered list of device names (i.e., a path)
                and returns the edges from the last device in the path to its immediate children.
        """

        visited = []
        to_visit = [[self.name]]

        while len(to_visit) > 0:
            path = to_visit.pop(0)
            current = path[-1]
            edges = find_devices_fn(path)
            current_vertex = None

            for v in self.network.vertices:
                if v.name == current:
                    current_vertex = v
                    break

            if current_vertex is None:
                current_vertex = Vertex(current)
                self.network.vertices.append(current_vertex)

            for u, v, w in edges:
                child_vertex = None
                for vx in self.network.vertices:
                    if vx.name == v:
                        child_vertex = vx
                        break

                if child_vertex is None:
                    child_vertex = Vertex(v)
                    self.network.vertices.append(child_vertex)
                current_vertex.children[v] = (u, v, w)

                if v not in visited:
                    to_visit.append(path + [v])

            if current not in visited:
                visited.append(current)


    def find_path(self, d_name: str) -> Optional[List[str]]:
        """
        Finds the cheapest path from this device to the specified target device 
        using the Cheapest-First Search (CFS) algorithm.

        Args:
            d_name (str): The name of the destination device.

        Returns:
            Optional[List[str]]: An ordered list of device names representing the path 
            from this device to the target. If no path exists, returns None.
        """
        open_list = [([self.name], 0.0)]
        cheapest_cost = {}

        while open_list:
            least_path, least_cost = open_list[0]

            for path, cost in open_list:
                if cost < least_cost:
                    least_path = path
                    least_cost = cost

            open_list.remove((least_path, least_cost))

            current = least_path[-1]

            if (current in cheapest_cost) and (cheapest_cost[current] <= least_cost):
                continue
            cheapest_cost[current] = least_cost

            if current == d_name:
                return least_path

            current_vertex = None
            for v in self.network.vertices:
                if v.name == current:
                    current_vertex = v
                    break
            if current_vertex is None:
                continue

            for child_name, edge in current_vertex.children.items():
                _, _, weight = edge
                new_cost = least_cost + weight
                new_path = least_path + [child_name]

                if (child_name not in cheapest_cost) or (new_cost < cheapest_cost[child_name]):
                    open_list.append((new_path, new_cost))

        return None


# ----------------------------------------------------------------------
# Mock function for testing
# ----------------------------------------------------------------------
def find_devices_fn(path: List[str]) -> List[Tuple[str, str, float]]:
    """
    A mock function that simulates network discovery.

    Args:
        path (List[str]): The sequence of device names representing the discovery path.

    Returns:
        List[Tuple[str, str, float]]: A list of edges, where each tuple contains:
            - source device name (str),
            - child device name (str),
            - edge weight (float).
    """
    if not path:
        return []

    last_device = path[-1]

    mock_network = {
        "chandra-s25": [
            ("chandra-s25", "router-051797", 1.0),
            ("chandra-s25", "helen-pc", 2.0),
        ],
        "router-051797": [
            ("router-051797", "ws-102", 1.2),
            ("router-051797", "switch-12", 0.8),
            ("router-051797", "srv-07", 1.0),
        ],
        "helen-pc": [
            ("helen-pc", "ws-14", 1.5),
        ],
    }

    return mock_network.get(last_device, [])
