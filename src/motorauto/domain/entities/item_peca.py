from dataclasses import dataclass, field
from decimal import Decimal

from motorauto.domain.enums.situacao_aprovacao_item import (
    SituacaoAprovacaoItem,
)


@dataclass
class ItemPeca:
    _descricao: str = field(repr=False)
    _quantidade: Decimal = field(repr=False)
    _valor_unitario: Decimal = field(repr=False)

    id: int | None = field(default=None, init=False)
    _situacao_aprovacao: SituacaoAprovacaoItem = field(
        default=SituacaoAprovacaoItem.PENDENTE, init=False
    )
    
    
    
    def __post_init__(self) -> None:
        self._preparar_atributos()

    def _preparar_atributos(self) -> None:
        self._descricao = self._validar_texto_obrigatorio(self._descricao, "descricao")
        self._quantidade = self._validar_decimal_positivo(self._quantidade, "quantidade")
        self._valor_unitario = self._validar_decimal_nao_negativo(self._valor_unitario, "valor_unitario")


    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def quantidade(self) -> Decimal:
        return self._quantidade

    @property
    def valor_unitario(self) -> Decimal:
        return self._valor_unitario

    @property
    def situacao_aprovacao(self) -> SituacaoAprovacaoItem:
        return self._situacao_aprovacao

    @property
    def subtotal(self) -> Decimal:
        return self._quantidade * self._valor_unitario
    
    def corrigir_descricao(self, nova_descricao: str) -> None:
        self._descricao = self._validar_texto_obrigatorio(
            nova_descricao,
            "descricao",
        )

    def alterar_quantidade(self, nova_quantidade: Decimal) -> None:
        self._quantidade = self._validar_decimal_positivo(
            nova_quantidade,
            "quantidade",
        )

    def alterar_valor_unitario(self, novo_valor_unitario: Decimal) -> None:
        self._valor_unitario = self._validar_decimal_nao_negativo(
            novo_valor_unitario,
            "valor_unitario",
        )

    def aprovar(self) -> None:
        self._situacao_aprovacao = SituacaoAprovacaoItem.APROVADO

    def recusar(self) -> None:
        self._situacao_aprovacao = SituacaoAprovacaoItem.RECUSADO
    
    def marcar_como_pendente(self) -> None:
        self._situacao_aprovacao = SituacaoAprovacaoItem.PENDENTE


    @staticmethod
    def _validar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
            if not isinstance(valor, str):
                raise TypeError(f"O campo {nome_campo} deve ser do tipo str.")
    
            valor = valor.strip()
    
            if not valor:
                raise ValueError(f"O campo {nome_campo} é obrigatório.")
    
            return valor
    

    @staticmethod
    def _validar_decimal_positivo(valor: Decimal, nome_campo: str) -> Decimal:
        if not isinstance(valor, Decimal):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo Decimal.")

        if valor <= Decimal("0.00"):
            raise ValueError(f"O campo {nome_campo} deve ser um valor positivo.")

        return valor
    

    @staticmethod
    def _validar_decimal_nao_negativo(valor: Decimal, nome_campo: str) -> Decimal:
        if not isinstance(valor, Decimal):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo Decimal.")

        if valor < Decimal("0.00"):
            raise ValueError(f"O campo {nome_campo} não pode ser negativo.")

        return valor
