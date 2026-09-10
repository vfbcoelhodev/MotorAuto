import pytest

from motorauto.application.services.cliente import (
    atualizar_cliente,
    buscar_cliente_por_id,
    cadastrar_cliente,
    listar_clientes,
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


def test_listar_clientes_deve_retornar_tupla_vazia(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    clientes = listar_clientes(repositorio)

    assert clientes == ()


def test_deve_listar_clientes_cadastrados(
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

    clientes = listar_clientes(repositorio)

    assert clientes == (
        primeiro,
        segundo,
    )


def test_atualizar_cliente_deve_alterar_endereco(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        endereco="Rua Antiga",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        endereco="Rua Nova",
    )

    assert cliente_atualizado.endereco == "Rua Nova"


def test_atualizar_cliente_deve_remover_endereco_quando_none_for_informado(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        endereco="Rua Antiga",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        endereco=None,
    )

    assert cliente_atualizado.endereco is None


def test_atualizar_cliente_deve_manter_endereco_quando_nao_for_informado(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        endereco="Rua Antiga",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
    )

    assert cliente_atualizado.endereco == "Rua Antiga"


def test_atualizar_cliente_deve_alterar_cpf(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        cpf="11111111111",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        cpf="22222222222",
    )

    assert cliente_atualizado.cpf == "22222222222"


def test_atualizar_cliente_deve_remover_cpf(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        cpf="11111111111",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        cpf=None,
    )

    assert cliente_atualizado.cpf is None


def test_atualizar_cliente_deve_alterar_observacoes(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        observacoes="Cliente antigo",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        observacoes="Cliente preferencial",
    )

    assert cliente_atualizado.observacoes == "Cliente preferencial"


def test_atualizar_cliente_deve_remover_observacoes(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        observacoes="Cliente antigo",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        observacoes=None,
    )

    assert cliente_atualizado.observacoes is None


def test_atualizar_cliente_deve_alterar_nome(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        nome="João da Silva",
    )

    assert cliente_atualizado.nome == "João da Silva"


def test_atualizar_cliente_deve_alterar_telefone(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        telefone="31888888888",
    )

    assert cliente_atualizado.telefone == "31888888888"


def test_atualizar_cliente_deve_ativar_whatsapp(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        possui_whatsapp=False,
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        possui_whatsapp=True,
    )

    assert cliente_atualizado.possui_whatsapp is True


def test_atualizar_cliente_deve_desativar_whatsapp(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        possui_whatsapp=True,
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        possui_whatsapp=False,
    )

    assert cliente_atualizado.possui_whatsapp is False


def test_atualizar_cliente_deve_manter_campos_nao_informados(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
        possui_whatsapp=True,
    )

    assert cliente.id is not None

    cliente_atualizado = atualizar_cliente(
        repositorio,
        cliente_id=cliente.id,
        nome="João da Silva",
    )

    assert cliente_atualizado.nome == "João da Silva"
    assert cliente_atualizado.telefone == "31999999999"
    assert cliente_atualizado.possui_whatsapp is True


def test_atualizar_cliente_nao_deve_manter_alteracao_parcial_em_caso_de_erro(
    repositorio: RepositorioClienteEmMemoria,
) -> None:
    cliente = cadastrar_cliente(
        repositorio,
        nome="João",
        telefone="31999999999",
    )

    assert cliente.id is not None

    with pytest.raises(
        ValueError,
        match="O campo telefone é obrigatório.",
    ):
        atualizar_cliente(
            repositorio,
            cliente_id=cliente.id,
            nome="João da Silva",
            telefone="   ",
        )

    cliente_encontrado = buscar_cliente_por_id(
        repositorio,
        cliente.id,
    )

    assert cliente_encontrado.nome == "João"
    assert cliente_encontrado.telefone == "31999999999"