from abc import ABC

from model.clipping_algorithms import ClippingAlgorithms
from model.world_objects.world_object import WorldObject


class SCWorldObject(WorldObject, ABC):
    """
    SCWorldObject - Switchable Clipping World Object
    Classe para objetos cujo algoritmo de clipping pode ser alterado.
    """

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: object,
    ) -> None:
        super().__init__(points, name, color, viewport_bounds)

        self.clipping_modes = {
            "cohen_sutherland": ClippingAlgorithms.cohen_sutherland_clipping,
            "liang_barsky": ClippingAlgorithms.liang_barsky_clipping,
        }
        self.clipping_mode = ClippingAlgorithms.cohen_sutherland_clipping

    def change_clipping_mode(self, mode: str) -> None:
        """
        Muda o modo de clipping. O atributo self.clipping_modes é um dicionário que mapeia
        nomes de modos de clipping para funções de clipping, e self.clipping_mode é a função de clipping atual.
        @param mode: Modo de clipping.
        """

        try:
            self.clipping_mode = self.clipping_modes[mode]
        except KeyError as e:
            raise ValueError(f"Modo de clipping inválido: {mode}") from e
