import numpy as np

def load_obj(filename):
    """
    Φορτώνει αρχείο .obj και επιστρέφει flatten πίνακα vertices και indices.
    Υποστηρίζει μόνο κορυφές (v) και πρόσωπα (f), αγνοεί υλικά, normals, UVs.
    Κάνει triangulation όταν υπάρχουν περισσότερες από 3 κορυφές σε ένα face.
    """
    raw_vertices = []
    indices = []
    unique_vertices = []
    vertex_dict = {}

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertex = tuple(map(float, parts[1:4]))
                raw_vertices.append(vertex)

        # Επαναδιαβάζουμε για τα faces
        f.seek(0)
        for line in f:
            if line.startswith('f '):
                parts = line.strip().split()[1:]
                face_indices = []
                for part in parts:
                    idx = int(part.split('/')[0]) - 1
                    vertex = raw_vertices[idx]

                    # Επαναχρησιμοποιούμε τα ίδια vertices
                    if vertex not in vertex_dict:
                        vertex_dict[vertex] = len(unique_vertices)
                        unique_vertices.append(vertex)
                    face_indices.append(vertex_dict[vertex])

                # Triangulation μέσω "fan method"
                for i in range(1, len(face_indices) - 1):
                    indices.extend([
                        face_indices[0],
                        face_indices[i],
                        face_indices[i + 1]
                    ])

    vertices = np.array(unique_vertices, dtype=np.float32).flatten()
    indices = np.array(indices, dtype=np.uint32)

    return vertices, indices
