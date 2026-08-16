from dataclasses import dataclass, field
from decimal import Decimal

from motorauto.domain.enums.situacao_aprovacao_item import (
    SituacaoAprovacaoItem,
)


@dataclass
class ItemServico:
    _descricao: str = field(repr=False)
    _valor: Decimal = field(repr=False)

    id: int | None = field(default=None, init=False)
    _situacao_aprovacao: SituacaoAprovacaoItem = field(
        default=SituacaoAprovacaoItem.PENDENTE, init=False
    )
    _executado: bool = field(default=False, init=False)
    
    def __post_init__(self) -> None:
        self._preparar_atributos()

    def _preparar_atributos(self) -> None:
        self._descricao = self._validar_texto_obrigatorio(self._descricao, "descricao")
        self._valor = self._validar_valor_nao_negativo(self._valor, "valor")

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def valor(self) -> Decimal:
        return self._valor

    @property
    def situacao_aprovacao(self) -> SituacaoAprovacaoItem:
        return self._situacao_aprovacao

    @property
    def executado(self) -> bool:
        return self._executado
    
    def corrigir_descricao(self, nova_descricao: str) -> None:
        self._descricao = self._validar_texto_obrigatorio(
            nova_descricao,
            "descricao",
        )


    def alterar_valor(self, novo_valor: Decimal) -> None:
        self._valor = self._validar_valor_nao_negativo(
            novo_valor,
            "valor",
        )


    def aprovar(self) -> None:
        self._garantir_nao_executado()
        self._situacao_aprovacao = SituacaoAprovacaoItem.APROVADO


    def recusar(self) -> None:
        self._garantir_nao_executado()
        self._situacao_aprovacao = SituacaoAprovacaoItem.RECUSADO


    def marcar_como_pendente(self) -> None:
        self._garantir_nao_executado()
        self._situacao_aprovacao = SituacaoAprovacaoItem.PENDENTE


    def marcar_como_executado(self) -> None:
        if self._situacao_aprovacao is not SituacaoAprovacaoItem.APROVADO:
            raise ValueError("Somente um serviço aprovado pode ser marcado como executado.")

        self._executado = True

   
    def _garantir_nao_executado(self) -> None:
        if self._executado:
            raise ValueError("Não é possível alterar a situação de aprovação de um serviço já executado.")

            
    @staticmethod
    def _validar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
        if not isinstance(valor, str):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo str.")

        valor = valor.strip()

        if not valor:
            raise ValueError(f"O campo {nome_campo} é obrigatório.")

        return valor
    
    @staticmethod
    def _validar_valor_nao_negativo(valor: Decimal, nome_campo: str) -> Decimal:
        if not isinstance(valor, Decimal):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo Decimal.")

        if valor < Decimal("0.00"):
            raise ValueError(f"O campo {nome_campo} não pode ser negativo.")

        return valor
