import pytest

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.veiculo import Veiculo
from motorauto.infrastructure.repositories.veiculo_memoria import (
    RepositorioVeiculoEmMemoria,
)


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="João",
        _telefone="31999999999",
    )


@pytest.fixture
def repositorio() -> RepositorioVeiculoEmMemoria:
    return RepositorioVeiculoEmMemoria()


def test_deve_adicionar_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    repositorio.adicionar(veiculo)

    assert repositorio.listar() == (veiculo,)


def test_deve_gerar_id_ao_adicionar_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    repositorio.adicionar(veiculo)

    assert veiculo.id == 1


def test_deve_gerar_ids_sequenciais(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    primeiro = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    segundo = Veiculo(
        _cliente=cliente,
        _marca="Volkswagen",
        _modelo="Gol",
    )

    repositorio.adicionar(primeiro)
    repositorio.adicionar(segundo)

    assert primeiro.id == 1
    assert segundo.id == 2


def test_deve_buscar_veiculo_por_id(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    repositorio.adicionar(veiculo)

    assert veiculo.id is not None

    veiculo_encontrado = repositorio.buscar_por_id(veiculo.id)

    assert veiculo_encontrado is veiculo


def test_buscar_por_id_deve_retornar_none_quando_veiculo_nao_existir(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    veiculo = repositorio.buscar_por_id(999)

    assert veiculo is None


def test_listar_deve_retornar_tuple(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    veiculos = repositorio.listar()

    assert isinstance(veiculos, tuple)


def test_adicionar_deve_rejeitar_objeto_que_nao_seja_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        TypeError,
        match="O veículo informado deve ser do tipo Veiculo.",
    ):
        repositorio.adicionar(
            "veículo inválido"  # ty: ignore[invalid-argument-type]
        )


def test_adicionar_deve_rejeitar_mesma_instancia_duas_vezes(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    repositorio.adicionar(veiculo)

    with pytest.raises(
        ValueError,
        match="O veículo informado já foi adicionado ao repositório.",
    ):
        repositorio.adicionar(veiculo)


def test_adicionar_deve_rejeitar_veiculo_que_ja_possui_id(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )
    veiculo.id = 10

    with pytest.raises(
        ValueError,
        match="Não é possível adicionar um veículo que já possui ID.",
    ):
        repositorio.adicionar(veiculo)


def test_deve_atualizar_veiculo_existente(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )
    repositorio.adicionar(veiculo)

    assert veiculo.id is not None

    veiculo_atualizado = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio Weekend",
    )
    veiculo_atualizado.id = veiculo.id

    repositorio.atualizar(veiculo_atualizado)

    veiculo_encontrado = repositorio.buscar_por_id(veiculo.id)

    assert veiculo_encontrado is veiculo_atualizado


def test_atualizar_deve_rejeitar_objeto_que_nao_seja_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        TypeError,
        match="O veículo informado deve ser do tipo Veiculo.",
    ):
        repositorio.atualizar(
            "veículo inválido"  # ty: ignore[invalid-argument-type]
        )


def test_atualizar_deve_rejeitar_veiculo_sem_id(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    with pytest.raises(
        ValueError,
        match="O veículo informado deve possuir ID.",
    ):
        repositorio.atualizar(veiculo)


def test_atualizar_deve_rejeitar_veiculo_com_id_inexistente(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )
    veiculo.id = 999

    with pytest.raises(
        ValueError,
        match="Veículo não encontrado no repositório.",
    ):
        repositorio.atualizar(veiculo)


