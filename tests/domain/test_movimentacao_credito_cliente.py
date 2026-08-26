from datetime import UTC, datetime
from decimal import Decimal

import pytest

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.movimentacao_credito_cliente import (
    MovimentacaoCreditoCliente,
)
from motorauto.domain.entities.ordem_servico import OrdemServico
from motorauto.domain.entities.veiculo import Veiculo
from motorauto.domain.enums.forma_pagamento import FormaPagamento
from motorauto.domain.enums.tipo_movimentacao_credito import TipoMovimentacaoCredito


def test_deve_criar_movimentacao_de_credito_valida() -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    assert movimentacao.valor == Decimal("500.00")
    assert movimentacao.tipo is TipoMovimentacaoCredito.CREDITO
    assert movimentacao.forma_origem is FormaPagamento.PIX
    assert movimentacao.ordem_servico is None


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="João da Silva",
        _telefone="31999999999",
    )


@pytest.fixture
def veiculo(cliente: Cliente) -> Veiculo:
    return Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )


@pytest.fixture
def ordem_servico(
    cliente: Cliente,
    veiculo: Veiculo,
) -> OrdemServico:
    return OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Barulho na suspensão.",
    )


def test_deve_criar_movimentacao_de_devolucao_valida() -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("80.00"),
        _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
        _forma_origem=FormaPagamento.PIX,
    )

    assert movimentacao.tipo is TipoMovimentacaoCredito.DEVOLUCAO
    assert movimentacao.forma_origem is FormaPagamento.PIX
    assert movimentacao.ordem_servico is None


def test_nao_deve_criar_movimentacao_com_valor_zero() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("0.00"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=FormaPagamento.PIX,
        )


def test_nao_deve_criar_movimentacao_com_valor_negativo() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("-0.01"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=FormaPagamento.PIX,
        )


def test_nao_deve_criar_movimentacao_com_valor_float() -> None:
    with pytest.raises(TypeError):
        MovimentacaoCreditoCliente(
            _valor=500.0,  # ty: ignore[invalid-argument-type]
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=FormaPagamento.PIX,
        )

def test_credito_deve_exigir_forma_origem() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("500.00"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=None,
        )


def test_devolucao_deve_exigir_forma_origem() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("80.00"),
            _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
            _forma_origem=None,
        )


def test_nao_deve_usar_credito_cliente_como_forma_origem() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("500.00"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=FormaPagamento.CREDITO_CLIENTE,
        )


def test_movimentacao_deve_gerar_data_automaticamente() -> None:
    antes = datetime.now(UTC)

    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    depois = datetime.now(UTC)

    assert antes <= movimentacao.data <= depois


def test_deve_normalizar_observacoes_vazias_para_none() -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
        _observacoes="   ",
    )

    assert movimentacao.observacoes is None


def test_deve_criar_movimentacao_de_uso_em_os_valida(
    ordem_servico: OrdemServico,
) -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("300.00"),
        _tipo=TipoMovimentacaoCredito.USO_EM_OS,
        _ordem_servico=ordem_servico,
    )

    assert movimentacao.valor == Decimal("300.00")
    assert movimentacao.tipo is TipoMovimentacaoCredito.USO_EM_OS
    assert movimentacao.ordem_servico is ordem_servico
    assert movimentacao.forma_origem is None


def test_uso_em_os_deve_exigir_ordem_servico() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("300.00"),
            _tipo=TipoMovimentacaoCredito.USO_EM_OS,
            _ordem_servico=None,
        )


def test_uso_em_os_nao_deve_aceitar_forma_origem(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("300.00"),
            _tipo=TipoMovimentacaoCredito.USO_EM_OS,
            _forma_origem=FormaPagamento.PIX,
            _ordem_servico=ordem_servico,
        )


def test_credito_nao_deve_aceitar_ordem_servico(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("500.00"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=FormaPagamento.PIX,
            _ordem_servico=ordem_servico,
        )


def test_devolucao_nao_deve_aceitar_ordem_servico(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("80.00"),
            _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
            _forma_origem=FormaPagamento.PIX,
            _ordem_servico=ordem_servico,
        )


def test_nao_deve_criar_movimentacao_com_tipo_invalido() -> None:
    with pytest.raises(TypeError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("100.00"),
            _tipo="Credito",  # ty: ignore[invalid-argument-type]
            _forma_origem=FormaPagamento.PIX,
        )


def test_nao_deve_criar_movimentacao_com_forma_origem_invalida() -> None:
    with pytest.raises(TypeError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("100.00"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem="Pix",  # ty: ignore[invalid-argument-type]
        )


def test_nao_deve_criar_movimentacao_com_observacoes_invalidas() -> None:
    with pytest.raises(TypeError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("100.00"),
            _tipo=TipoMovimentacaoCredito.CREDITO,
            _forma_origem=FormaPagamento.PIX,
            _observacoes=123,  # ty: ignore[invalid-argument-type]
        )


def test_deve_criar_movimentacao_de_ajuste_os_valida(
    ordem_servico: OrdemServico,
) -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.AJUSTE_OS,
        _ordem_servico=ordem_servico,
    )

    assert movimentacao.valor == Decimal("100.00")
    assert movimentacao.tipo is TipoMovimentacaoCredito.AJUSTE_OS
    assert movimentacao.ordem_servico is ordem_servico
    assert movimentacao.forma_origem is None


def test_ajuste_os_deve_exigir_ordem_servico() -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("100.00"),
            _tipo=TipoMovimentacaoCredito.AJUSTE_OS,
            _ordem_servico=None,
        )


def test_ajuste_os_nao_deve_aceitar_forma_origem(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        MovimentacaoCreditoCliente(
            _valor=Decimal("100.00"),
            _tipo=TipoMovimentacaoCredito.AJUSTE_OS,
            _forma_origem=FormaPagamento.PIX,
            _ordem_servico=ordem_servico,
        )
               