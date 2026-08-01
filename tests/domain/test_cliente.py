import pytest

from motorauto.domain.entities.cliente import Cliente


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="Victor",
        _telefone="31999999999",
    )

def test_deve_criar_cliente_com_nome_valido(cliente: Cliente) -> None:
    #Assert
    assert cliente.nome == "Victor"

def test_cliente_deve_iniciar_ativo(cliente: Cliente) -> None:
   #Assert
    assert cliente.ativo is True

def test_deve_criar_cliente_com_telefone_valido(cliente: Cliente) -> None:
    #Assert
    assert cliente.telefone == "31999999999"

def test_nao_deve_criar_cliente_sem_telefone() -> None:
    #Act
    with pytest.raises(ValueError):
        Cliente(
            _nome="Victor",
            _telefone="",
        )

def test_deve_atualizar_nome_do_cliente(cliente: Cliente) -> None:
    #Act
    cliente.atualizar_nome("Novo Nome")

    #Assert
    assert cliente.nome == "Novo Nome"

def test_nao_deve_atualizar_cliente_com_nome_invalido(cliente: Cliente) -> None:
    #Act
    with pytest.raises(ValueError):
        cliente.atualizar_nome("")

    #Assert
    assert cliente.nome == "Victor"

def test_deve_atualizar_telefone_do_cliente(cliente: Cliente) -> None:
    #Act
    cliente.atualizar_telefone("31988888888")

    #Assert
    assert cliente.telefone == "31988888888"

def test_nao_deve_atualizar_cliente_com_telefone_invalido(cliente: Cliente) -> None:
    #Act
    with pytest.raises(ValueError):
        cliente.atualizar_telefone("")

    #Assert
    assert cliente.telefone == "31999999999"
