from motorauto.domain.enums.situacao_aprovacao_item import SituacaoAprovacaoItem


def test_deve_possuir_situacoes_de_aprovacao_corretas() -> None:
    assert SituacaoAprovacaoItem.PENDENTE.value == "Pendente"
    assert SituacaoAprovacaoItem.APROVADO.value == "Aprovado"
    assert SituacaoAprovacaoItem.RECUSADO.value == "Recusado"
    