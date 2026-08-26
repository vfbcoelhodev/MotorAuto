from dataclasses import dataclass, field
from decimal import Decimal

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.movimentacao_credito_cliente import (
    MovimentacaoCreditoCliente,
)
from motorauto.domain.enums.tipo_movimentacao_credito import (
    TipoMovimentacaoCredito,
)


@dataclass
class ContaCreditoCliente:
    _cliente: Cliente = field(repr=False)

    id: int | None = field(default=None, init=False)
    _movimentacoes: list[MovimentacaoCreditoCliente] = field(
        default_factory=list,
        init=False,
        repr=False,
    )


    def __post_init__(self) -> None:
        self._cliente = self._validar_cliente(self._cliente)

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def movimentacoes(self) -> tuple[MovimentacaoCreditoCliente, ...]:
        return tuple(self._movimentacoes)

    @property
    def saldo(self) -> Decimal:
        total_creditos = sum(
        (
            movimentacao.valor
            for movimentacao in self._movimentacoes
            if movimentacao.tipo
            in {
                TipoMovimentacaoCredito.CREDITO,
                TipoMovimentacaoCredito.AJUSTE_OS,
            }
        ),
        Decimal("0.00"),
    )
    
        total_debitos = sum(
            (
                movimentacao.valor
                for movimentacao in self._movimentacoes
                if movimentacao.tipo
                in {
                    TipoMovimentacaoCredito.USO_EM_OS,
                    TipoMovimentacaoCredito.DEVOLUCAO,
                }
            ),
            Decimal("0.00"),
        )

        return total_creditos - total_debitos


    def registrar_credito(
        self,
        movimentacao: MovimentacaoCreditoCliente,
    ) -> None:
        movimentacao = self._validar_movimentacao(movimentacao)

        if movimentacao.tipo is not TipoMovimentacaoCredito.CREDITO:
            raise ValueError(
                "Somente uma movimentação do tipo CREDITO "
                "pode ser registrada como crédito."
            )

        self._movimentacoes.append(movimentacao)
    
    def utilizar_credito_em_os(
        self,
        movimentacao: MovimentacaoCreditoCliente,
    ) -> None:
        movimentacao = self._validar_movimentacao(movimentacao)

        if movimentacao.tipo is not TipoMovimentacaoCredito.USO_EM_OS:
            raise ValueError(
                "Somente uma movimentação do tipo USO_EM_OS "
                "pode ser registrada como uso em OS."
            )

        if (
            movimentacao.ordem_servico is None
            or movimentacao.ordem_servico.cliente is not self._cliente
        ):
            raise ValueError(
                "A Ordem de Serviço informada não pertence "
                "ao cliente desta conta de crédito."
            )

        if movimentacao.valor > self.saldo:
            raise ValueError(
                "O valor utilizado não pode ser maior que "
                "o saldo de crédito disponível."
            )

        self._movimentacoes.append(movimentacao)

    def registrar_devolucao(
        self,
        movimentacao: MovimentacaoCreditoCliente,
    ) -> None:
        movimentacao = self._validar_movimentacao(movimentacao)

        if movimentacao.tipo is not TipoMovimentacaoCredito.DEVOLUCAO:
            raise ValueError(
                "Somente uma movimentação do tipo DEVOLUCAO "
                "pode ser registrada como devolução."
            )

        if movimentacao.valor > self.saldo:
            raise ValueError(
                "O valor da devolução não pode ser maior que "
                "o saldo de crédito disponível."
            )

        self._movimentacoes.append(movimentacao)

    def registrar_ajuste_os(
            self,
            movimentacao: MovimentacaoCreditoCliente,
    ) -> None:
            movimentacao = self._validar_movimentacao(movimentacao)
    
            if movimentacao.tipo is not TipoMovimentacaoCredito.AJUSTE_OS:
                raise ValueError(
                    "Somente uma movimentação do tipo AJUSTE_OS "
                    "pode ser registrada como ajuste de OS."
                )
    
            if (
                movimentacao.ordem_servico is None
                or movimentacao.ordem_servico.cliente is not self._cliente
            ):
                raise ValueError(
                    "A Ordem de Serviço informada não pertence "
                    "ao cliente desta conta de crédito."
                )
    
            self._movimentacoes.append(movimentacao)

    @staticmethod
    def _validar_cliente(cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "O campo cliente deve ser do tipo Cliente."
            )

        return cliente

    @staticmethod
    def _validar_movimentacao(
        movimentacao: MovimentacaoCreditoCliente,
    ) -> MovimentacaoCreditoCliente:
        if not isinstance(movimentacao, MovimentacaoCreditoCliente):
            raise TypeError(
                "A movimentação deve ser do tipo MovimentacaoCreditoCliente."
            )

        return movimentacao