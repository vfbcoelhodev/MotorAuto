from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from motorauto.domain.enums.forma_pagamento import FormaPagamento


@dataclass
class Pagamento:
    _valor: Decimal = field(repr=False)
    _forma_pagamento: FormaPagamento = field(repr=False)

    _observacoes: str | None = field(default=None, repr=False)

    id: int | None = field(default=None, init=False)
    _data_pagamento: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        self._preparar_atributos()

    def _preparar_atributos(self) -> None:
        self._valor = self._validar_decimal_positivo(self._valor, "valor")
        self._forma_pagamento = self._validar_forma_pagamento(self._forma_pagamento)
        self._observacoes = self._normalizar_texto_opcional(self._observacoes)
    

    @property
    def valor(self) -> Decimal:
        return self._valor
    
    @property
    def forma_pagamento(self) -> FormaPagamento:
        return self._forma_pagamento
    
    @property
    def observacoes(self) -> str | None:    
        return self._observacoes
    
    @property
    def data_pagamento(self) -> datetime:
        return self._data_pagamento

    
    @staticmethod
    def _validar_decimal_positivo(valor: Decimal, nome_campo: str) -> Decimal:
        if not isinstance(valor, Decimal):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo Decimal.")

        if valor <= Decimal("0.00"):
            raise ValueError(f"O campo {nome_campo} deve ser um valor positivo.")

        return valor
    

    @staticmethod
    def _validar_forma_pagamento(forma_pagamento: FormaPagamento) -> FormaPagamento:
        if not isinstance(forma_pagamento, FormaPagamento):
            raise TypeError("O campo forma_pagamento deve ser do tipo FormaPagamento.")

        return forma_pagamento
    

    @staticmethod
    def _normalizar_texto_opcional(valor: str | None) -> str | None:
        if valor is None:
            return None

        if not isinstance(valor, str):
            raise TypeError("O campo observacoes deve ser do tipo str ou None.")

        valor = valor.strip()

        return valor or None
