from motorauto.domain.enums.status_ordem_servico import StatusOrdemServico


def test_deve_possuir_status_corretos() -> None:
    assert StatusOrdemServico.ABERTA.value == "Aberta"
    assert StatusOrdemServico.EM_DIAGNOSTICO.value == "Em diagnóstico"
    assert StatusOrdemServico.AGUARDANDO_APROVACAO.value == "Aguardando aprovação"
    assert StatusOrdemServico.EM_EXECUCAO.value == "Em execução"
    assert StatusOrdemServico.CONCLUIDA.value == "Concluída"
    assert StatusOrdemServico.ENTREGUE.value == "Entregue"
    assert StatusOrdemServico.CANCELADA.value == "Cancelada"
    