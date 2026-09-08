from motorauto.application.repositories.cliente import RepositorioCliente
from motorauto.domain.entities.cliente import Cliente


def cadastrar_cliente(
    repositorio: RepositorioCliente,
    nome: str,
    telefone: str,
    possui_whatsapp: bool = False,
    cpf: str | None = None,
    endereco: str | None = None,
    observacoes: str | None = None,
) -> Cliente:
    cliente = Cliente(
        _nome=nome,
        _telefone=telefone,
        _possui_whatsapp=possui_whatsapp,
        _cpf=cpf,
        _endereco=endereco,
        _observacoes=observacoes,
    )

    repositorio.adicionar(cliente)

    return cliente


def buscar_cliente_por_id(
    repositorio: RepositorioCliente,
    cliente_id: int,
) -> Cliente:
    if isinstance(cliente_id, bool) or not isinstance(cliente_id, int):
        raise TypeError(
            "O ID do cliente deve ser do tipo int."
        )

    if cliente_id <= 0:
        raise ValueError(
            "O ID do cliente deve ser maior que zero."
        )

    cliente = repositorio.buscar_por_id(cliente_id)

    if cliente is None:
        raise ValueError(
            "Cliente não encontrado."
        )

    return cliente


