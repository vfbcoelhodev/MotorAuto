from motorauto.domain.entities.pagamento import Pagamento
from decimal import Decimal

import pytest

from motorauto.application.services.credito_cliente import (
    utilizar_credito_em_os, converter_excedente_os_em_credito, registrar_credito_cliente, devolver_credito_cliente,
)
from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.conta_credito_cliente import ContaCreditoCliente
from motorauto.domain.entities.item_peca import ItemPeca
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
        _nome="João",
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
    os = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Barulho na suspensão.",
    )

    peca = ItemPeca(
        _descricao="Bucha",
        _quantidade=Decimal("1.0"),
        _valor_unitario=Decimal("300.00"),
    )

    os.adicionar_item_peca(peca)
    os.aprovar_item_peca(peca)

    return os


@pytest.fixture
def conta_credito(
    cliente: Cliente,
) -> ContaCreditoCliente:
    conta = ContaCreditoCliente(
        _cliente=cliente,
    )

    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    conta.registrar_credito(credito)

    return conta


def test_deve_utilizar_credito_em_os(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    utilizar_credito_em_os(
        conta_credito,
        ordem_servico,
        Decimal("200.00"),
    )

    assert conta_credito.saldo == Decimal("300.00")
    assert ordem_servico.total_recebido == Decimal("200.00")
    assert ordem_servico.saldo_restante == Decimal("100.00")

    assert conta_credito.movimentacoes[-1].tipo is (
        TipoMovimentacaoCredito.USO_EM_OS
    )

    assert ordem_servico.pagamentos[-1].forma_pagamento is (
        FormaPagamento.CREDITO_CLIENTE
    )


def test_nao_deve_utilizar_credito_de_outro_cliente(
    ordem_servico: OrdemServico,
) -> None:
    outro_cliente = Cliente(
        _nome="Maria",
        _telefone="31988888888",
    )

    conta = ContaCreditoCliente(
        _cliente=outro_cliente,
    )

    credito = MovimentacaoCreditoCliente(
        _valor=Decimal("500.00"),
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=FormaPagamento.PIX,
    )

    conta.registrar_credito(credito)

    with pytest.raises(ValueError):
        utilizar_credito_em_os(
            conta,
            ordem_servico,
            Decimal("100.00"),
        )


def test_nao_deve_utilizar_valor_maior_que_credito_disponivel(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        utilizar_credito_em_os(
            conta_credito,
            ordem_servico,
            Decimal("500.01"),
        )


def test_nao_deve_utilizar_valor_maior_que_saldo_da_os(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        utilizar_credito_em_os(
            conta_credito,
            ordem_servico,
            Decimal("300.01"),
        )


def test_nao_deve_utilizar_credito_com_valor_zero(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        utilizar_credito_em_os(
            conta_credito,
            ordem_servico,
            Decimal("0.00"),
        )


def test_nao_deve_utilizar_credito_com_float(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(TypeError):
        utilizar_credito_em_os(
            conta_credito,
            ordem_servico,
            100.0,  # ty: ignore[invalid-argument-type]
        )


def test_deve_permitir_utilizar_todo_credito_disponivel(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    utilizar_credito_em_os(
        conta_credito,
        ordem_servico,
        Decimal("300.00"),
    )

    assert conta_credito.saldo == Decimal("200.00")
    assert ordem_servico.total_recebido == Decimal("300.00")
    assert ordem_servico.saldo_restante == Decimal("0.00")


def test_deve_permitir_utilizar_todo_saldo_da_conta(
    conta_credito: ContaCreditoCliente,
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Reparo completo.",
    )

    peca = ItemPeca(
        _descricao="Kit de peças",
        _quantidade=Decimal("1.0"),
        _valor_unitario=Decimal("700.00"),
    )

    ordem_servico.adicionar_item_peca(peca)
    ordem_servico.aprovar_item_peca(peca)

    utilizar_credito_em_os(
        conta_credito,
        ordem_servico,
        Decimal("500.00"),
    )

    assert conta_credito.saldo == Decimal("0.00")
    assert ordem_servico.total_recebido == Decimal("500.00")
    assert ordem_servico.saldo_restante == Decimal("200.00")
    

def test_deve_converter_excedente_da_os_em_credito(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    pagamento = Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    ordem_servico.registrar_pagamento(pagamento)

    item = ordem_servico.itens_peca[0]

    ordem_servico.alterar_valor_unitario_item_peca(
        item,
        Decimal("200.00"),
    )

    converter_excedente_os_em_credito(
        conta_credito,
        ordem_servico,
    )

    assert ordem_servico.valor_excedente == Decimal("100.00")
    assert conta_credito.saldo == Decimal("600.00")


def test_nao_deve_converter_o_mesmo_excedente_duas_vezes(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    pagamento = Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    ordem_servico.registrar_pagamento(pagamento)

    item = ordem_servico.itens_peca[0]

    ordem_servico.alterar_valor_unitario_item_peca(
        item,
        Decimal("200.00"),
    )

    converter_excedente_os_em_credito(
        conta_credito,
        ordem_servico,
    )

    with pytest.raises(ValueError):
        converter_excedente_os_em_credito(
            conta_credito,
            ordem_servico,
        )

    assert conta_credito.saldo == Decimal("600.00")


def test_deve_creditar_apenas_nova_diferenca_do_excedente(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    pagamento = Pagamento(
        _valor=Decimal("300.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    ordem_servico.registrar_pagamento(pagamento)

    item = ordem_servico.itens_peca[0]

    ordem_servico.alterar_valor_unitario_item_peca(
        item,
        Decimal("200.00"),
    )

    converter_excedente_os_em_credito(
        conta_credito,
        ordem_servico,
    )

    ordem_servico.alterar_valor_unitario_item_peca(
        item,
        Decimal("150.00"),
    )

    converter_excedente_os_em_credito(
        conta_credito,
        ordem_servico,
    )

    assert ordem_servico.valor_excedente == Decimal("150.00")
    assert conta_credito.saldo == Decimal("650.00")


def test_deve_registrar_credito_cliente_via_pix(
    conta_credito: ContaCreditoCliente,
) -> None:
    saldo_inicial = conta_credito.saldo

    registrar_credito_cliente(
        conta_credito,
        Decimal("200.00"),
        FormaPagamento.PIX,
        "Entrada antecipada.",
    )

    assert conta_credito.saldo == saldo_inicial + Decimal("200.00")

    movimentacao = conta_credito.movimentacoes[-1]

    assert movimentacao.tipo is TipoMovimentacaoCredito.CREDITO
    assert movimentacao.valor == Decimal("200.00")
    assert movimentacao.forma_origem is FormaPagamento.PIX
    assert movimentacao.observacoes == "Entrada antecipada."


def test_deve_registrar_credito_cliente_via_dinheiro(
    conta_credito: ContaCreditoCliente,
) -> None:
    saldo_inicial = conta_credito.saldo

    registrar_credito_cliente(
        conta_credito,
        Decimal("100.00"),
        FormaPagamento.DINHEIRO,
    )

    assert conta_credito.saldo == saldo_inicial + Decimal("100.00")
    assert conta_credito.movimentacoes[-1].forma_origem is (
        FormaPagamento.DINHEIRO
    )


def test_nao_deve_registrar_credito_com_valor_zero(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(ValueError):
        registrar_credito_cliente(
            conta_credito,
            Decimal("0.00"),
            FormaPagamento.PIX,
        )


def test_nao_deve_registrar_credito_com_valor_negativo(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(ValueError):
        registrar_credito_cliente(
            conta_credito,
            Decimal("-10.00"),
            FormaPagamento.PIX,
        )


def test_nao_deve_registrar_credito_com_float(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(TypeError):
        registrar_credito_cliente(
            conta_credito,
            100.0,  # ty: ignore[invalid-argument-type]
            FormaPagamento.PIX,
        )


def test_nao_deve_registrar_credito_usando_credito_cliente_como_origem(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(ValueError):
        registrar_credito_cliente(
            conta_credito,
            Decimal("100.00"),
            FormaPagamento.CREDITO_CLIENTE,
        )

def test_nao_deve_registrar_credito_em_conta_invalida() -> None:
    with pytest.raises(TypeError):
        registrar_credito_cliente(
            "conta invalida",  # ty: ignore[invalid-argument-type]
            Decimal("100.00"),
            FormaPagamento.PIX,
        )


def test_deve_devolver_parte_do_credito_cliente(
    conta_credito: ContaCreditoCliente,
) -> None:
    saldo_inicial = conta_credito.saldo

    devolver_credito_cliente(
        conta_credito,
        Decimal("200.00"),
        FormaPagamento.PIX,
        "Devolução Parcial"
    )

    assert conta_credito.saldo == saldo_inicial - Decimal("200.00")

    movimentacao = conta_credito.movimentacoes[-1]

    assert movimentacao.tipo is TipoMovimentacaoCredito.DEVOLUCAO
    assert movimentacao.valor == Decimal("200.00")
    assert movimentacao.forma_origem is FormaPagamento.PIX
    assert movimentacao.observacoes == "Devolução Parcial"


def test_deve_permitir_devolver_todo_o_credito_cliente(
    conta_credito: ContaCreditoCliente,
) -> None:
    saldo_disponivel = conta_credito.saldo

    devolver_credito_cliente(
        conta_credito,
        saldo_disponivel,
        FormaPagamento.DINHEIRO,
    )

    assert conta_credito.saldo == Decimal("0.00")


def test_nao_deve_devolver_valor_maior_que_saldo(
    conta_credito: ContaCreditoCliente,
) -> None:
    valor_maior_que_saldo = conta_credito.saldo + Decimal("0.01")

    with pytest.raises(ValueError):
        devolver_credito_cliente(
            conta_credito,
            valor_maior_que_saldo,
            FormaPagamento.DINHEIRO,
        )


def test_nao_deve_devolver_credito_com_valor_zero(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(ValueError):
        devolver_credito_cliente(
            conta_credito,
            Decimal("0.00"),
            FormaPagamento.PIX,
        )


def test_nao_deve_devolver_credito_com_valor_negativo(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(ValueError):
        devolver_credito_cliente(
            conta_credito,
            Decimal("-10.00"),
            FormaPagamento.PIX,
        )


def test_nao_deve_devolver_credito_com_float(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(TypeError):
        devolver_credito_cliente(
            conta_credito,
            100.0,  # ty: ignore[invalid-argument-type]
            FormaPagamento.PIX,
        )        


def test_nao_deve_devolver_credito_com_forma_invalida(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(TypeError):
        devolver_credito_cliente(
            conta_credito,
            Decimal("100.00"),
            "Pix",  # ty: ignore[invalid-argument-type]
        )


def test_nao_deve_usar_credito_cliente_como_forma_de_devolucao(
    conta_credito: ContaCreditoCliente,
) -> None:
    with pytest.raises(ValueError):
        devolver_credito_cliente(
            conta_credito,
            Decimal("100.00"),
            FormaPagamento.CREDITO_CLIENTE,
        )

