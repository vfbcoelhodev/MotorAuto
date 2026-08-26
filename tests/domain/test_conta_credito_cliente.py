from decimal import Decimal

import pytest

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.conta_credito_cliente import (
    ContaCreditoCliente,
)
from motorauto.domain.entities.movimentacao_credito_cliente import (
    MovimentacaoCreditoCliente,
)
from motorauto.domain.entities.ordem_servico import OrdemServico
from motorauto.domain.entities.veiculo import Veiculo
from motorauto.domain.enums.forma_pagamento import FormaPagamento
from motorauto.domain.enums.tipo_movimentacao_credito import (
    TipoMovimentacaoCredito,
)


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="João da Silva",
        _telefone="31999999999",
    )


@pytest.fixture
def conta(cliente: Cliente) -> ContaCreditoCliente:
    return ContaCreditoCliente(
        _cliente=cliente,
    )


def test_deve_criar_conta_para_cliente(
    conta: ContaCreditoCliente,
    cliente: Cliente,
) -> None:
    assert conta.cliente is cliente


def test_conta_deve_iniciar_sem_movimentacoes(
    conta: ContaCreditoCliente,
) -> None:
    assert conta.movimentacoes == ()


def test_conta_deve_iniciar_com_saldo_zero(
    conta: ContaCreditoCliente,
) -> None:
    assert conta.saldo == Decimal("0.00")


def test_nao_deve_criar_conta_com_cliente_invalido() -> None:
    with pytest.raises(TypeError):
        ContaCreditoCliente(
            _cliente="João",  # ty: ignore[invalid-argument-type]
        )

    
def test_deve_registrar_credito(
    conta: ContaCreditoCliente,
) -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    conta.registrar_credito(movimentacao)

    assert conta.movimentacoes == (movimentacao,)
    assert conta.saldo == Decimal("500.00")


def test_deve_acumular_multiplos_creditos(
    conta: ContaCreditoCliente,
) -> None:
    credito_pix = MovimentacaoCreditoCliente(
        _valor=Decimal("300.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    credito_dinheiro = MovimentacaoCreditoCliente(
        _valor=Decimal("200.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.DINHEIRO,
    )

    conta.registrar_credito(credito_pix)
    conta.registrar_credito(credito_dinheiro)

    assert conta.saldo == Decimal("500.00")
    assert conta.movimentacoes == (
        credito_pix,
        credito_dinheiro,
    )


def test_registrar_credito_deve_rejeitar_movimentacao_de_devolucao(
    conta: ContaCreditoCliente,
) -> None:
    movimentacao = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
        _forma_origem=FormaPagamento.PIX,
    )

    with pytest.raises(ValueError):
        conta.registrar_credito(movimentacao)

    assert conta.saldo == Decimal("0.00")
    assert conta.movimentacoes == ()


def test_registrar_credito_deve_rejeitar_tipo_invalido(
    conta: ContaCreditoCliente,
) -> None:
    with pytest.raises(TypeError):
        conta.registrar_credito(
            "movimentacao invalida",  # ty: ignore[invalid-argument-type]
        )

    assert conta.movimentacoes == ()


def test_deve_registrar_devolucao(
    conta: ContaCreditoCliente,
) -> None:
    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )
    devolucao = MovimentacaoCreditoCliente(
        _valor=Decimal("200.00"),
        _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
        _forma_origem=FormaPagamento.PIX,
    )

    conta.registrar_credito(credito)
    conta.registrar_devolucao(devolucao)

    assert conta.saldo == Decimal("300.00")


def test_nao_deve_devolver_valor_maior_que_saldo(
    conta: ContaCreditoCliente,
) -> None:
    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("200.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )
    devolucao = MovimentacaoCreditoCliente(
        _valor=Decimal("300.00"),
        _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
        _forma_origem=FormaPagamento.PIX,
    )

    conta.registrar_credito(credito)

    with pytest.raises(ValueError):
        conta.registrar_devolucao(devolucao)

    assert conta.saldo == Decimal("200.00")
    assert conta.movimentacoes == (credito,)


def test_deve_utilizar_credito_em_os_do_mesmo_cliente(
    conta: ContaCreditoCliente,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Barulho na suspensão.",
    )

    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    uso_em_os = MovimentacaoCreditoCliente(
        _valor=Decimal("300.00"),
        _tipo=TipoMovimentacaoCredito.USO_EM_OS,
        _ordem_servico=ordem_servico,
    )

    conta.registrar_credito(credito)
    conta.utilizar_credito_em_os(uso_em_os)

    assert conta.saldo == Decimal("200.00")
    assert conta.movimentacoes == (
        credito,
        uso_em_os,
    )


def test_nao_deve_utilizar_credito_maior_que_saldo(
    conta: ContaCreditoCliente,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Barulho na suspensão.",
    )

    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("200.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    uso_em_os = MovimentacaoCreditoCliente(
        _valor=Decimal("300.00"),
        _tipo=TipoMovimentacaoCredito.USO_EM_OS,
        _ordem_servico=ordem_servico,
    )

    conta.registrar_credito(credito)

    with pytest.raises(ValueError):
        conta.utilizar_credito_em_os(uso_em_os)

    assert conta.saldo == Decimal("200.00")
    assert conta.movimentacoes == (credito,)


def test_nao_deve_utilizar_credito_em_os_de_outro_cliente(
    conta: ContaCreditoCliente,
) -> None:
    outro_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )

    outro_veiculo = Veiculo(
        _cliente=outro_cliente,
        _marca="Volkswagen",
        _modelo="Gol",
    )

    outra_os = OrdemServico(
        _cliente=outro_cliente,
        _veiculo=outro_veiculo,
        _defeito_relatado="Motor falhando.",
    )

    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    uso_em_os = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.USO_EM_OS,
        _ordem_servico=outra_os,
    )

    conta.registrar_credito(credito)

    with pytest.raises(ValueError):
        conta.utilizar_credito_em_os(uso_em_os)

    assert conta.saldo == Decimal("500.00")
    assert conta.movimentacoes == (credito,)


def test_utilizar_credito_em_os_deve_rejeitar_tipo_incorreto(
    conta: ContaCreditoCliente,
) -> None:
    devolucao = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
        _forma_origem=FormaPagamento.PIX,
    )

    with pytest.raises(ValueError):
        conta.utilizar_credito_em_os(devolucao)


def test_registrar_devolucao_deve_rejeitar_tipo_incorreto(
    conta: ContaCreditoCliente,
) -> None:
    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    with pytest.raises(ValueError):
        conta.registrar_devolucao(credito)


def test_deve_permitir_utilizar_todo_o_saldo(
    conta: ContaCreditoCliente,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Barulho na suspensão.",
    )

    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    uso = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.USO_EM_OS,
        _ordem_servico=ordem_servico,
    )

    conta.registrar_credito(credito)
    conta.utilizar_credito_em_os(uso)

    assert conta.saldo == Decimal("0.00")


def test_deve_registrar_ajuste_os_e_aumentar_saldo(
    conta: ContaCreditoCliente,
    cliente: Cliente,
) -> None:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )

    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Barulho na suspensão.",
    )

    ajuste = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.AJUSTE_OS,
        _ordem_servico=ordem_servico,
    )

    conta.registrar_ajuste_os(ajuste)

    assert conta.saldo == Decimal("100.00")
    assert conta.movimentacoes == (ajuste,)


def test_nao_deve_registrar_ajuste_os_de_outro_cliente(
    conta: ContaCreditoCliente,
) -> None:
    outro_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )

    outro_veiculo = Veiculo(
        _cliente=outro_cliente,
        _marca="Volkswagen",
        _modelo="Gol",
    )

    outra_os = OrdemServico(
        _cliente=outro_cliente,
        _veiculo=outro_veiculo,
        _defeito_relatado="Motor falhando.",
    )

    ajuste = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.AJUSTE_OS,
        _ordem_servico=outra_os,
    )

    with pytest.raises(ValueError):
        conta.registrar_ajuste_os(ajuste)

    assert conta.saldo == Decimal("0.00")
    assert conta.movimentacoes == ()


def test_registrar_ajuste_os_deve_rejeitar_tipo_incorreto(
    conta: ContaCreditoCliente,
) -> None:
    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("100.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    with pytest.raises(ValueError):
        conta.registrar_ajuste_os(credito)
        