from decimal import Decimal

from motorauto.domain.entities.conta_credito_cliente import ContaCreditoCliente
from motorauto.domain.entities.movimentacao_credito_cliente import (
    MovimentacaoCreditoCliente,
)
from motorauto.domain.entities.ordem_servico import OrdemServico
from motorauto.domain.entities.pagamento import Pagamento
from motorauto.domain.enums.forma_pagamento import FormaPagamento
from motorauto.domain.enums.tipo_movimentacao_credito import (
    TipoMovimentacaoCredito,
)


def utilizar_credito_em_os(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
    valor: Decimal,
) -> None:
    if not isinstance(conta_credito, ContaCreditoCliente):
        raise TypeError(
            "A conta informada deve ser do tipo ContaCreditoCliente."
        )

    if not isinstance(ordem_servico, OrdemServico):
        raise TypeError(
            "A Ordem de Serviço informada deve ser do tipo OrdemServico."
        )
        
    if conta_credito.cliente is not ordem_servico.cliente:
        raise ValueError(
            "A conta de crédito deve pertencer ao cliente "
            "da Ordem de Serviço."
        )

    if not isinstance(valor, Decimal):
        raise TypeError(
            "O valor deve ser do tipo Decimal."
        )

    if valor <= Decimal("0.00"):
        raise ValueError(
            "O valor utilizado deve ser maior que zero."
        )

    if valor > conta_credito.saldo:
        raise ValueError(
            "O valor utilizado não pode ultrapassar "
            "o saldo de crédito disponível."
        )

    if valor > ordem_servico.saldo_restante:
        raise ValueError(
            "O valor utilizado não pode ultrapassar "
            "o saldo restante da Ordem de Serviço."
        )

    movimentacao = MovimentacaoCreditoCliente(
        _valor=valor,
        _tipo=TipoMovimentacaoCredito.USO_EM_OS,
        _ordem_servico=ordem_servico,
    )

    pagamento = Pagamento(
        _valor=valor,
        _forma_pagamento=FormaPagamento.CREDITO_CLIENTE,
    )

    conta_credito.utilizar_credito_em_os(movimentacao)

    ordem_servico.registrar_pagamento_com_credito_cliente(
        pagamento
    )


def converter_excedente_os_em_credito(
    conta_credito: ContaCreditoCliente,
    ordem_servico: OrdemServico,
) -> None:
    if not isinstance(conta_credito, ContaCreditoCliente):
        raise TypeError(
            "A conta informada deve ser do tipo ContaCreditoCliente."
        )

    if not isinstance(ordem_servico, OrdemServico):
        raise TypeError(
            "A Ordem de Serviço informada deve ser do tipo OrdemServico."
        )
    if conta_credito.cliente is not ordem_servico.cliente:
        raise ValueError(
            "A conta de crédito deve pertencer ao cliente "
            "da Ordem de Serviço."
        )

    if ordem_servico.valor_excedente == Decimal("0.00"):
        raise ValueError(
            "A Ordem de Serviço não possui valor excedente."
        )

    total_ajustes_ja_registrados = sum(
        (
            movimentacao.valor
            for movimentacao in conta_credito.movimentacoes
            if (
                movimentacao.tipo is TipoMovimentacaoCredito.AJUSTE_OS
                and movimentacao.ordem_servico is ordem_servico
            )
        ),
        Decimal("0.00"),
    )

    valor_a_creditar = (
        ordem_servico.valor_excedente
        - total_ajustes_ja_registrados
    )

    if valor_a_creditar <= Decimal("0.00"):
        raise ValueError(
            "O valor excedente desta Ordem de Serviço "
            "já foi convertido em crédito."
        )

    movimentacao = MovimentacaoCreditoCliente(
        _valor=valor_a_creditar,
        _tipo=TipoMovimentacaoCredito.AJUSTE_OS,
        _ordem_servico=ordem_servico,
    )

    conta_credito.registrar_ajuste_os(movimentacao)


def registrar_credito_cliente(
    conta_credito: ContaCreditoCliente,
    valor: Decimal,
    forma_origem: FormaPagamento,
    observacoes: str | None = None,
) -> None:
    if not isinstance(conta_credito, ContaCreditoCliente):
        raise TypeError(
            "A conta informada deve ser do tipo ContaCreditoCliente."
        )

    if not isinstance(valor, Decimal):
        raise TypeError(
            "O valor deve ser do tipo Decimal."
        )

    if valor <= Decimal("0.00"):
        raise ValueError(
            "O valor do crédito deve ser maior que zero."
        )

    if not isinstance(forma_origem, FormaPagamento):
        raise TypeError(
            "A forma de origem deve ser do tipo FormaPagamento."
        )

    if forma_origem is FormaPagamento.CREDITO_CLIENTE:
        raise ValueError(
            "Crédito do cliente não pode ser usado como "
            "forma de origem de um novo crédito."
        )

    movimentacao = MovimentacaoCreditoCliente(
        _valor=valor,
        _tipo=TipoMovimentacaoCredito.CREDITO,
        _forma_origem=forma_origem,
        _observacoes=observacoes,
    )

    conta_credito.registrar_credito(movimentacao)   


def devolver_credito_cliente(
    conta_credito: ContaCreditoCliente,
    valor: Decimal,
    forma_devolucao: FormaPagamento,
    observacoes: str | None = None,
) -> None:
    if not isinstance(conta_credito, ContaCreditoCliente):
        raise TypeError(
            "A conta informada deve ser do tipo ContaCreditoCliente."
        )

    if not isinstance(valor, Decimal):
        raise TypeError(
            "O valor deve ser do tipo Decimal."
        )

    if valor <= Decimal("0.00"):
        raise ValueError(
            "O valor da devolução deve ser maior que zero."
        )

    if valor > conta_credito.saldo:
        raise ValueError(
            "O valor da devolução não pode ultrapassar "
            "o saldo de crédito disponível."
        )

    if not isinstance(forma_devolucao, FormaPagamento):
        raise TypeError(
            "A forma de devolução deve ser do tipo FormaPagamento."
        )

    if forma_devolucao is FormaPagamento.CREDITO_CLIENTE:
        raise ValueError(
            "Crédito do cliente não pode ser usado "
            "como forma de devolução."
        )

    movimentacao = MovimentacaoCreditoCliente(
        _valor=valor,
        _tipo=TipoMovimentacaoCredito.DEVOLUCAO,
        _forma_origem=forma_devolucao,
        _observacoes=observacoes,
    )

    conta_credito.registrar_devolucao(movimentacao)
