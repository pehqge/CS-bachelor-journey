from model.world_object import WorldObject


class ObjHandler:
    """Classe que descreve um objeto gráfico."""

    def __init__(self):
        pass

    def read_obj_file(self, filepath: str) -> list[list]:
        """
        Lê um arquivo Wavefront OBJ e extrai informações de objetos.
        """

        vertices = []  # Armazena todos os vértices (x, y) lidos
        objects_list = []  # Lista final [nome, [(x,y), ...]]
        current_object_name = "Object 0"  # Nome padrão se nenhum 'o' for encontrado
        current_object_points = []  # Pontos (x,y) do objeto atual

        try:
            with open(filepath, "r") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()
                    command = parts[0].lower()  # tipo do comando

                    if command == "v":  # Define um vértice

                        x = float(parts[1])
                        y = float(parts[2])
                        vertices.append((x, y))

                    elif command == "o":  # Define o nome do objeto

                        if current_object_points:
                            objects_list.append(
                                [current_object_name, current_object_points]
                            )

                        current_object_name = (
                            parts[1]
                            if len(parts) > 1
                            else f"Object {len(objects_list) + 1}"
                        )
                        current_object_points = []

                    elif command in (
                        "f",
                        "l",
                        "p",
                    ):  # Define uma face ou linha ou ponto

                        indices = []
                        for part in parts[1:]:
                            try:
                                indices.append(int(part))
                            except ValueError:
                                break

                        for index in indices:
                            if index > 0:
                                vertex_index = index - 1

                            elif index < 0:
                                vertex_index = index

                            else:
                                raise ValueError(
                                    f"Índice de vértice inválido (0) na linha {line_num}"
                                )

                            current_object_points.append(vertices[vertex_index])

            # Adiciona o último objeto lido se ele tiver pontos
            if current_object_points:
                objects_list.append([current_object_name, current_object_points])

        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        except Exception as e:
            raise Exception(f"Erro ao processar o arquivo {filepath}: {e}")

        return objects_list

    def generate_obj_str(self, objects_list: list[WorldObject]) -> None:
        """Gera uma string .obj a partir de uma lista de objetos."""

        obj_str = ""

        for obj in objects_list:
            obj_str += obj.get_obj_description()

        return obj_str
