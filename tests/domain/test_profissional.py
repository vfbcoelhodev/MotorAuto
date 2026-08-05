import pytest

from motorauto.domain.entities.profissional import Profissional
from motorauto.domain.enums.funcao_profissional import FuncaoProfissional


@pytest.fixture
def profissional() -> Profissional:
    return Profissional(
        _nome="Victor",
        _telefone="31999999999",
        _funcao=FuncaoProfissional.MECANICO,
    )


def test_deve_criar_profissional_com_nome_valido(profissional: Profissional) -> None:
    assert profissional.nome == "Victor"


def test_deve_criar_profissional_com_telefone_valido(profissional: Profissional) -> None:
    assert profissional.telefone == "31999999999"


def test_deve_criar_profissional_com_funcao_valida(profissional: Profissional) -> None:
    assert profissional.funcao == FuncaoProfissional.MECANICO


def test_deve_iniciar_profissional_sem_observacoes(profissional: Profissional) -> None:
    assert profissional.observacoes is None


def test_profissional_deve_iniciar_ativo(profissional: Profissional) -> None:
    assert profissional.ativo is True


def test_nao_deve_criar_profissional_com_nome_vazio() -> None:
    with pytest.raises(ValueError):
        Profissional(
            _nome="",
            _telefone="31999999999",
            _funcao=FuncaoProfissional.MECANICO,
        )


def test_nao_deve_criar_profissional_com_telefone_vazio() -> None:
    with pytest.raises(ValueError):
        Profissional(
            _nome="Victor",
            _telefone="",
            _funcao=FuncaoProfissional.MECANICO,
        )


def test_nao_deve_criar_profissional_com_funcao_invalida() -> None:
    with pytest.raises(TypeError):
        Profissional(
            _nome="Victor",
            _telefone="31999999999",
            _funcao="Invalido",  # ty: ignore[invalid-argument-type]        
            )


def test_deve_atualizar_nome_do_profissional(
    profissional: Profissional,
) -> None:
    profissional.atualizar_nome("Novo Nome")

    assert profissional.nome == "Novo Nome"


def test_nao_deve_atualizar_nome_do_profissional_com_nome_vazio(
    profissional: Profissional,
) -> None:
    with pytest.raises(ValueError):
        profissional.atualizar_nome("")

    assert profissional.nome == "Victor"


def test_deve_atualizar_telefone_do_profissional(
    profissional: Profissional,
) -> None:
    profissional.atualizar_telefone("31888888888")

    assert profissional.telefone == "31888888888"


def test_nao_deve_atualizar_telefone_do_profissional_com_telefone_vazio(
    profissional: Profissional,
) -> None:
    with pytest.raises(ValueError):
        profissional.atualizar_telefone("")

    assert profissional.telefone == "31999999999"


def test_deve_alterar_funcao_do_profissional(
    profissional: Profissional,
) -> None:
    profissional.alterar_funcao(FuncaoProfissional.GERENTE)

    assert profissional.funcao is FuncaoProfissional.GERENTE


def test_nao_deve_alterar_funcao_do_profissional_com_tipo_invalido(
    profissional: Profissional,
) -> None:
    with pytest.raises(TypeError):
        profissional.alterar_funcao(
            "Invalido",  # ty: ignore[invalid-argument-type]
        )

    assert profissional.funcao is FuncaoProfissional.MECANICO


def test_deve_atualizar_observacoes_do_profissional(
    profissional: Profissional,
) -> None:
    profissional.atualizar_observacoes("Novas observações")

    assert profissional.observacoes == "Novas observações"


def test_deve_normalizar_observacoes_vazias_para_none(
    profissional: Profissional,
) -> None:
    profissional.atualizar_observacoes("")

    assert profissional.observacoes is None


def test_deve_desativar_profissional(
    profissional: Profissional,
) -> None:
    profissional.desativar()

    assert profissional.ativo is False


def test_deve_ativar_profissional(
    profissional: Profissional,
) -> None:
    profissional.desativar()
    profissional.ativar()

    assert profissional.ativo is True
