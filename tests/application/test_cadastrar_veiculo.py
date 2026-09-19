import pytest

from motorauto.application.services.veiculo import (
    atualizar_veiculo,
    buscar_veiculo_por_id,
    cadastrar_veiculo,
    corrigir_dados_veiculo,
    listar_veiculos,
    transferir_propriedade_veiculo,
)
from motorauto.domain.entities.cliente import Cliente
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


def test_deve_cadastrar_veiculo_com_dados_obrigatorios(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
    )

    assert veiculo.id == 1
    assert veiculo.cliente is cliente
    assert veiculo.marca == "Fiat"
    assert veiculo.modelo == "Palio"

    assert repositorio.buscar_por_id(1) is veiculo


def test_deve_cadastrar_veiculo_com_dados_opcionais(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Volkswagen",
        modelo="Gol",
        ano=2020,
        placa="abc-1d23",
        combustivel="Flex",
        observacoes="Veículo bem conservado",
    )

    assert veiculo.ano == 2020
    assert veiculo.placa == "ABC1D23"
    assert veiculo.combustivel == "Flex"
    assert veiculo.observacoes == "Veículo bem conservado"


def test_deve_buscar_veiculo_por_id(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
    )

    assert veiculo.id is not None

    veiculo_encontrado = buscar_veiculo_por_id(
        repositorio,
        veiculo.id,
    )

    assert veiculo_encontrado is veiculo


def test_buscar_veiculo_por_id_deve_rejeitar_id_inexistente(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        ValueError,
        match="Veículo não encontrado.",
    ):
        buscar_veiculo_por_id(
            repositorio,
            999,
        )


def test_buscar_veiculo_por_id_deve_rejeitar_id_que_nao_seja_int(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        TypeError,
        match="O ID do veículo deve ser do tipo int.",
    ):
        buscar_veiculo_por_id(
            repositorio,
            "1",  # ty: ignore[invalid-argument-type]
        )


def test_buscar_veiculo_por_id_deve_rejeitar_bool(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        TypeError,
        match="O ID do veículo deve ser do tipo int.",
    ):
        buscar_veiculo_por_id(
            repositorio,
            True,
        )


def test_buscar_veiculo_por_id_deve_rejeitar_id_zero(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        ValueError,
        match="O ID do veículo deve ser maior que zero.",
    ):
        buscar_veiculo_por_id(
            repositorio,
            0,
        )


def test_buscar_veiculo_por_id_deve_rejeitar_id_negativo(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    with pytest.raises(
        ValueError,
        match="O ID do veículo deve ser maior que zero.",
    ):
        buscar_veiculo_por_id(
            repositorio,
            -1,
        )


def test_deve_listar_veiculos_quando_repositorio_estiver_vazio(
    repositorio: RepositorioVeiculoEmMemoria,
) -> None:
    veiculos = listar_veiculos(repositorio)

    assert veiculos == ()


def test_deve_listar_veiculos_cadastrados(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    primeiro = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
    )

    segundo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Volkswagen",
        modelo="Gol",
    )

    veiculos = listar_veiculos(repositorio)

    assert veiculos == (primeiro, segundo)


def test_deve_atualizar_placa_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        placa="ABC1234",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        placa="def-5g67",
    )

    assert veiculo_atualizado.placa == "DEF5G67"


def test_deve_remover_placa_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        placa="ABC1234",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        placa=None,
    )

    assert veiculo_atualizado.placa is None


def test_deve_atualizar_combustivel_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        combustivel="Gasolina",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        combustivel="Flex",
    )

    assert veiculo_atualizado.combustivel == "Flex"


def test_deve_remover_combustivel_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        combustivel="Gasolina",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        combustivel=None,
    )

    assert veiculo_atualizado.combustivel is None


def test_deve_atualizar_observacoes_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        observacoes="Observação antiga",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        observacoes="Nova observação",
    )

    assert veiculo_atualizado.observacoes == "Nova observação"


def test_deve_remover_observacoes_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        observacoes="Alguma observação",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        observacoes=None,
    )

    assert veiculo_atualizado.observacoes is None


def test_atualizar_veiculo_deve_preservar_campos_nao_informados(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        placa="ABC1234",
        combustivel="Gasolina",
        observacoes="Observação original",
    )

    assert veiculo.id is not None

    veiculo_atualizado = atualizar_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        placa="DEF5678",
    )

    assert veiculo_atualizado.placa == "DEF5678"
    assert veiculo_atualizado.combustivel == "Gasolina"
    assert veiculo_atualizado.observacoes == "Observação original"


def test_atualizar_veiculo_deve_manter_estado_original_se_alteracao_falhar(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        placa="ABC1234",
        combustivel="Gasolina",
    )

    assert veiculo.id is not None

    with pytest.raises(TypeError, match="O valor informado deve ser do tipo str ou None."):
        atualizar_veiculo(
            repositorio=repositorio,
            veiculo_id=veiculo.id,
            placa="DEF5678",
            combustivel=123,  # ty: ignore[invalid-argument-type]
        )

    veiculo_armazenado = repositorio.buscar_por_id(veiculo.id)

    assert veiculo_armazenado is not None
    assert veiculo_armazenado.placa == "ABC1234"
    assert veiculo_armazenado.combustivel == "Gasolina"
    

def test_deve_corrigir_marca_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
    )

    assert veiculo.id is not None

    veiculo_corrigido = corrigir_dados_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        marca="Volkswagen",
    )

    assert veiculo_corrigido.marca == "Volkswagen"


def test_deve_corrigir_modelo_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Pálio",
    )

    assert veiculo.id is not None

    veiculo_corrigido = corrigir_dados_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        modelo="Palio",
    )

    assert veiculo_corrigido.modelo == "Palio"


def test_deve_corrigir_ano_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        ano=2017,
    )

    assert veiculo.id is not None

    veiculo_corrigido = corrigir_dados_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        ano=2018,
    )

    assert veiculo_corrigido.ano == 2018


def test_deve_remover_ano_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        ano=2018,
    )

    assert veiculo.id is not None

    veiculo_corrigido = corrigir_dados_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        ano=None,
    )

    assert veiculo_corrigido.ano is None


def test_corrigir_dados_veiculo_deve_preservar_campos_nao_informados(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        ano=2018,
    )

    assert veiculo.id is not None

    veiculo_corrigido = corrigir_dados_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        modelo="Palio Weekend",
    )

    assert veiculo_corrigido.marca == "Fiat"
    assert veiculo_corrigido.modelo == "Palio Weekend"
    assert veiculo_corrigido.ano == 2018


def test_corrigir_dados_veiculo_deve_manter_estado_original_se_correcao_falhar(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
        ano=2018,
    )

    assert veiculo.id is not None

    with pytest.raises(
        ValueError,
        match="O ano do veículo deve estar entre 1886 e 2100.",
    ):
        corrigir_dados_veiculo(
            repositorio=repositorio,
            veiculo_id=veiculo.id,
            marca="Fiat Automóveis",
            ano=1800,
        )

    veiculo_armazenado = repositorio.buscar_por_id(veiculo.id)

    assert veiculo_armazenado is not None
    assert veiculo_armazenado.marca == "Fiat"
    assert veiculo_armazenado.ano == 2018


def test_deve_transferir_propriedade_do_veiculo(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
    )

    novo_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )

    assert veiculo.id is not None

    veiculo_transferido = transferir_propriedade_veiculo(
        repositorio=repositorio,
        veiculo_id=veiculo.id,
        novo_cliente=novo_cliente,
    )

    assert veiculo_transferido.cliente is novo_cliente

    veiculo_armazenado = repositorio.buscar_por_id(veiculo.id)

    assert veiculo_armazenado is not None
    assert veiculo_armazenado.cliente is novo_cliente


def test_transferir_propriedade_deve_rejeitar_novo_cliente_invalido(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    veiculo = cadastrar_veiculo(
        repositorio=repositorio,
        cliente=cliente,
        marca="Fiat",
        modelo="Palio",
    )

    assert veiculo.id is not None

    with pytest.raises(
        TypeError,
        match="O veículo deve estar associado a um cliente válido.",
    ):
        transferir_propriedade_veiculo(
            repositorio=repositorio,
            veiculo_id=veiculo.id,
            novo_cliente="Maria",  # ty: ignore[invalid-argument-type]
        )

    assert veiculo.cliente is cliente


def test_transferir_propriedade_deve_rejeitar_veiculo_inexistente(
    repositorio: RepositorioVeiculoEmMemoria,
    cliente: Cliente,
) -> None:
    novo_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )

    with pytest.raises(
        ValueError,
        match="Veículo não encontrado.",
    ):
        transferir_propriedade_veiculo(
            repositorio=repositorio,
            veiculo_id=999,
            novo_cliente=novo_cliente,
        )


