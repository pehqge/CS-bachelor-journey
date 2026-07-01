import re

import numpy as np

from model.world_objects.world_bezier_curve import WorldBezierCurve
from model.world_objects.world_bezier_surface import WorldBezierSurface
from model.world_objects.world_bicubic_surface import WorldBicubicSurface
from model.world_objects.world_bspline_curve import WorldBSplineCurve
from model.world_objects.world_line import WorldLine
from model.world_objects.world_point import WorldPoint
from model.world_objects.world_polygon import WorldPolygon
from model.world_objects.world_wireframe import WorldWireframe
from view.viewport.viewport_bounds import ViewportBounds


class WorldObjectFactory:
    """
    Uma classe de fábrica para instanciar objetos no mundo
    """

    viewport_bounds: ViewportBounds = None

    @classmethod
    def new_world_object(
        cls,
        points: list,
        name: str,
        color: tuple,
        display_file: list,
        is_filled: bool,
        object_type: type,
        edges: list,
    ):
        """
        Cria um novo objeto do mundo a partir de uma lista de pontos.
        """

        if not isinstance(object_type, (WorldBezierSurface, WorldBicubicSurface)):
            if any(
                all(isinstance(p, tuple) and len(p) == 3 for p in points)
                and points == [(x, y, z) for x, y, z, _ in objs.perceived_points]
                for objs in display_file
                if objs.perceived_points and objs.__class__ == object_type
            ):
                return None
        else:
            pass

        kwargs = {
            "points": points,
            "color": color,
            "viewport_bounds": cls.viewport_bounds,
        }

        if object_type == WorldWireframe:  # Único que tem arestas e preenchimento
            kwargs["edges"] = edges
        elif object_type == WorldPolygon:
            kwargs["is_filled"] = is_filled

        if not name:
            obj_type_name = object_type.__name__.replace("World", "")

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

        return object_type(**kwargs)

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
                obj_points = current_object_points

                if current_command == "p":
                    obj_type = WorldPoint
                elif current_command == "l":
                    if tam == 2:
                        obj_type = WorldLine
                    else:
                        obj_type = WorldWireframe
                elif current_command == "f":
                    obj_type = WorldPolygon
                elif current_command == "bezier":
                    obj_type = WorldBezierCurve
                elif current_command == "bspline":
                    obj_type = WorldBSplineCurve
                elif current_command == "bezier_surface":
                    obj_type = WorldBezierSurface
                    if len(current_object_points) % 4 != 0:
                        raise ValueError(
                            f"Objeto {current_object_name} (bezier_surface): número de pontos ({len(current_object_points)}) não é múltiplo de 4."
                        )
                    obj_points = [
                        current_object_points[i : i + 4]
                        for i in range(0, len(current_object_points), 4)
                    ]
                elif current_command == "bicubic_surface":
                    obj_type = WorldBicubicSurface
                    N, M = current_surface_dims
                    obj_points_np = np.array(current_object_points).reshape((N, M, 3))
                    obj_points = obj_points_np.tolist()

                objects_list.append(
                    [
                        current_object_name,
                        obj_points,
                        current_fill_state,
                        obj_type,
                        edges_list,
                    ]
                )

        vertices = []  # Armazena todos os vértices (x, y) lidos
        objects_list = []  # Lista final [nome, [(x,y), ...]]
        current_object_name = "Object 0"  # Nome padrão se nenhum 'o' for encontrado
        current_object_points = []  # Pontos (x,y) do objeto atual
        current_fill_state = False  # Estado de preenchimento
        current_command = None
        current_index = 0
        edges_list = []
        wireframe = False
        current_surface_dims = []

        try:
            with open(filepath, "r") as f:
                all_lines = f.readlines()  # Ler todas as linhas aqui
                for line_num, line_content in enumerate(
                    all_lines, 1
                ):  # Iterar sobre all_lines
                    line = line_content.strip()  # Usar line_content
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()
                    command = parts[0].lower()  # tipo do comando

                    if command == "v":  # Define um vértice

                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3])
                        vertices.append((x, y, z))

                    elif command == "o":  # Define um novo objeto

                        add_object()

                        current_object_name = (
                            " ".join(parts[1:])
                            if len(parts) > 1
                            else f"Object {len(objects_list) + 1}"
                        )

                        current_index = len(vertices) + 1
                        current_fill_state = False
                        current_object_points = []
                        wireframe = False
                        edges_list = []

                    elif command in (
                        "f",
                        "l",
                        "p",
                        "bezier",
                        "bspline",
                        "bezier_surface",
                        "bicubic_surface",
                    ):  # Define uma face ou linha ou ponto ou curva/superfície

                        if command == "f":
                            current_fill_state = True

                        # confere se o comando atual é l e se a proxima linha começa com l
                        # Acessar all_lines e verificar os limites
                        if (
                            command == "l"
                            and (line_num < len(all_lines))
                            and all_lines[line_num].strip().startswith("l")
                        ):  # é um wireframe
                            wireframe = True

                        indices = []
                        parts_iter = iter(parts[1:])
                        if command == "bicubic_surface":
                            try:
                                N_str = next(parts_iter)
                                M_str = next(parts_iter)
                                current_surface_dims = [int(N_str), int(M_str)]
                                if (
                                    current_surface_dims[0] < 4
                                    or current_surface_dims[1] < 4
                                ):
                                    raise ValueError(
                                        "Dimensões N e M devem ser >= 4 para bicubic_surface."
                                    )
                            except (StopIteration, ValueError) as e:
                                raise ValueError(
                                    f"Erro ao ler dimensões N, M para bicubic_surface na linha {line_num}: {e}"
                                )

                        for part in parts_iter:
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

                            if (
                                command != "bicubic_surface"
                                and not vertices[vertex_index] in current_object_points
                            ):
                                current_object_points.append(vertices[vertex_index])
                            elif command == "bicubic_surface":
                                current_object_points.append(vertices[vertex_index])

                        if wireframe:
                            edges_list.append([x - current_index for x in indices])
                        current_command = command

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
            edges_list = obj_data[4]

            world_object = cls.new_world_object(
                points=obj_points,
                name=obj_name,
                color=(0, 0, 0),
                display_file=display_file,
                is_filled=obj_is_filled,
                object_type=obj_type,
                edges=edges_list,
            )

            if world_object is None:
                skipped_objects.append(obj_name)
            else:
                world_objects.append(world_object)

        return world_objects, skipped_objects
