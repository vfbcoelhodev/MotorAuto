from datetime import UTC, datetime
from decimal import Decimal

import pytest

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.item_peca import ItemPeca
from motorauto.domain.entities.item_servico import ItemServico
from motorauto.domain.entities.ordem_servico import OrdemServico
from motorauto.domain.entities.pagamento import Pagamento
from motorauto.domain.entities.profissional import Profissional
from motorauto.domain.entities.veiculo import Veiculo
from motorauto.domain.enums.forma_pagamento import FormaPagamento
from motorauto.domain.enums.funcao_profissional import FuncaoProfissional
from motorauto.domain.enums.situacao_aprovacao_item import SituacaoAprovacaoItem
from motorauto.domain.enums.situacao_orcamento import SituacaoOrcamento
from motorauto.domain.enums.situacao_pagamento import SituacaoPagamento
from motorauto.domain.enums.status_ordem_servico import StatusOrdemServico


@pytest.fixture
def cliente() -> Cliente:
    return Cliente(
        _nome="João da Silva",
        _telefone="31999999999",
    )


@pytest.fixture
def veiculo(cliente: Cliente) -> Veiculo:
    return Veiculo(
        _cliente=cliente,
        _marca="Fiat",
        _modelo="Palio",
    )


@pytest.fixture
def profissional() -> Profissional:
    return Profissional(
        _nome="Carlos",
        _telefone="31988888888",
        _funcao=FuncaoProfissional.MECANICO,
    )


@pytest.fixture
def ordem_servico(
    cliente: Cliente,
    veiculo: Veiculo,
) -> OrdemServico:
    return OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Motor falhando.",
    )


@pytest.fixture
def item_servico() -> ItemServico:
    return ItemServico(
        _descricao="Troca de óleo",
        _valor=Decimal("80.00"),
    )


@pytest.fixture
def item_peca() -> ItemPeca:
    return ItemPeca(
        _descricao="Filtro de óleo",
        _quantidade=Decimal("1.0"),
        _valor_unitario=Decimal("30.00"),
    )


@pytest.fixture
def pagamento_pix() -> Pagamento:
    return Pagamento(
        _valor=Decimal("20.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )



def test_deve_criar_ordem_servico_com_cliente_valido(
    ordem_servico: OrdemServico,
    cliente: Cliente,
) -> None:
    assert ordem_servico.cliente is cliente


def test_deve_criar_ordem_servico_com_veiculo_valido(
    ordem_servico: OrdemServico,
    veiculo: Veiculo,
) -> None:
    assert ordem_servico.veiculo is veiculo


def test_deve_criar_ordem_servico_com_defeito_relatado_valido(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.defeito_relatado == "Motor falhando."


def test_ordem_servico_deve_iniciar_aberta(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.status is StatusOrdemServico.ABERTA


def test_ordem_servico_deve_iniciar_sem_profissional(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.profissional_responsavel is None


def test_ordem_servico_deve_iniciar_sem_data_saida(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.data_saida is None


def test_ordem_servico_deve_iniciar_sem_itens(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.itens_servico == ()
    assert ordem_servico.itens_peca == ()


def test_ordem_servico_deve_iniciar_sem_pagamentos(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.pagamentos == ()
    assert ordem_servico.total_recebido == Decimal("0.00")


def test_ordem_servico_deve_iniciar_sem_desconto(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.desconto == Decimal("0.00")


def test_ordem_servico_sem_itens_deve_ter_orcamento_pendente(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.situacao_orcamento is SituacaoOrcamento.PENDENTE


def test_ordem_servico_sem_valor_deve_ser_considerada_paga(
    ordem_servico: OrdemServico,
) -> None:
    assert ordem_servico.total_final == Decimal("0.00")
    assert ordem_servico.situacao_pagamento is SituacaoPagamento.PAGO


def test_data_entrada_deve_ser_gerada_automaticamente(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    antes = datetime.now(UTC)

    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Motor falhando.",
    )

    depois = datetime.now(UTC)

    assert antes <= ordem_servico.data_entrada <= depois


def test_nao_deve_criar_ordem_servico_com_cliente_invalido(
    veiculo: Veiculo,
) -> None:
    with pytest.raises(TypeError):
        OrdemServico(
            _cliente="João",  # ty: ignore[invalid-argument-type]
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
        )


def test_nao_deve_criar_ordem_servico_com_veiculo_invalido(
    cliente: Cliente,
) -> None:
    with pytest.raises(TypeError):
        OrdemServico(
            _cliente=cliente,
            _veiculo="Palio",  # ty: ignore[invalid-argument-type]
            _defeito_relatado="Motor falhando.",
        )


def test_nao_deve_criar_ordem_servico_com_veiculo_de_outro_cliente(
    cliente: Cliente,
) -> None:
    outro_cliente = Cliente(
        _nome="Maria",
        _telefone="31977777777",
    )

    veiculo = Veiculo(
        _cliente=outro_cliente,
        _marca="Volkswagen",
        _modelo="Gol",
    )

    with pytest.raises(ValueError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
        )


def test_nao_deve_criar_ordem_servico_com_defeito_relatado_vazio(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(ValueError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="   ",
        )


def test_nao_deve_criar_ordem_servico_com_defeito_relatado_de_tipo_invalido(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(TypeError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado=123,  # ty: ignore[invalid-argument-type]
        )


def test_deve_normalizar_defeito_relatado(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="  Motor falhando.  ",
    )

    assert ordem_servico.defeito_relatado == "Motor falhando."


def test_deve_aceitar_quilometragem_zero(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Motor falhando.",
        _quilometragem=0,
    )

    assert ordem_servico.quilometragem == 0


def test_nao_deve_criar_ordem_servico_com_quilometragem_negativa(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(ValueError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
            _quilometragem=-1,
        )


def test_nao_deve_criar_ordem_servico_com_quilometragem_float(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(TypeError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
            _quilometragem=1000.5,  # ty: ignore[invalid-argument-type]
        )


def test_nao_deve_criar_ordem_servico_com_quilometragem_bool(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(TypeError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
            _quilometragem=True,  
        )


def test_deve_aceitar_data_prevista_saida_com_timezone(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    data_prevista = datetime(2026, 8, 30, 15, 0, tzinfo=UTC)

    ordem_servico = OrdemServico(
        _cliente=cliente,
        _veiculo=veiculo,
        _defeito_relatado="Motor falhando.",
        _data_prevista_saida=data_prevista,
    )

    assert ordem_servico.data_prevista_saida == data_prevista


def test_nao_deve_aceitar_data_prevista_saida_sem_timezone(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(ValueError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
            _data_prevista_saida=datetime(2026, 8, 30, 15, 0), # noqa: DTZ001
        )


def test_nao_deve_aceitar_data_prevista_saida_de_tipo_invalido(
    cliente: Cliente,
    veiculo: Veiculo,
) -> None:
    with pytest.raises(TypeError):
        OrdemServico(
            _cliente=cliente,
            _veiculo=veiculo,
            _defeito_relatado="Motor falhando.",
            _data_prevista_saida="30/08/2026",  # ty: ignore[invalid-argument-type]
        )


def test_deve_atribuir_profissional(
    ordem_servico: OrdemServico,
    profissional: Profissional,
) -> None:
    ordem_servico.atribuir_profissional(profissional)

    assert ordem_servico.profissional_responsavel is profissional


def test_deve_atualizar_quilometragem(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.atualizar_quilometragem(150000)

    assert ordem_servico.quilometragem == 150000


def test_deve_registrar_diagnostico(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.registrar_diagnostico("Falha na bobina.")

    assert ordem_servico.diagnostico == "Falha na bobina."


def test_deve_atualizar_observacoes(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.atualizar_observacoes(
        "Cliente solicitou retorno por telefone."
    )

    assert (
        ordem_servico.observacoes
        == "Cliente solicitou retorno por telefone."
    )


def test_nao_deve_atribuir_profissional_invalido(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(TypeError):
        ordem_servico.atribuir_profissional(
            "Carlos",  # ty: ignore[invalid-argument-type]
        )


def test_nao_deve_atualizar_quilometragem_para_valor_negativo(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.atualizar_quilometragem(-1)


def test_nao_deve_registrar_diagnostico_com_tipo_invalido(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(TypeError):
        ordem_servico.registrar_diagnostico(
            123,  # ty: ignore[invalid-argument-type]
        )


def test_os_cancelada_nao_deve_permitir_atribuir_profissional(
    ordem_servico: OrdemServico,
    profissional: Profissional,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.atribuir_profissional(profissional)


def test_os_cancelada_nao_deve_permitir_atualizar_quilometragem(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.atualizar_quilometragem(100000)


def test_os_cancelada_nao_deve_permitir_registrar_diagnostico(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.registrar_diagnostico("Diagnóstico.")


def test_os_cancelada_nao_deve_permitir_atualizar_observacoes(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.atualizar_observacoes("Observação.")


def test_deve_adicionar_item_servico(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    assert ordem_servico.itens_servico == (item_servico,)


def test_nao_deve_adicionar_objeto_que_nao_seja_item_servico(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(TypeError):
        ordem_servico.adicionar_item_servico(
            "Troca de óleo",  # ty: ignore[invalid-argument-type]
        )


def test_deve_remover_item_servico(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    ordem_servico.remover_item_servico(item_servico)

    assert ordem_servico.itens_servico == ()


def test_nao_deve_remover_item_servico_que_nao_pertence_a_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.remover_item_servico(item_servico)


def test_nao_deve_remover_item_servico_recusado(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.recusar_item_servico(item_servico)

    with pytest.raises(ValueError):
        ordem_servico.remover_item_servico(item_servico)


def test_deve_corrigir_descricao_item_servico_pela_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    ordem_servico.corrigir_descricao_item_servico(
        item_servico,
        "Troca de óleo do motor",
    )

    assert item_servico.descricao == "Troca de óleo do motor"


def test_deve_alterar_valor_item_servico_pela_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    ordem_servico.alterar_valor_item_servico(
        item_servico,
        Decimal("100.00"),
    )

    assert item_servico.valor == Decimal("100.00")


def test_deve_aprovar_item_servico_pela_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    ordem_servico.aprovar_item_servico(item_servico)

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.APROVADO
    )


def test_deve_recusar_item_servico_pela_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    ordem_servico.recusar_item_servico(item_servico)

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.RECUSADO
    )


def test_deve_marcar_item_servico_como_pendente_pela_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.marcar_item_servico_como_pendente(item_servico)

    assert (
        item_servico.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_nao_deve_alterar_item_servico_que_nao_pertence_a_os(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.alterar_valor_item_servico(
            item_servico,
            Decimal("100.00"),
        )


def test_deve_adicionar_item_peca(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    assert ordem_servico.itens_peca == (item_peca,)


def test_nao_deve_adicionar_objeto_que_nao_seja_item_peca(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(TypeError):
        ordem_servico.adicionar_item_peca(
            "Filtro de óleo",  # ty: ignore[invalid-argument-type]
        )


def test_deve_remover_item_peca(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.remover_item_peca(item_peca)

    assert ordem_servico.itens_peca == ()


def test_nao_deve_remover_item_peca_que_nao_pertence_a_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.remover_item_peca(item_peca)


def test_nao_deve_remover_item_peca_recusado(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.recusar_item_peca(item_peca)

    with pytest.raises(ValueError):
        ordem_servico.remover_item_peca(item_peca)


def test_deve_corrigir_descricao_item_peca_pela_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.corrigir_descricao_item_peca(
        item_peca,
        "Filtro de óleo do motor",
    )

    assert item_peca.descricao == "Filtro de óleo do motor"


def test_deve_alterar_quantidade_item_peca_pela_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.alterar_quantidade_item_peca(
        item_peca,
        Decimal("2.0"),
    )

    assert item_peca.quantidade == Decimal("2.0")
    assert item_peca.subtotal == Decimal("60.00")


def test_deve_alterar_valor_unitario_item_peca_pela_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.alterar_valor_unitario_item_peca(
        item_peca,
        Decimal("40.00"),
    )

    assert item_peca.valor_unitario == Decimal("40.00")
    assert item_peca.subtotal == Decimal("40.00")


def test_deve_aprovar_item_peca_pela_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_peca(item_peca)

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.APROVADO
    )


def test_deve_recusar_item_peca_pela_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.recusar_item_peca(item_peca)

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.RECUSADO
    )


def test_deve_marcar_item_peca_como_pendente_pela_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.marcar_item_peca_como_pendente(item_peca)

    assert (
        item_peca.situacao_aprovacao
        is SituacaoAprovacaoItem.PENDENTE
    )


def test_nao_deve_alterar_item_peca_que_nao_pertence_a_os(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.alterar_quantidade_item_peca(
            item_peca,
            Decimal("2.0"),
        )


def test_total_orcado_deve_somar_servicos_e_pecas(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    assert ordem_servico.total_orcado == Decimal("110.00")


def test_orcamento_deve_permanecer_pendente_enquanto_houver_item_pendente(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)

    assert ordem_servico.situacao_orcamento is SituacaoOrcamento.PENDENTE


def test_orcamento_deve_ser_aprovado_quando_todos_itens_foreem_aprovados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)
    ordem_servico.aprovar_item_peca(item_peca)

    assert ordem_servico.situacao_orcamento is SituacaoOrcamento.APROVADO


def test_orcamento_deve_ser_recusado_quando_todos_itens_foreem_recusados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.recusar_item_servico(item_servico)
    ordem_servico.recusar_item_peca(item_peca)

    assert ordem_servico.situacao_orcamento is SituacaoOrcamento.RECUSADO


def test_orcamento_deve_ser_parcialmente_aprovado_com_itens_aprovados_e_recusados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)
    ordem_servico.recusar_item_peca(item_peca)

    assert (
        ordem_servico.situacao_orcamento
        is SituacaoOrcamento.PARCIALMENTE_APROVADO
    )


def test_total_aprovado_deve_somar_somente_itens_aprovados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)
    ordem_servico.recusar_item_peca(item_peca)

    assert ordem_servico.total_aprovado == Decimal("80.00")


def test_total_recusado_deve_somar_somente_itens_recusados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)
    ordem_servico.recusar_item_peca(item_peca)

    assert ordem_servico.total_recusado == Decimal("30.00")


def test_item_pendente_nao_deve_entrar_em_total_aprovado_nem_recusado(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    assert ordem_servico.total_orcado == Decimal("80.00")
    assert ordem_servico.total_aprovado == Decimal("0.00")
    assert ordem_servico.total_recusado == Decimal("0.00")


def test_total_bruto_deve_considerar_servico_aprovado_e_executado(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)

    assert ordem_servico.total_bruto == Decimal("80.00")


def test_servico_aprovado_nao_executado_nao_deve_entrar_no_total_bruto(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    assert ordem_servico.total_aprovado == Decimal("80.00")
    assert ordem_servico.total_bruto == Decimal("0.00")


def test_peca_aprovada_deve_entrar_no_total_bruto(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    assert ordem_servico.total_bruto == Decimal("30.00")


def test_total_bruto_deve_somar_servicos_executados_e_pecas_aprovadas(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)

    assert ordem_servico.total_bruto == Decimal("110.00")


def test_total_final_deve_ser_total_bruto_menos_desconto(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.conceder_desconto(Decimal("5.00"))

    assert ordem_servico.total_bruto == Decimal("30.00")
    assert ordem_servico.desconto == Decimal("5.00")
    assert ordem_servico.total_final == Decimal("25.00")


def test_nao_deve_conceder_desconto_negativo(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.conceder_desconto(Decimal("-0.01"))


def test_nao_deve_conceder_desconto_maior_que_total_bruto(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    with pytest.raises(ValueError):
        ordem_servico.conceder_desconto(Decimal("30.01"))


def test_nao_deve_conceder_desconto_usando_float(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(TypeError):
        ordem_servico.conceder_desconto(
            10.0,  # ty: ignore[invalid-argument-type]
        )


def test_deve_permitir_desconto_igual_ao_total_bruto(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.conceder_desconto(Decimal("30.00"))

    assert ordem_servico.total_final == Decimal("0.00")
    assert ordem_servico.situacao_pagamento is SituacaoPagamento.PAGO


def test_deve_registrar_pagamento(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
    pagamento_pix: Pagamento,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.registrar_pagamento(pagamento_pix)

    assert ordem_servico.pagamentos == (pagamento_pix,)
    assert ordem_servico.total_recebido == Decimal("20.00")


def test_deve_calcular_saldo_restante(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
    pagamento_pix: Pagamento,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.registrar_pagamento(pagamento_pix)

    assert ordem_servico.total_final == Decimal("30.00")
    assert ordem_servico.saldo_restante == Decimal("10.00")


def test_pagamento_parcial_deve_resultar_em_situacao_parcial(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
    pagamento_pix: Pagamento,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    ordem_servico.registrar_pagamento(pagamento_pix)

    assert ordem_servico.situacao_pagamento is SituacaoPagamento.PARCIAL


def test_pagamento_integral_deve_resultar_em_situacao_paga(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    pagamento = Pagamento(
        _valor=Decimal("30.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    ordem_servico.registrar_pagamento(pagamento)

    assert ordem_servico.total_recebido == Decimal("30.00")
    assert ordem_servico.saldo_restante == Decimal("0.00")
    assert ordem_servico.situacao_pagamento is SituacaoPagamento.PAGO


def test_nao_deve_registrar_pagamento_maior_que_saldo(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    pagamento = Pagamento(
        _valor=Decimal("30.01"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    with pytest.raises(ValueError):
        ordem_servico.registrar_pagamento(pagamento)

    assert ordem_servico.total_recebido == Decimal("0.00")


def test_nao_deve_registrar_pagamento_quando_nao_ha_saldo(
    ordem_servico: OrdemServico,
) -> None:
    pagamento = Pagamento(
        _valor=Decimal("10.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    with pytest.raises(ValueError):
        ordem_servico.registrar_pagamento(pagamento)


def test_nao_deve_registrar_credito_cliente_diretamente(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    pagamento = Pagamento(
        _valor=Decimal("10.00"),
        _forma_pagamento=FormaPagamento.CREDITO_CLIENTE,
    )

    with pytest.raises(ValueError):
        ordem_servico.registrar_pagamento(pagamento)

    assert ordem_servico.total_recebido == Decimal("0.00")


def test_reducao_do_total_final_deve_gerar_valor_excedente(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.aprovar_item_peca(item_peca)

    pagamento = Pagamento(
        _valor=Decimal("30.00"),
        _forma_pagamento=FormaPagamento.PIX,
    )

    ordem_servico.registrar_pagamento(pagamento)

    ordem_servico.alterar_valor_unitario_item_peca(
        item_peca,
        Decimal("20.00"),
    )

    assert ordem_servico.total_final == Decimal("20.00")
    assert ordem_servico.total_recebido == Decimal("30.00")
    assert ordem_servico.saldo_restante == Decimal("0.00")
    assert ordem_servico.valor_excedente == Decimal("10.00")
    assert ordem_servico.situacao_pagamento is SituacaoPagamento.PAGO


def test_deve_iniciar_diagnostico(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.iniciar_diagnostico()

    assert ordem_servico.status is StatusOrdemServico.EM_DIAGNOSTICO


def test_deve_aguardar_aprovacao(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()

    assert (
        ordem_servico.status
        is StatusOrdemServico.AGUARDANDO_APROVACAO
    )


def test_deve_iniciar_execucao_com_orcamento_parcialmente_aprovado(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.adicionar_item_peca(item_peca)

    ordem_servico.aprovar_item_servico(item_servico)
    ordem_servico.recusar_item_peca(item_peca)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()

    assert ordem_servico.status is StatusOrdemServico.EM_EXECUCAO


def test_nao_deve_iniciar_execucao_com_itens_pendentes(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()

    with pytest.raises(ValueError):
        ordem_servico.iniciar_execucao()


def test_nao_deve_iniciar_execucao_com_orcamento_totalmente_recusado(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.recusar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()

    with pytest.raises(ValueError):
        ordem_servico.iniciar_execucao()


def test_deve_concluir_os_em_execucao_com_servicos_executados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)
    ordem_servico.concluir()

    assert ordem_servico.status is StatusOrdemServico.CONCLUIDA


def test_deve_concluir_os_quando_todos_itens_foreem_recusados(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.recusar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.concluir()

    assert ordem_servico.status is StatusOrdemServico.CONCLUIDA


def test_nao_deve_concluir_os_com_item_pendente(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()

    with pytest.raises(ValueError):
        ordem_servico.concluir()


def test_nao_deve_concluir_os_com_servico_aprovado_nao_executado(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()

    with pytest.raises(ValueError):
        ordem_servico.concluir()


def test_deve_registrar_entrega_de_os_concluida(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)
    ordem_servico.concluir()
    ordem_servico.registrar_entrega()

    assert ordem_servico.status is StatusOrdemServico.ENTREGUE
    assert ordem_servico.data_saida is not None
    assert ordem_servico.data_saida.tzinfo is not None


def test_deve_cancelar_ordem_servico(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()

    assert ordem_servico.status is StatusOrdemServico.CANCELADA


def test_nao_deve_cancelar_ordem_servico_entregue(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)
    ordem_servico.concluir()
    ordem_servico.registrar_entrega()

    with pytest.raises(ValueError):
        ordem_servico.cancelar()


def test_nao_deve_cancelar_ordem_servico_ja_cancelada(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.cancelar()


def test_deve_registrar_saida_de_ordem_servico_cancelada(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()
    ordem_servico.registrar_saida_cancelada()

    assert ordem_servico.status is StatusOrdemServico.CANCELADA
    assert ordem_servico.data_saida is not None
    assert ordem_servico.data_saida.tzinfo is not None


def test_nao_deve_registrar_saida_cancelada_em_os_nao_cancelada(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.registrar_saida_cancelada()


def test_nao_deve_registrar_saida_cancelada_duas_vezes(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.cancelar()
    ordem_servico.registrar_saida_cancelada()

    with pytest.raises(ValueError):
        ordem_servico.registrar_saida_cancelada()


def test_deve_retornar_de_aguardando_aprovacao_para_diagnostico(
    ordem_servico: OrdemServico,
) -> None:
    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()

    ordem_servico.retornar_para_diagnostico()

    assert ordem_servico.status is StatusOrdemServico.EM_DIAGNOSTICO


def test_deve_retornar_de_execucao_para_diagnostico(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()

    ordem_servico.retornar_para_diagnostico()

    assert ordem_servico.status is StatusOrdemServico.EM_DIAGNOSTICO


def test_deve_retornar_de_execucao_para_aprovacao(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()

    ordem_servico.retornar_para_aprovacao()

    assert (
        ordem_servico.status
        is StatusOrdemServico.AGUARDANDO_APROVACAO
    )


def test_deve_reabrir_execucao_de_os_concluida(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)
    ordem_servico.concluir()

    ordem_servico.reabrir_execucao()

    assert ordem_servico.status is StatusOrdemServico.EM_EXECUCAO


def test_nao_deve_retornar_para_aprovacao_se_nao_estiver_em_execucao(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.retornar_para_aprovacao()


def test_nao_deve_reabrir_execucao_se_os_nao_estiver_concluida(
    ordem_servico: OrdemServico,
) -> None:
    with pytest.raises(ValueError):
        ordem_servico.reabrir_execucao()


def test_os_cancelada_nao_deve_permitir_adicionar_item_servico(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.adicionar_item_servico(item_servico)


def test_os_cancelada_nao_deve_permitir_alterar_item_servico(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.alterar_valor_item_servico(
            item_servico,
            Decimal("100.00"),
        )


def test_os_cancelada_nao_deve_permitir_adicionar_item_peca(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.adicionar_item_peca(item_peca)


def test_os_cancelada_nao_deve_permitir_alterar_item_peca(
    ordem_servico: OrdemServico,
    item_peca: ItemPeca,
) -> None:
    ordem_servico.adicionar_item_peca(item_peca)
    ordem_servico.cancelar()

    with pytest.raises(ValueError):
        ordem_servico.alterar_quantidade_item_peca(
            item_peca,
            Decimal("2.0"),
        )


def test_os_entregue_nao_deve_permitir_alterar_itens(
    ordem_servico: OrdemServico,
    item_servico: ItemServico,
) -> None:
    ordem_servico.adicionar_item_servico(item_servico)
    ordem_servico.aprovar_item_servico(item_servico)

    ordem_servico.iniciar_diagnostico()
    ordem_servico.aguardar_aprovacao()
    ordem_servico.iniciar_execucao()
    ordem_servico.marcar_item_servico_como_executado(item_servico)
    ordem_servico.concluir()
    ordem_servico.registrar_entrega()

    with pytest.raises(ValueError):
        ordem_servico.alterar_valor_item_servico(
            item_servico,
            Decimal("100.00"),
        )


