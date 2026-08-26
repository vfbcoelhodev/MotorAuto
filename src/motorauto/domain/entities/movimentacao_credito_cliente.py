from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from motorauto.domain.entities.ordem_servico import OrdemServico
from motorauto.domain.enums.forma_pagamento import FormaPagamento
from motorauto.domain.enums.tipo_movimentacao_credito import (
    TipoMovimentacaoCredito,
)


@dataclass
class MovimentacaoCreditoCliente:
    _valor: Decimal = field(repr=False)
    _tipo: TipoMovimentacaoCredito = field(repr=False)

    _forma_origem: FormaPagamento | None = field(default=None, repr=False)
    _ordem_servico: OrdemServico | None = field(default=None, repr=False)
    _observacoes: str | None = field(default=None, repr=False)

    id: int | None = field(default=None, init=False)
    _data: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        self._preparar_atributos()

    def _preparar_atributos(self) -> None:
        self._valor = self._validar_decimal_positivo(self._valor, "valor")
        self._tipo = self._validar_tipo_movimentacao(self._tipo)
        self._forma_origem = self._validar_forma_origem(self._forma_origem, self._tipo)
        self._ordem_servico = self._validar_ordem_servico(self._ordem_servico, self._tipo)
        self._observacoes = self._normalizar_texto_opcional(self._observacoes, "observacoes")


    @property
    def valor(self) -> Decimal:
        return self._valor

    @property
    def tipo(self) -> TipoMovimentacaoCredito:
        return self._tipo

    @property
    def forma_origem(self) -> FormaPagamento | None:
        return self._forma_origem

    @property
    def ordem_servico(self) -> OrdemServico | None:
        return self._ordem_servico

    @property
    def observacoes(self) -> str | None:
        return self._observacoes

    @property
    def data(self) -> datetime:
        return self._data
        
    @staticmethod
    def _validar_decimal_positivo(valor: Decimal, nome_campo: str) -> Decimal:
            if not isinstance(valor, Decimal):
                raise TypeError(f"O campo {nome_campo} deve ser do tipo Decimal.")
    
            if valor <= Decimal("0.00"):
                raise ValueError(f"O campo {nome_campo} deve ser um valor positivo.")
    
            return valor
    

    @staticmethod
    def _normalizar_texto_opcional(valor: str | None, nome_campo: str) -> str | None:
        if valor is None:
            return None

        if not isinstance(valor, str):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo str ou None.")

        valor = valor.strip()

        return valor or None
    

    @staticmethod
    def _validar_ordem_servico(
        ordem_servico: OrdemServico | None,
        tipo_movimentacao: TipoMovimentacaoCredito,
    ) -> OrdemServico | None:
        if tipo_movimentacao in {
            TipoMovimentacaoCredito.USO_EM_OS,
            TipoMovimentacaoCredito.AJUSTE_OS,
        }:
            if ordem_servico is None:
                raise ValueError(
                    "O campo ordem_servico é obrigatório "
                    "para este tipo de movimentação."
                )

            if not isinstance(ordem_servico, OrdemServico):
                raise TypeError(
                    "O campo ordem_servico deve ser do tipo OrdemServico."
                )

            return ordem_servico

        if ordem_servico is not None:
            raise ValueError(
                "O campo ordem_servico deve ser None "
                "para este tipo de movimentação."
            )

        return None
    @staticmethod
    def _validar_forma_origem(
        forma_origem: FormaPagamento | None,
        tipo_movimentacao: TipoMovimentacaoCredito,
    ) -> FormaPagamento | None:
        if tipo_movimentacao in {
            TipoMovimentacaoCredito.USO_EM_OS,
            TipoMovimentacaoCredito.AJUSTE_OS,
        }:
            if forma_origem is not None:
                raise ValueError(
                    "O campo forma_origem deve ser None "
                    "para este tipo de movimentação."
                )

            return None

        if forma_origem is None:
            raise ValueError(
                "O campo forma_origem é obrigatório "
                "para este tipo de movimentação."
            )

        if not isinstance(forma_origem, FormaPagamento):
            raise TypeError(
                "O campo forma_origem deve ser do tipo FormaPagamento."
            )

        if forma_origem is FormaPagamento.CREDITO_CLIENTE:
            raise ValueError(
                "Crédito do cliente não pode ser usado como forma de origem."
            )

        return forma_origem


    @staticmethod
    def _validar_tipo_movimentacao(tipo_movimentacao: TipoMovimentacaoCredito) -> TipoMovimentacaoCredito:
        if not isinstance(tipo_movimentacao, TipoMovimentacaoCredito):
            raise TypeError("O campo tipo_movimentacao deve ser do tipo TipoMovimentacaoCredito.")

        return tipo_movimentacao