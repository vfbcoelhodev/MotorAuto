from enum import Enum


class TipoMovimentacaoCredito(Enum):
    CREDITO = "Crédito"
    USO_EM_OS = "Uso em OS"
    DEVOLUCAO = "Devolução"
    AJUSTE_OS = "Crédito por ajuste de OS"