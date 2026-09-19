from typing import Protocol

from motorauto.domain.entities.veiculo import Veiculo


class RepositorioVeiculo(Protocol):
    def adicionar(self, veiculo: Veiculo) -> None:
        ...

    def buscar_por_id(self, veiculo_id: int) -> Veiculo | None:
        ...

    def listar(self) -> tuple[Veiculo, ...]:
        ...

    def atualizar(self, veiculo: Veiculo) -> None:
        ...