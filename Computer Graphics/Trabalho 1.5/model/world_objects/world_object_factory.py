import re

from model.world_objects.world_curve import WorldCurve
from model.world_objects.world_line import WorldLine
from model.world_objects.world_point import WorldPoint
from model.world_objects.world_wireframe import WorldWireframe
from utils.bounds import Bounds


class WorldObjectFactory:
    """
    Uma classe de fábrica para instanciar objetos no mundo
    """

    viewport_bounds: Bounds = None

    @classmethod
    def new_world_object(
        cls,
        points: list,
        name: str,
        color: tuple,
        display_file: list,
        is_filled: bool,
        object_type: str,
    ):
        """
        Cria um novo objeto do mundo a partir de uma lista de pontos.
        """

        if any(
            points == [(x, y) for x, y, *_ in objs.world_points]
            for objs in display_file
        ):
            return None

        kwargs = {
            "points": points,
            "color": color,
            "viewport_bounds": cls.viewport_bounds,
        }

        if object_type == "Point":
            obj_type = WorldPoint
        elif object_type == "Line":
            obj_type = WorldLine
        elif object_type == "Wireframe":
            obj_type = WorldWireframe
            kwargs["is_filled"] = is_filled
        elif object_type == "Curve":
            obj_type = WorldCurve
        else:
            raise ValueError(f"Tipo de objeto inválido: {object_type}")

        if not name:
            obj_type_name = obj_type.__name__.replace("World", "")

            highest_index = 0
            pattern = re.compile(rf"^{obj_type_name} (\d+)$")

            for obj in display_file:
                if obj.__class__.__name__.replace("World", "") == obj_type_name:
                    match = pattern.match(obj.name)
                    if match:
                        index = int(match.group(1))
                        highest_index = max(highest_index, index)

            name = f"{obj_type_name} {highest_index + 1}"

        kwargs["name"] = name

        return obj_type(**kwargs)

    @classmethod
    def read_obj_file(cls, filepath: str) -> list:
        """
        Realiza o parsing de um arquivo Wavefront OBJ, extraindo informações sobre objetos.
        @param filepath: Caminho do arquivo OBJ a ser lido.
        @return: Lista de objetos lidos do arquivo OBJ. Formato: [nome: str, pontos: list, preenchimento: bool].
        """

        def add_object():
            if (
                current_object_points
            ):  # Adiciona o último objeto lido se ele tiver pontos

                tam = len(current_object_points)

                if tam == 2:
                    obj_type = "Line"
                elif tam > 2:
                    obj_type = "Wireframe"
                else:
                    obj_type = "Point"

                if (
                    obj_type == "Wireframe"
                    and not current_fill_state
                    and current_object_points[0] == current_object_points[-1]
                ):  # Se o objeto não for preenchido, remove o último ponto
                    current_object_points.pop()

                objects_list.append(
                    [
                        current_object_name,
                        current_object_points,
                        current_fill_state,
                        obj_type,
                    ]
                )

        vertices = []  # Armazena todos os vértices (x, y) lidos
        objects_list = []  # Lista final [nome, [(x,y), ...]]
        current_object_name = "Object 0"  # Nome padrão se nenhum 'o' for encontrado
        current_object_points = []  # Pontos (x,y) do objeto atual
        current_fill_state = False  # Estado de preenchimento

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

                    elif command == "o":  # Define um novo objeto

                        add_object()

                        current_object_name = (
                            " ".join(parts[1:])
                            if len(parts) > 1
                            else f"Object {len(objects_list) + 1}"
                        )

                        current_fill_state = False
                        current_object_points = []

                    elif command in (
                        "f",
                        "l",
                        "p",
                    ):  # Define uma face ou linha ou ponto

                        if command == "f":
                            current_fill_state = True

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
            add_object()

        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        except Exception as e:
            raise Exception(f"Erro ao processar o arquivo {filepath}: {e}")

        return objects_list

    @classmethod
    def new_objects_from_file(cls, filepath: str, display_file: list) -> list:
        """
        Lê um arquivo OBJ e cria novos objetos do mundo a partir dele.

        @param filepath: Caminho do arquivo OBJ a ser lido.
        @param display_file: Lista de objetos do mundo já existentes.
        @returns: Uma lista de objetos do mundo criados e uma lista de objetos que foram pulados
        (porque já existem no display_file).
        """

        objects_list = cls.read_obj_file(filepath)
        world_objects = []
        skipped_objects = []

        for obj_data in objects_list:
            obj_name = obj_data[0]
            obj_points = obj_data[1]
            obj_is_filled = obj_data[2]
            obj_type = obj_data[3]

            world_object = cls.new_world_object(
                points=obj_points,
                name=obj_name,
                color=(0, 0, 0),
                display_file=display_file,
                is_filled=obj_is_filled,
                object_type=obj_type,
            )

            if world_object is None:
                skipped_objects.append(obj_name)
            else:
                world_objects.append(world_object)

        return world_objects, skipped_objects
