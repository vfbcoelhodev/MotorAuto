from decimal import Decimal

import pytest

from motorauto.domain.entities.item_servico import ItemServico
from motorauto.domain.enums.situacao_aprovacao_item import SituacaoAprovacaoItem


@pytest.fixture
def item_servico() -> ItemServico:
    return ItemServico(
        _descricao="Troca de óleo",
        _valor=Decimal("60.00"),
    )


def test_deve_criar_item_servico_com_descricao_valida(item_servico: ItemServico) -> None:
    assert item_servico.descricao == "Troca de óleo"


def test_deve_criar_item_servico_com_valor_valido(item_servico: ItemServico) -> None:
    assert item_servico.valor == Decimal("60.00")


def test_item_servico_deve_iniciar_pendente(item_servico: ItemServico) -> None:
    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_item_servico_deve_iniciar_nao_executado(item_servico: ItemServico) -> None:
    assert item_servico.executado is False


def test_nao_deve_criar_item_servico_com_descricao_vazia() -> None:
    with pytest.raises(ValueError):
        ItemServico(
            _descricao="",
            _valor=Decimal("60.00"),
        )


def test_nao_deve_criar_item_servico_com_valor_negativo() -> None:
    with pytest.raises(ValueError):
        ItemServico(
            _descricao="Troca de óleo",
            _valor=Decimal("-0.01"),
        )


def test_deve_aceitar_item_servico_com_valor_zero() -> None:
    item = ItemServico(
        _descricao="Serviço em garantia",
        _valor=Decimal("0.00"),
    )

    assert item.valor == Decimal("0.00")


def test_nao_deve_criar_item_servico_com_float() -> None:
    with pytest.raises(TypeError):
        ItemServico(
            _descricao="Troca de óleo",
            _valor=60.0,  # ty: ignore[invalid-argument-type]
        )


def test_deve_aprovar_item_servico(item_servico: ItemServico) -> None:
    item_servico.aprovar()

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.APROVADO
    )


def test_deve_recusar_item_servico(item_servico: ItemServico) -> None:
    item_servico.recusar()

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.RECUSADO
    )


def test_deve_marcar_item_servico_como_pendente(item_servico: ItemServico) -> None:
    item_servico.aprovar()
    item_servico.marcar_como_pendente()

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_deve_marcar_item_servico_aprovado_como_executado(item_servico: ItemServico) -> None:
    item_servico.aprovar()
    item_servico.marcar_como_executado()

    assert item_servico.executado is True


def test_nao_deve_executar_item_servico_pendente(item_servico: ItemServico) -> None:
    with pytest.raises(ValueError):
        item_servico.marcar_como_executado()

    assert item_servico.executado is False


def test_nao_deve_executar_item_servico_recusado(item_servico: ItemServico) -> None:
    item_servico.recusar()

    with pytest.raises(ValueError):
        item_servico.marcar_como_executado()

    assert item_servico.executado is False


def test_nao_deve_alterar_aprovacao_de_item_executado(item_servico: ItemServico) -> None:
    item_servico.aprovar()
    item_servico.marcar_como_executado()

    with pytest.raises(ValueError):
        item_servico.recusar()

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.APROVADO
    )
    assert item_servico.executado is True


def test_deve_corrigir_descricao_do_item_servico(item_servico: ItemServico) -> None:
    item_servico.corrigir_descricao("Troca do filtro de óleo")

    assert item_servico.descricao == "Troca do filtro de óleo"


def test_nao_deve_corrigir_descricao_com_valor_vazio(item_servico: ItemServico) -> None:
    with pytest.raises(ValueError):
        item_servico.corrigir_descricao("")

    assert item_servico.descricao == "Troca de óleo"


def test_deve_alterar_valor_do_item_servico(item_servico: ItemServico) -> None:
    item_servico.alterar_valor(Decimal("80.00"))

    assert item_servico.valor == Decimal("80.00")


def test_deve_permitir_alterar_valor_para_zero(item_servico: ItemServico) -> None:
    item_servico.alterar_valor(Decimal("0.00"))

    assert item_servico.valor == Decimal("0.00")


def test_nao_deve_alterar_valor_para_negativo(item_servico: ItemServico) -> None:
    with pytest.raises(ValueError):
        item_servico.alterar_valor(Decimal("-0.01"))

    assert item_servico.valor == Decimal("60.00")


def test_nao_deve_alterar_valor_usando_float(item_servico: ItemServico) -> None:
    with pytest.raises(TypeError):
        item_servico.alterar_valor(
            80.0,  # ty: ignore[invalid-argument-type]
        )

    assert item_servico.valor == Decimal("60.00")

