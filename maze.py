class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):


        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = dict()
            self.vertices[vertex_id]["n"] = None
            self.vertices[vertex_id]["s"] = None
            self.vertices[vertex_id]["e"] = None
            self.vertices[vertex_id]["w"] = None

    def add_edge(self, vertex1_id, vertex2_id, direction):

        if vertex2_id not in self.vertices:
            self.add_vertex(vertex2_id)

        self.vertices[vertex1_id][direction] = vertex2_id

        reverse_direction = opposite_directions[direction]
        self.vertices[vertex2_id][reverse_direction] = vertex1_id

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def find_shortest_sequence_of_nodes_between(self, starting_vertex, destination_vertex):

        vertices_to_visit = Queue()
        vertices_to_visit.enqueue(starting_vertex)
        paths_to_vertices = dict()
        paths_to_vertices[starting_vertex] = []
        vertices_already_visited = set()

        while vertices_to_visit.size() > 0:

            current_vertex = vertices_to_visit.dequeue()

            if current_vertex not in vertices_already_visited:
                vertices_already_visited.add(current_vertex)
                neighbor_data = self.get_neighbors(current_vertex)

                for direction in neighbor_data:
                    neighbor = neighbor_data[direction]

                    if neighbor is not None:
                        if neighbor == destination_vertex:
                            final_path = paths_to_vertices[current_vertex][:]
                            final_path.append(current_vertex)
                            final_path.append(neighbor)
                        vertices_to_visit.enqueue(neighbor)
                        copy_of_path_to_parent = paths_to_vertices[current_vertex][:]
                        copy_of_path_to_parent.append(current_vertex)
                        paths_to_vertices[neighbor] = copy_of_path_to_parent

        # target not found
        print("Vertex", destination_vertex, "was not found.")
        return

opposite_directions = dict()
opposite_directions["n"] = "s"
opposite_directions["s"] = "n"
opposite_directions["e"] = "w"
opposite_directions["w"] = "e"


def traverse_maze(player):

    maze = Graph()
    traversal_path = []
    visited_rooms = dict()
    rooms_to_visit = Stack()

    new_room = player.current_room
    rooms_to_visit.push(new_room)

    previous_room = None

    while rooms_to_visit.size() > 0:

        new_room = rooms_to_visit.pop()
        if new_room.id not in visited_rooms:
            if previous_room is not None:

                is_valid_direct_connection = False
                exit_to_use = None

                for exit_direction in previous_room.get_exits():

                    adjoining_room = previous_room.get_room_in_direction(exit_direction)

                    if adjoining_room.id == new_room.id:
                        is_valid_direct_connection = True
                        exit_to_use = exit_direction

                if not is_valid_direct_connection:
                    path_between_rooms = maze.find_shortest_sequence_of_nodes_between(previous_room.id, new_room.id)

                    traversal_path = traversal_path + path_between_rooms

            visited_rooms[new_room.id] = new_room

            maze.add_vertex(new_room.id)

            traversal_path.append(new_room.id)

            for exit_direction in new_room.get_exits():

                adjoining_room = new_room.get_room_in_direction(exit_direction)

                maze.add_edge(new_room.id, adjoining_room.id, exit_direction)

                rooms_to_visit.push(adjoining_room)

            previous_room = new_room

    traversal_directions = []

    for i in range(0, len(traversal_path) - 1):

        previous_room = traversal_path[i]
        current_room = traversal_path[i + 1]

        neighbor_data = maze.get_neighbors(previous_room)

        for direction in neighbor_data:

            if neighbor_data[direction] == current_room:
                traversal_directions.append(direction)

    print(traversal_path)
    print(traversal_directions)
    print("done")

    dead_ends = dict()

    for room in visited_rooms:

        neighbor_data = maze.get_neighbors(room)
        actual_neighbors = []

        for direction in neighbor_data:
            neighbor = neighbor_data[direction]

            if neighbor is not None:
                actual_neighbors.append(neighbor)

        path_from_dead_end = []

        while len(actual_neighbors) == 1:

            prev_room = room
            room = actual_neighbors[0]

            neighbor_data = maze.get_neighbors(room)
            actual_neighbors = []

            for direction in neighbor_data:
                neighbor = neighbor_data[direction]

                if neighbor is not None and neighbor != prev_room:
                    actual_neighbors.append(neighbor)

            path_from_dead_end.append(prev_room)

        if len(path_from_dead_end) > 0:

            path_to_dead_end = path_from_dead_end[1:]
            path_to_dead_end.reverse()

            dead_ends[prev_room] = path_to_dead_end + path_from_dead_end

    print("Passage costs:", dead_ends)

    return traversal_path, traversal_directions
