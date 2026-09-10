from motorauto.domain.entities.cliente import Cliente


class RepositorioClienteEmMemoria:
    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._proximo_id = 1


    def adicionar(self, cliente: Cliente) -> None:
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "O cliente informado deve ser do tipo Cliente."
            )

        if any(
            cliente_existente is cliente
            for cliente_existente in self._clientes
        ):
            raise ValueError(
                "O cliente informado já foi adicionado ao repositório."
            )

        if cliente.id is not None:
            raise ValueError(
                "Não é possível adicionar um cliente que já possui ID."
            )

        cliente.id = self._proximo_id
        self._proximo_id += 1

        self._clientes.append(cliente)

    
    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        for cliente in self._clientes:
            if cliente.id == cliente_id:
                return cliente

        return None
    

    def listar(self) -> tuple[Cliente, ...]:
        return tuple(self._clientes)
    

    def atualizar(self, cliente: Cliente) -> None:
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "O cliente informado deve ser do tipo Cliente."
            )

        if cliente.id is None:
            raise ValueError(
                "O cliente informado deve possuir ID."
            )

        for i, cliente_existente in enumerate(self._clientes):
            if cliente_existente.id == cliente.id:
                self._clientes[i] = cliente
                return
     
        raise ValueError(
        "Cliente não encontrado no repositório."
        )