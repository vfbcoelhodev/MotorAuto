from enum import Enum


class StatusOrdemServico(Enum):
    ABERTA = "Aberta"
    EM_DIAGNOSTICO = "Em diagnóstico"
    AGUARDANDO_APROVACAO = "Aguardando aprovação"
    EM_EXECUCAO = "Em execução"
    CONCLUIDA = "Concluída"
    ENTREGUE = "Entregue"
    CANCELADA = "Cancelada"
