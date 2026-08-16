from motorauto.domain.enums.situacao_pagamento import SituacaoPagamento


def test_deve_possuir_situacoes_de_pagamento_corretas() -> None:
    assert SituacaoPagamento.PENDENTE.value == "Pendente"
    assert SituacaoPagamento.PARCIAL.value == "Parcial"
    assert SituacaoPagamento.PAGO.value == "Pago"
    