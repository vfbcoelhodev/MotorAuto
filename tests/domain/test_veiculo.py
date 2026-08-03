import pytest

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.veiculo import Veiculo


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="Victor",
        _telefone="31999999999",
    )


@pytest.fixture
def veiculo(cliente: Cliente) -> Veiculo:
    return Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Uno",
    )

def test_deve_criar_veiculo_com_marca_valida(veiculo: Veiculo,) -> None:
    assert veiculo.marca == "Fiat"

def test_deve_criar_veiculo_com_modelo_valido(veiculo: Veiculo,) -> None:
    assert veiculo.modelo == "Uno"

def test_deve_criar_veiculo_com_cliente_valido(veiculo: Veiculo,) -> None:
    assert veiculo.cliente.nome == "Victor"

def test_veiculo_deve_iniciar_sem_placa(veiculo: Veiculo) -> None:
    assert veiculo.placa is None

def test_veiculo_deve_iniciar_sem_ano(veiculo: Veiculo) -> None:
    assert veiculo.ano is None

def test_veiculo_deve_iniciar_sem_combustivel(veiculo: Veiculo) -> None:
    assert veiculo.combustivel is None

def test_veiculo_deve_iniciar_sem_observacoes(veiculo: Veiculo) -> None:
    assert veiculo.observacoes is None

def test_deve_corrigir_marca_do_veiculo(veiculo: Veiculo) -> None:
    veiculo.corrigir_marca("Chevrolet")
    assert veiculo.marca == "Chevrolet"

def test_deve_corrigir_modelo_do_veiculo(veiculo: Veiculo) -> None:
    veiculo.corrigir_modelo("Corsa")
    assert veiculo.modelo == "Corsa"

def test_deve_corrigir_ano_do_veiculo(veiculo: Veiculo) -> None:
    veiculo.corrigir_ano(2020)
    assert veiculo.ano == 2020

def test_deve_atualizar_placa_do_veiculo(veiculo: Veiculo) -> None:
    veiculo.atualizar_placa("ABC1234")
    assert veiculo.placa == "ABC1234"

def test_deve_atualizar_combustivel_do_veiculo(veiculo: Veiculo) -> None:
    veiculo.atualizar_combustivel("Gasolina")
    assert veiculo.combustivel == "Gasolina"

def test_deve_atualizar_observacoes_do_veiculo(veiculo: Veiculo) -> None:
    veiculo.atualizar_observacoes("Veículo em bom estado")
    assert veiculo.observacoes == "Veículo em bom estado"

def test_deve_transferir_propriedade_do_veiculo(veiculo: Veiculo) -> None:
    novo_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )
    veiculo.transferir_propriedade(novo_cliente)
    assert veiculo.cliente.nome == "Maria"

def test_nao_deve_criar_veiculo_sem_marca(cliente: Cliente) -> None:
    with pytest.raises(ValueError):
        Veiculo(
            _cliente=cliente,
            _marca="",
            _modelo="Uno",
        )

def test_nao_deve_criar_veiculo_sem_modelo(cliente: Cliente) -> None:
    with pytest.raises(ValueError):
        Veiculo(
            _cliente=cliente,
            _marca="Fiat",
            _modelo="",
        )

def test_nao_deve_criar_veiculo_com_cliente_invalido() -> None:
    with pytest.raises(TypeError):
        Veiculo(
            _cliente="Cliente inválido",  # type: ignore
            _marca="Fiat",
            _modelo="Uno",
        )
