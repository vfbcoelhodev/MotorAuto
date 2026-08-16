from enum import Enum


class SituacaoPagamento(Enum):
    PENDENTE = "Pendente"
    PARCIAL = "Parcial"
    PAGO = "Pago"
