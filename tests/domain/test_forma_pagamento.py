from motorauto.domain.enums.forma_pagamento import FormaPagamento


def test_deve_possuir_formas_de_pagamento_corretas() -> None:
    assert FormaPagamento.DINHEIRO.value == "Dinheiro"
    assert FormaPagamento.PIX.value == "Pix"
    assert FormaPagamento.CARTAO_DEBITO.value == "Cartão de débito"
    assert FormaPagamento.CARTAO_CREDITO.value == "Cartão de crédito"
    