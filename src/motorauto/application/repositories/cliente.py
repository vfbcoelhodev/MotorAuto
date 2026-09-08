from typing import Protocol

from motorauto.domain.entities.cliente import Cliente


class RepositorioCliente(Protocol):
    def adicionar(self, cliente: Cliente) -> None:
        ...

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        ...

    def listar(self) -> tuple[Cliente, ...]:
        ...