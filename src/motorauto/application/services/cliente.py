from copy import deepcopy

from motorauto.application.repositories.cliente import RepositorioCliente
from motorauto.domain.entities.cliente import Cliente


class _NaoInformado:
    pass


_NAO_INFORMADO = _NaoInformado()


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


def listar_clientes(
    repositorio: RepositorioCliente,
) -> tuple[Cliente, ...]:
    return repositorio.listar()


def atualizar_cliente(
    repositorio: RepositorioCliente,
    cliente_id: int,
    nome: str | _NaoInformado = _NAO_INFORMADO,
    telefone: str | _NaoInformado = _NAO_INFORMADO,
    possui_whatsapp: bool | _NaoInformado = _NAO_INFORMADO,
    endereco: str | None | _NaoInformado = _NAO_INFORMADO,
    observacoes: str | None | _NaoInformado = _NAO_INFORMADO,
    cpf: str | None | _NaoInformado = _NAO_INFORMADO,
) -> Cliente:
    cliente_atual = buscar_cliente_por_id(
        repositorio,
        cliente_id,
    )

    cliente = deepcopy(cliente_atual)

    if not isinstance(nome, _NaoInformado):
        cliente.atualizar_nome(nome)

    if not isinstance(telefone, _NaoInformado):
        cliente.atualizar_telefone(telefone)

    if not isinstance(possui_whatsapp, _NaoInformado):
        if possui_whatsapp:
            cliente.ativar_whatsapp()
        else:
            cliente.desativar_whatsapp()

    if not isinstance(endereco, _NaoInformado):
        cliente.atualizar_endereco(endereco)

    if not isinstance(observacoes, _NaoInformado):
        cliente.atualizar_observacoes(observacoes)

    if not isinstance(cpf, _NaoInformado):
        cliente.atualizar_cpf(cpf)

    repositorio.atualizar(cliente)

    return cliente
   

def ativar_cliente(
    repositorio: RepositorioCliente,
    cliente_id: int,
) -> Cliente:
    cliente = buscar_cliente_por_id(
        repositorio,
        cliente_id,
    )

    cliente.ativar()
    repositorio.atualizar(cliente)

    return cliente


def desativar_cliente(
    repositorio: RepositorioCliente,
    cliente_id: int,
) -> Cliente:
    cliente = buscar_cliente_por_id(
        repositorio,
        cliente_id,
    )

    cliente.desativar()
    repositorio.atualizar(cliente)

    return cliente
    