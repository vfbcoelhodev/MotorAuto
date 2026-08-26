from motorauto.domain.enums.tipo_movimentacao_credito import (
    TipoMovimentacaoCredito,
)


def test_deve_possuir_tipos_de_movimentacao_corretos() -> None:
    assert TipoMovimentacaoCredito.CREDITO.value == "Crédito"
    assert TipoMovimentacaoCredito.USO_EM_OS.value == "Uso em OS"
    assert TipoMovimentacaoCredito.DEVOLUCAO.value == "Devolução"


def test_deve_possuir_tipo_ajuste_os() -> None:
    assert (
        TipoMovimentacaoCredito.AJUSTE_OS.value
        == "Crédito por ajuste de OS"
    )