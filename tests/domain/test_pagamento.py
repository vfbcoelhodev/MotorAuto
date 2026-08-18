from datetime import UTC, datetime
from decimal import Decimal

import pytest

from motorauto.domain.entities.pagamento import Pagamento
from motorauto.domain.enums.forma_pagamento import FormaPagamento


@pytest.fixture
def pagamento() -> Pagamento:
    return Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )


def test_deve_criar_pagamento_com_valor_valido(pagamento: Pagamento) -> None:
    assert pagamento.valor == Decimal("300.00")


def test_deve_criar_pagamento_com_forma_pagamento_valida(pagamento: Pagamento) -> None:
    assert pagamento.forma_pagamento is FormaPagamento.PIX


def test_pagamento_deve_iniciar_sem_observacoes(pagamento: Pagamento) -> None:
    assert pagamento.observacoes is None


def test_pagamento_deve_gerar_data_automaticamente(pagamento: Pagamento) -> None:
    assert isinstance(pagamento.data_pagamento, datetime)


def test_nao_deve_criar_pagamento_com_valor_zero() -> None:
    with pytest.raises(ValueError):
        Pagamento(
            _valor=Decimal("0.00"),
            _forma_pagamento=FormaPagamento.PIX,
        )


def test_nao_deve_criar_pagamento_com_valor_negativo() -> None:
    with pytest.raises(ValueError):
        Pagamento(
            _valor=Decimal("-0.01"),
            _forma_pagamento=FormaPagamento.PIX,
        )


def test_nao_deve_criar_pagamento_com_valor_float() -> None:
    with pytest.raises(TypeError):
        Pagamento(
            _valor=300.0,  # ty: ignore[invalid-argument-type]
            _forma_pagamento=FormaPagamento.PIX,
        )


def test_nao_deve_criar_pagamento_com_forma_pagamento_invalida() -> None:
    with pytest.raises(TypeError):
        Pagamento(
            _valor=Decimal("300.00"),
            _forma_pagamento="Pix",  # ty: ignore[invalid-argument-type]
        )


def test_deve_normalizar_observacoes_vazias_para_none() -> None:
    pagamento = Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
        _observacoes="   ",
    )

    assert pagamento.observacoes is None


def test_deve_normalizar_observacoes_removendo_espacos() -> None:
    pagamento = Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
        _observacoes="  Entrada recebida  ",
    )

    assert pagamento.observacoes == "Entrada recebida"


def test_nao_deve_criar_pagamento_com_observacoes_de_tipo_invalido() -> None:
    with pytest.raises(TypeError):
        Pagamento(
            _valor=Decimal("300.00"),
            _forma_pagamento=FormaPagamento.PIX,
            _observacoes=123,  # ty: ignore[invalid-argument-type]
        )


def test_data_pagamento_deve_corresponder_ao_momento_da_criacao() -> None:
    antes = datetime.now(UTC)

    pagamento = Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    depois = datetime.now(UTC)

    assert antes <= pagamento.data_pagamento <= depois

