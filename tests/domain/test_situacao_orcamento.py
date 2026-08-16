from motorauto.domain.enums.situacao_orcamento import SituacaoOrcamento


def test_deve_possuir_situacoes_de_orcamento_corretas() -> None:
    assert SituacaoOrcamento.PENDENTE.value == "Pendente"
    assert SituacaoOrcamento.APROVADO.value == "Aprovado"
    assert SituacaoOrcamento.PARCIALMENTE_APROVADO.value == "Parcialmente aprovado"
    assert SituacaoOrcamento.RECUSADO.value == "Recusado"
    