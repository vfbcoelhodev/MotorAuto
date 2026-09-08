import pytest

from motorauto.application.services.cliente import (
    buscar_cliente_por_id,
    cadastrar_cliente,
)
from motorauto.domain.entities.cliente import Cliente
from motorauto.infrastructure.repositories.cliente_memoria import (
    RepositorioClienteEmMemoria,
)


@pytest.fixture
def repositorio() -> RepositorioClienteEmMemoria:
    return RepositorioClienteEmMemoria()


def test_deve_cadastrar_cliente(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        "João",
        "31999999999",
    )

    assert isinstance(cliente, Cliente)
    assert cliente.nome == "João"
    assert cliente.telefone == "31999999999"


def test_deve_adicionar_cliente_ao_repositorio(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        "João",
        "31999999999",
    )

    assert repositorio.listar() == (cliente,)


def test_cliente_cadastrado_deve_receber_id(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        "João",
        "31999999999",
    )

    assert cliente.id == 1


def test_deve_gerar_ids_sequenciais_ao_cadastrar_clientes(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    primeiro = cadastrar_cliente(
        repositorio,
        "João",
        "31999999999",
    )

    segundo = cadastrar_cliente(
        repositorio,
        "Maria",
        "31988888888",
    )

    assert primeiro.id == 1
    assert segundo.id == 2


def test_deve_cadastrar_cliente_com_dados_opcionais(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        "João",
        "31999999999",
        possui_whatsapp=True,
        cpf="12345678900",
        endereco="Rua A, 100",
        observacoes="Cliente preferencial.",
    )

    assert cliente.possui_whatsapp is True
    assert cliente.cpf == "12345678900"
    assert cliente.endereco == "Rua A, 100"
    assert cliente.observacoes == "Cliente preferencial."


def test_nao_deve_cadastrar_cliente_sem_nome(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    with pytest.raises(ValueError):
        cadastrar_cliente(
            repositorio,
            "   ",
            "31999999999",
        )

    assert repositorio.listar() == ()


def test_nao_deve_cadastrar_cliente_sem_telefone(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    with pytest.raises(ValueError):
        cadastrar_cliente(
            repositorio,
            "João",
            "   ",
        )

    assert repositorio.listar() == ()


def test_deve_buscar_cliente_por_id(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        "João",
        "31999999999",
    )

    assert cliente.id is not None
    
    cliente_encontrado = buscar_cliente_por_id(
        repositorio,
        cliente.id,
    )

    assert cliente_encontrado is cliente


def test_buscar_cliente_por_id_deve_rejeitar_id_inexistente(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    with pytest.raises(ValueError):
        buscar_cliente_por_id(
            repositorio,
            999,
        )


def test_buscar_cliente_por_id_deve_rejeitar_tipo_invalido(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    with pytest.raises(TypeError):
        buscar_cliente_por_id(
            repositorio,
            "1",  # ty: ignore[invalid-argument-type]
        )


def test_buscar_cliente_por_id_deve_rejeitar_bool(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    with pytest.raises(TypeError):
        buscar_cliente_por_id(
            repositorio,
            True,
        )


@pytest.mark.parametrize(
    "cliente_id",
    [
        0,
        -1,
        -100,
    ],
)
def test_buscar_cliente_por_id_deve_rejeitar_id_nao_positivo(
    repositorio: RepositorioClienteEmMemoria,
    cliente_id: int,
) -> None:
    with pytest.raises(ValueError):
        buscar_cliente_por_id(
            repositorio,
            cliente_id,
        )