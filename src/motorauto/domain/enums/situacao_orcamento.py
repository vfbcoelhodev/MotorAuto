from enum import Enum


class SituacaoOrcamento(Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    PARCIALMENTE_APROVADO = "Parcialmente aprovado"
    RECUSADO = "Recusado"
    