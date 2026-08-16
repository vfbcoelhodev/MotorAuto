from decimal import Decimal

import pytest

from motorauto.domain.entities.item_peca import ItemPeca
from motorauto.domain.enums.situacao_aprovacao_item import SituacaoAprovacaoItem


@pytest.fixture
def item_peca() -> ItemPeca:
    return ItemPeca(
        _descricao="Filtro de óleo",
        _quantidade=Decimal("1.0"),
        _valor_unitario=Decimal("30.00"),
    )


def test_deve_criar_item_peca_com_descricao_valida(item_peca: ItemPeca) -> None:
    assert item_peca.descricao == "Filtro de óleo"


def test_deve_criar_item_peca_com_quantidade_valida(item_peca: ItemPeca) -> None:
    assert item_peca.quantidade == Decimal("1.0")


def test_deve_criar_item_peca_com_valor_unitario_valido(item_peca: ItemPeca) -> None:
    assert item_peca.valor_unitario == Decimal("30.00")


def test_item_peca_deve_iniciar_pendente(item_peca: ItemPeca) -> None:
    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_nao_deve_criar_item_peca_com_descricao_vazia() -> None:
    with pytest.raises(ValueError):
        ItemPeca(
            _descricao="",
            _quantidade=Decimal("1.0"),
            _valor_unitario=Decimal("30.00"),
        )


def test_nao_deve_criar_item_peca_com_quantidade_negativa() -> None:
    with pytest.raises(ValueError):
        ItemPeca(
            _descricao="Filtro de óleo",
            _quantidade=Decimal("-1.0"),
            _valor_unitario=Decimal("30.00"),
        )


def test_nao_deve_criar_item_peca_com_valor_unitario_negativo() -> None:
    with pytest.raises(ValueError):
        ItemPeca(
            _descricao="Filtro de óleo",
            _quantidade=Decimal("1.0"),
            _valor_unitario=Decimal("-30.00"),
        )


def test_nao_deve_criar_item_peca_com_quantidade_zero() -> None:
    with pytest.raises(ValueError):
        ItemPeca(
            _descricao="Filtro de óleo",
            _quantidade=Decimal("0.0"),
            _valor_unitario=Decimal("30.00"),
        )


def test_deve_aceitar_item_peca_com_valor_unitario_zero() -> None:
    item = ItemPeca(
        _descricao="Peça em garantia",
        _quantidade=Decimal("1.0"),
        _valor_unitario=Decimal("0.00"),
    )

    assert item.valor_unitario == Decimal("0.00")


def test_nao_deve_criar_item_peca_com_quantidade_float() -> None:
    with pytest.raises(TypeError):
        ItemPeca(
            _descricao="Filtro de óleo",
            _quantidade=1.0,  # ty: ignore[invalid-argument-type]
            _valor_unitario=Decimal("30.00"),
        )


def test_deve_calcular_subtotal_do_item_peca() -> None:
    item = ItemPeca(
        _descricao="Óleo do motor",
        _quantidade=Decimal("4.0"),
        _valor_unitario=Decimal("35.00"),
    )

    assert item.subtotal == Decimal("140.000")


def test_deve_calcular_subtotal_com_quantidade_fracionada() -> None:
    item = ItemPeca(
        _descricao="Produto por quantidade fracionada",
        _quantidade=Decimal("1.5"),
        _valor_unitario=Decimal("20.00"),
    )

    assert item.subtotal == Decimal("30.000")


def test_deve_corrigir_descricao_do_item_peca(item_peca: ItemPeca) -> None:
    item_peca.corrigir_descricao("Filtro de combustível")

    assert item_peca.descricao == "Filtro de combustível"


def test_nao_deve_corrigir_descricao_com_valor_vazio(item_peca: ItemPeca) -> None:
    with pytest.raises(ValueError):
        item_peca.corrigir_descricao("")

    assert item_peca.descricao == "Filtro de óleo"


def test_deve_alterar_quantidade_do_item_peca(item_peca: ItemPeca) -> None:
    item_peca.alterar_quantidade(Decimal("2.0"))

    assert item_peca.quantidade == Decimal("2.0")
    assert item_peca.subtotal == Decimal("60.00")


def test_nao_deve_alterar_quantidade_para_zero(item_peca: ItemPeca) -> None:
    with pytest.raises(ValueError):
        item_peca.alterar_quantidade(Decimal("0.0"))

    assert item_peca.quantidade == Decimal("1.0")


def test_nao_deve_alterar_quantidade_para_negativa(item_peca: ItemPeca) -> None:
    with pytest.raises(ValueError):
        item_peca.alterar_quantidade(Decimal("-1.0"))

    assert item_peca.quantidade == Decimal("1.0")


def test_deve_alterar_valor_unitario_do_item_peca(item_peca: ItemPeca) -> None:
    item_peca.alterar_valor_unitario(Decimal("40.00"))

    assert item_peca.valor_unitario == Decimal("40.00")
    assert item_peca.subtotal == Decimal("40.00")


def test_deve_permitir_alterar_valor_unitario_para_zero(item_peca: ItemPeca) -> None:
    item_peca.alterar_valor_unitario(Decimal("0.00"))

    assert item_peca.valor_unitario == Decimal("0.00")
    assert item_peca.subtotal == Decimal("0.00")


def test_nao_deve_alterar_valor_unitario_para_negativo(item_peca: ItemPeca) -> None:
    with pytest.raises(ValueError):
        item_peca.alterar_valor_unitario(Decimal("-0.01"))

    assert item_peca.valor_unitario == Decimal("30.00")


def test_deve_aprovar_item_peca(item_peca: ItemPeca) -> None:
    item_peca.aprovar()

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.APROVADO
    )


def test_deve_recusar_item_peca(item_peca: ItemPeca) -> None:
    item_peca.recusar()

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.RECUSADO
    )


def test_deve_voltar_item_peca_aprovado_para_pendente(item_peca: ItemPeca) -> None:
    item_peca.aprovar()
    item_peca.marcar_como_pendente()

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_deve_voltar_item_peca_recusado_para_pendente(item_peca: ItemPeca) -> None:
    item_peca.recusar()
    item_peca.marcar_como_pendente()

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_deve_permitir_item_peca_aprovado_ser_recusado(item_peca: ItemPeca) -> None:
    item_peca.aprovar()
    item_peca.recusar()

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.RECUSADO
    )


def test_deve_permitir_item_peca_recusado_ser_aprovado(item_peca: ItemPeca) -> None:
    item_peca.recusar()
    item_peca.aprovar()

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.APROVADO
    )


def test_nao_deve_alterar_quantidade_usando_float(item_peca: ItemPeca) -> None:
    with pytest.raises(TypeError):
        item_peca.alterar_quantidade(
            2.0,  # ty: ignore[invalid-argument-type]
        )

    assert item_peca.quantidade == Decimal("1.0")


def test_nao_deve_alterar_valor_unitario_usando_float(item_peca: ItemPeca) -> None:
    with pytest.raises(TypeError):
        item_peca.alterar_valor_unitario(
            40.0,  # ty: ignore[invalid-argument-type]
        )

    assert item_peca.valor_unitario == Decimal("30.00")