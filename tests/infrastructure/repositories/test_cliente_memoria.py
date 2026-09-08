import pytest

from motorauto.application.repositories.cliente import RepositorioCliente
from motorauto.domain.entities.cliente import Cliente
from motorauto.infrastructure.repositories.cliente_memoria import (
    RepositorioClienteEmMemoria,
)


@pytest.fixture
def repositorio() -> RepositorioClienteEmMemoria:
    return RepositorioClienteEmMemoria()


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="João",
        _telefone="31999999999",
    )


def test_deve_adicionar_cliente(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    repositorio.adicionar(cliente)

    assert repositorio.listar() == (cliente,)


def test_deve_gerar_id_ao_adicionar_cliente(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    assert cliente.id is None

    repositorio.adicionar(cliente)

    assert cliente.id == 1


def test_deve_gerar_ids_sequenciais(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    outro_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )

    repositorio.adicionar(cliente)
    repositorio.adicionar(outro_cliente)

    assert cliente.id == 1
    assert outro_cliente.id == 2


def test_deve_buscar_cliente_por_id(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    repositorio.adicionar(cliente)

    cliente_encontrado = repositorio.buscar_por_id(1)

    assert cliente_encontrado is cliente


def test_buscar_por_id_deve_retornar_none_quando_cliente_nao_existir(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente_encontrado = repositorio.buscar_por_id(999)

    assert cliente_encontrado is None


def test_listar_deve_retornar_clientes_como_tupla(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    repositorio.adicionar(cliente)

    clientes = repositorio.listar()

    assert isinstance(clientes, tuple)
    assert clientes == (cliente,)


def test_nao_deve_adicionar_tipo_invalido(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    with pytest.raises(TypeError):
        repositorio.adicionar(
            "cliente inválido",  # ty: ignore[invalid-argument-type]
        )


def test_nao_deve_adicionar_mesmo_cliente_duas_vezes(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    repositorio.adicionar(cliente)

    with pytest.raises(ValueError):
        repositorio.adicionar(cliente)

    assert repositorio.listar() == (cliente,)


def _aceitar_repositorio_cliente(
    repositorio: RepositorioCliente,
) -> RepositorioCliente:
    return repositorio


def test_repositorio_em_memoria_deve_satisfazer_contrato() -> None:
    repositorio = RepositorioClienteEmMemoria()

    repositorio_tipado = _aceitar_repositorio_cliente(
        repositorio
    )

    assert repositorio_tipado is repositorio


def test_nao_deve_adicionar_cliente_que_ja_possui_id(
    repositorio: RepositorioClienteEmMemoria,
    cliente: Cliente,
) -> None:
    cliente.id = 99

    with pytest.raises(ValueError):
        repositorio.adicionar(cliente)

    assert repositorio.listar() == ()
    