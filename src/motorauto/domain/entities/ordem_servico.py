from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.item_peca import ItemPeca
from motorauto.domain.entities.item_servico import ItemServico
from motorauto.domain.entities.pagamento import Pagamento
from motorauto.domain.entities.profissional import Profissional
from motorauto.domain.entities.veiculo import Veiculo
from motorauto.domain.enums.forma_pagamento import FormaPagamento
from motorauto.domain.enums.situacao_aprovacao_item import SituacaoAprovacaoItem
from motorauto.domain.enums.situacao_orcamento import SituacaoOrcamento
from motorauto.domain.enums.situacao_pagamento import SituacaoPagamento
from motorauto.domain.enums.status_ordem_servico import StatusOrdemServico


@dataclass
class OrdemServico:
    _cliente: Cliente = field(repr=False)
    _veiculo: Veiculo = field(repr=False)
    _defeito_relatado: str = field(repr=False)

    _profissional_responsavel: Profissional | None = None
    _quilometragem: int | None = None
    _diagnostico: str | None = None
    _observacoes: str | None = None
    _data_prevista_saida: datetime | None = None

    id: int | None = field(default=None, init=False)
    _numero: int | None = field(default=None, init=False)
    _data_entrada: datetime = field(default_factory=lambda: datetime.now(UTC), init=False, repr=False)
    _status: StatusOrdemServico = field(default=StatusOrdemServico.ABERTA, init=False, repr=False)
    _data_saida: datetime | None = field(default=None, init=False, repr=False)

    _itens_servico: list[ItemServico] = field(default_factory=list, init=False, repr=False)
    _itens_peca: list[ItemPeca] = field(default_factory=list, init=False, repr=False)
    _pagamentos: list[Pagamento] = field(default_factory=list, init=False, repr=False)

    _desconto: Decimal = field(default=Decimal("0.00"), init=False, repr=False)
 
    def __post_init__(self) -> None:
        self._preparar_atributos()
    
    def _preparar_atributos(self) -> None:
        self._cliente = self._validar_cliente(self._cliente)
        self._veiculo = self._validar_veiculo(self._veiculo)
        self._validar_vinculo_cliente_veiculo(self._cliente, self._veiculo)
        self._defeito_relatado = self._validar_texto_obrigatorio(self._defeito_relatado, "defeito_relatado")
        self._profissional_responsavel = self._validar_profissional_responsavel(self._profissional_responsavel)
        self._quilometragem = self._validar_quilometragem(self._quilometragem)
        self._diagnostico = self._normalizar_texto_opcional(self._diagnostico, "diagnostico")
        self._observacoes = self._normalizar_texto_opcional(self._observacoes, "observacoes")
        self._data_prevista_saida = self._validar_data_prevista_saida(self._data_prevista_saida)

        
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def veiculo(self) -> Veiculo:
        return self._veiculo
    
    @property
    def defeito_relatado(self) -> str:
        return self._defeito_relatado
    
    @property
    def profissional_responsavel(self) -> Profissional | None:
        return self._profissional_responsavel
    
    @property
    def quilometragem(self) -> int | None:
        return self._quilometragem
    
    @property
    def diagnostico(self) -> str | None:
        return self._diagnostico
    
    @property
    def observacoes(self) -> str | None:
        return self._observacoes
    
    @property
    def data_prevista_saida(self) -> datetime | None:
        return self._data_prevista_saida
    
    @property
    def numero(self) -> int | None:
        return self._numero
    
    @property
    def data_entrada(self) -> datetime:
        return self._data_entrada
    
    @property
    def status(self) -> StatusOrdemServico:
        return self._status 
    
    @property
    def data_saida(self) -> datetime | None:
        return self._data_saida
    
    @property
    def itens_servico(self) -> tuple[ItemServico, ...]:
        return tuple(self._itens_servico)
    
    @property
    def itens_peca(self) -> tuple[ItemPeca, ...]:
        return tuple(self._itens_peca)
    
    @property
    def pagamentos(self) -> tuple[Pagamento, ...]:
        return tuple(self._pagamentos)
    
    @property
    def desconto(self) -> Decimal:
        return self._desconto
    
    @property
    def situacao_orcamento(self) -> SituacaoOrcamento:
        itens = [*self._itens_servico, *self._itens_peca]

        if not itens:
            return SituacaoOrcamento.PENDENTE

        if any(item.situacao_aprovacao is SituacaoAprovacaoItem.PENDENTE for item in itens):
            return SituacaoOrcamento.PENDENTE
        
        if all(item.situacao_aprovacao is SituacaoAprovacaoItem.APROVADO for item in itens):
            return SituacaoOrcamento.APROVADO
        
        if all(item.situacao_aprovacao is SituacaoAprovacaoItem.RECUSADO for item in itens):
            return SituacaoOrcamento.RECUSADO

        return SituacaoOrcamento.PARCIALMENTE_APROVADO
    
    @property
    def total_orcado(self) -> Decimal:
        total_servicos = sum((item.valor for item in self._itens_servico), Decimal("0.00"))

        total_pecas = sum((item.subtotal for item in self._itens_peca), Decimal("0.00"))

        return total_servicos + total_pecas

    @property
    def total_aprovado(self) -> Decimal:
        total_servicos = sum((item.valor for item in self._itens_servico if item.situacao_aprovacao is SituacaoAprovacaoItem.APROVADO), Decimal("0.00"))

        total_pecas = sum((item.subtotal for item in self._itens_peca if item.situacao_aprovacao is SituacaoAprovacaoItem.APROVADO), Decimal("0.00"))

        return total_servicos + total_pecas
    
    @property
    def total_recusado(self) -> Decimal:
        total_servicos = sum((item.valor for item in self._itens_servico if item.situacao_aprovacao is SituacaoAprovacaoItem.RECUSADO), Decimal("0.00"))

        total_pecas = sum((item.subtotal for item in self._itens_peca if item.situacao_aprovacao is SituacaoAprovacaoItem.RECUSADO), Decimal("0.00"))

        return total_servicos + total_pecas
    
    @property
    def total_bruto(self) -> Decimal:
        total_servicos = sum(
            (
                item.valor
                for item in self._itens_servico
                if (
                    item.situacao_aprovacao is SituacaoAprovacaoItem.APROVADO
                    and item.executado
                )
            ),
            Decimal("0.00"),
        )

        total_pecas = sum(
            (
                item.subtotal
                for item in self._itens_peca
                if item.situacao_aprovacao is SituacaoAprovacaoItem.APROVADO
            ),
            Decimal("0.00"),
        )

        return total_servicos + total_pecas

    @property
    def total_final(self) -> Decimal:
        return self.total_bruto - self.desconto

    @property
    def total_recebido(self) -> Decimal:
        return sum(
            (pagamento.valor for pagamento in self._pagamentos),
            Decimal("0.00"),
        )

    @property
    def saldo_restante(self) -> Decimal:
        saldo = self.total_final - self.total_recebido

        if saldo <= Decimal("0.00"):
            return Decimal("0.00")

        return saldo
    
    @property
    def valor_excedente(self) -> Decimal:
        excedente = self.total_recebido - self.total_final

        if excedente <= Decimal("0.00"):
            return Decimal("0.00")

        return excedente
        
    @property
    def situacao_pagamento(self) -> SituacaoPagamento:
        if self.total_final == Decimal("0.00"):
            return SituacaoPagamento.PAGO

        if self.total_recebido == Decimal("0.00"):
            return SituacaoPagamento.PENDENTE

        if self.total_recebido < self.total_final:
            return SituacaoPagamento.PARCIAL

        return SituacaoPagamento.PAGO
    
    def _garantir_os_editavel(self) -> None:
        if self._status in {
            StatusOrdemServico.CONCLUIDA,
            StatusOrdemServico.ENTREGUE,
            StatusOrdemServico.CANCELADA,
        }:
            raise ValueError("Não é possível alterar itens de uma Ordem de Serviço encerrada.")
    
    def adicionar_item_servico(self, item: ItemServico) -> None: 
        self._garantir_os_editavel()

        if not isinstance(item, ItemServico):
            raise TypeError("O item informado deve ser do tipo ItemServico.")

        self._itens_servico.append(item)
    
    def remover_item_servico(self, item: ItemServico) -> None:
        self._garantir_os_editavel()

        if not isinstance(item, ItemServico):
            raise TypeError("O item informado deve ser do tipo ItemServico.")

        indice = next(
            (
                indice
                for indice, item_existente in enumerate(self._itens_servico)
                if item_existente is item
            ),
            None,
        )

        if indice is None:
            raise ValueError("O item de serviço informado não pertence à Ordem de Serviço.")

        if item.situacao_aprovacao is SituacaoAprovacaoItem.RECUSADO:
            raise ValueError("Não é possível remover um item de serviço recusado.")

        self._itens_servico.pop(indice)

    def adicionar_item_peca(self, item: ItemPeca) -> None:
        self._garantir_os_editavel()

        if not isinstance(item, ItemPeca):
            raise TypeError("O item informado deve ser do tipo ItemPeca.")

        self._itens_peca.append(item)
    
    def remover_item_peca(self, item: ItemPeca) -> None:
        self._garantir_os_editavel()

        if not isinstance(item, ItemPeca):
            raise TypeError("O item informado deve ser do tipo ItemPeca.")

        indice = next(
            (
                indice
                for indice, item_existente in enumerate(self._itens_peca)
                if item_existente is item
            ),
            None,
        )

        if indice is None:
            raise ValueError("O item de peça informado não pertence à Ordem de Serviço.")

        if item.situacao_aprovacao is SituacaoAprovacaoItem.RECUSADO:
            raise ValueError("Não é possível remover um item de peça recusado.")

        self._itens_peca.pop(indice)
    
    def atribuir_profissional(self, profissional: Profissional) -> None:
        self._garantir_os_nao_encerrada()

        self._profissional_responsavel = self._validar_profissional(profissional)

    def atualizar_quilometragem(self, nova_quilometragem: int | None) -> None:
        self._garantir_os_nao_encerrada()

        self._quilometragem = self._validar_quilometragem(nova_quilometragem)
        
    def registrar_diagnostico(self, diagnostico: str | None) -> None:
        self._garantir_os_nao_encerrada()

        self._diagnostico = self._normalizar_texto_opcional(diagnostico, "diagnostico")

    def atualizar_observacoes(self, nova_observacao: str | None) -> None:
        self._garantir_os_nao_encerrada()

        self._observacoes = self._normalizar_texto_opcional(nova_observacao, "observacoes")

    def iniciar_diagnostico(self) -> None:
        if self._status is not StatusOrdemServico.ABERTA:
            raise ValueError("Somente uma Ordem de Serviço aberta pode iniciar o diagnóstico.")

        self._status = StatusOrdemServico.EM_DIAGNOSTICO
    
    def aguardar_aprovacao(self) -> None:
        if self._status is not StatusOrdemServico.EM_DIAGNOSTICO:
            raise ValueError("Somente uma Ordem de Serviço em diagnóstico pode aguardar aprovação.")

        self._status = StatusOrdemServico.AGUARDANDO_APROVACAO
    
    def iniciar_execucao(self) -> None:
        if self._status is not StatusOrdemServico.AGUARDANDO_APROVACAO:
            raise ValueError("Somente uma Ordem de Serviço aguardando aprovação pode iniciar a execução.")

        if self.situacao_orcamento is SituacaoOrcamento.PENDENTE:
            raise ValueError("Não é possível iniciar a execução enquanto houver itens pendentes de aprovação.")

        if self.situacao_orcamento is SituacaoOrcamento.RECUSADO:
            raise ValueError("Não é possível iniciar a execução quando todos os itens foram recusados.")

        self._status = StatusOrdemServico.EM_EXECUCAO
    
    def concluir(self) -> None:
        if self._status is StatusOrdemServico.AGUARDANDO_APROVACAO:
            if self.situacao_orcamento is not SituacaoOrcamento.RECUSADO:
                raise ValueError(
                    "Uma Ordem de Serviço aguardando aprovação "
                    "só pode ser concluída quando todos os itens "
                    "forem recusados."
                )

            self._status = StatusOrdemServico.CONCLUIDA
            return

        if self._status is not StatusOrdemServico.EM_EXECUCAO:
            raise ValueError(
                "Somente uma Ordem de Serviço em execução ou com "
                "orçamento totalmente recusado pode ser concluída."
            )

        if self.situacao_orcamento is SituacaoOrcamento.PENDENTE:
            raise ValueError(
                "Não é possível concluir uma Ordem de Serviço "
                "com itens pendentes de aprovação."
            )

        if any(
            item.situacao_aprovacao is SituacaoAprovacaoItem.APROVADO
            and not item.executado
            for item in self._itens_servico
        ):
            raise ValueError(
                "Não é possível concluir a Ordem de Serviço "
                "enquanto houver serviços aprovados não executados."
            )

        self._status = StatusOrdemServico.CONCLUIDA
    
    def registrar_entrega(self) -> None:
        if self._status is not StatusOrdemServico.CONCLUIDA:
            raise ValueError(
                "Somente uma Ordem de Serviço concluída pode ser entregue."
            )

        if self._data_saida is not None:
            raise ValueError(
                "A saída do veículo já foi registrada."
            )

        self._status = StatusOrdemServico.ENTREGUE
        self._data_saida = datetime.now(UTC)
    
    def cancelar(self) -> None:
        if self._status in {
            StatusOrdemServico.ENTREGUE,
            StatusOrdemServico.CANCELADA,
        }:
            raise ValueError(
                "Não é possível cancelar uma Ordem de Serviço "
                "que já está entregue ou cancelada."
            )

        self._status = StatusOrdemServico.CANCELADA
    
    def registrar_saida_cancelada(self) -> None:
        if self._status is not StatusOrdemServico.CANCELADA:
            raise ValueError(
                "Somente uma Ordem de Serviço cancelada pode registrar "
                "a saída do veículo."
            )

        if self._data_saida is not None:
            raise ValueError(
                "A saída do veículo já foi registrada."
            )
        
        self._data_saida = datetime.now(UTC)
    
    def conceder_desconto(self, desconto: Decimal) -> None:
        if not isinstance(desconto, Decimal):
            raise TypeError(
                "O campo desconto deve ser do tipo Decimal."
            )

        if desconto < Decimal("0.00"):
            raise ValueError(
                "O desconto não pode ser negativo."
            )

        if desconto > self.total_bruto:
            raise ValueError(
                "O desconto não pode ser maior que o total bruto da Ordem de Serviço."
            )

        if self._status in {
            StatusOrdemServico.ENTREGUE,
            StatusOrdemServico.CANCELADA,
        }:
            raise ValueError(
                "Não é possível conceder desconto em uma Ordem de Serviço encerrada."
            )

        self._desconto = desconto
    
    def registrar_pagamento(self, pagamento: Pagamento) -> None:
        if not isinstance(pagamento, Pagamento):
            raise TypeError(
                "O pagamento informado deve ser do tipo Pagamento."
            )

        if pagamento.forma_pagamento is FormaPagamento.CREDITO_CLIENTE:
            raise ValueError(
                "Pagamentos com crédito do cliente devem ser registrados "
                "pelo fluxo de utilização de crédito."
            )

        if self.saldo_restante == Decimal("0.00"):
            raise ValueError(
                "A Ordem de Serviço não possui saldo a receber."
            )

        novo_total_recebido = self.total_recebido + pagamento.valor

        if novo_total_recebido > self.total_final:
            raise ValueError(
                "A soma dos pagamentos não pode ultrapassar "
                "o TOTAL FINAL DA OS."
            )

        self._pagamentos.append(pagamento)
    
    def retornar_para_diagnostico(self) -> None:
        if self._status not in {
            StatusOrdemServico.AGUARDANDO_APROVACAO,
            StatusOrdemServico.EM_EXECUCAO,
        }:
            raise ValueError(
                "Somente uma Ordem de Serviço aguardando aprovação "
                "ou em execução pode retornar para diagnóstico."
            )

        self._status = StatusOrdemServico.EM_DIAGNOSTICO
    
    def retornar_para_aprovacao(self) -> None:
        if self._status is not StatusOrdemServico.EM_EXECUCAO:
            raise ValueError(
                "Somente uma Ordem de Serviço em execução "
                "pode retornar para aguardando aprovação."
            )

        self._status = StatusOrdemServico.AGUARDANDO_APROVACAO

    def reabrir_execucao(self) -> None:
        if self._status is not StatusOrdemServico.CONCLUIDA:
            raise ValueError(
                "Somente uma Ordem de Serviço concluída "
                "pode retornar para execução."
            )

        self._status = StatusOrdemServico.EM_EXECUCAO

    def _garantir_os_nao_encerrada(self) -> None:
        if self._status in {
            StatusOrdemServico.ENTREGUE,
            StatusOrdemServico.CANCELADA,
        }:
            raise ValueError(
                "Não é possível alterar uma Ordem de Serviço encerrada."
            )
    
    def _garantir_item_servico_pertence_os(
        self,
        item: ItemServico,
    ) -> ItemServico:
        if not isinstance(item, ItemServico):
            raise TypeError(
                "O item informado deve ser do tipo ItemServico."
            )

        if not any(
            item_existente is item
            for item_existente in self._itens_servico
        ):
            raise ValueError(
                "O item de serviço informado não pertence "
                "à Ordem de Serviço."
            )

        return item

    def _garantir_item_peca_pertence_os(
        self,
        item: ItemPeca,
    ) -> ItemPeca:
        if not isinstance(item, ItemPeca):
            raise TypeError(
                "O item informado deve ser do tipo ItemPeca."
            )

        if not any(
            item_existente is item
            for item_existente in self._itens_peca
        ):
            raise ValueError(
                "O item de peça informado não pertence "
                "à Ordem de Serviço."
            )

        return item
    
    def corrigir_descricao_item_servico(
        self,
        item: ItemServico,
        nova_descricao: str,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_servico_pertence_os(item)

        item.corrigir_descricao(nova_descricao)


    def alterar_valor_item_servico(
        self,
        item: ItemServico,
        novo_valor: Decimal,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_servico_pertence_os(item)

        item.alterar_valor(novo_valor)


    def aprovar_item_servico(
        self,
        item: ItemServico,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_servico_pertence_os(item)

        item.aprovar()


    def recusar_item_servico(
        self,
        item: ItemServico,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_servico_pertence_os(item)

        item.recusar()


    def marcar_item_servico_como_pendente(
        self,
        item: ItemServico,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_servico_pertence_os(item)

        item.marcar_como_pendente()
    
    def marcar_item_servico_como_executado(
        self,
        item: ItemServico,
    ) -> None:
        if self._status is not StatusOrdemServico.EM_EXECUCAO:
            raise ValueError(
                "Um serviço somente pode ser marcado como executado "
                "quando a Ordem de Serviço estiver em execução."
            )

        item = self._garantir_item_servico_pertence_os(item)

        item.marcar_como_executado()
    
    def corrigir_descricao_item_peca(
        self,
        item: ItemPeca,
        nova_descricao: str,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_peca_pertence_os(item)

        item.corrigir_descricao(nova_descricao)

    def alterar_quantidade_item_peca(
        self,
        item: ItemPeca,
        nova_quantidade: Decimal,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_peca_pertence_os(item)

        item.alterar_quantidade(nova_quantidade)


    def alterar_valor_unitario_item_peca(
        self,
        item: ItemPeca,
        novo_valor_unitario: Decimal,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_peca_pertence_os(item)

        item.alterar_valor_unitario(novo_valor_unitario)


    def aprovar_item_peca(self, item: ItemPeca) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_peca_pertence_os(item)

        item.aprovar()


    def recusar_item_peca(self, item: ItemPeca) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_peca_pertence_os(item)

        item.recusar()


    def marcar_item_peca_como_pendente(
        self,
        item: ItemPeca,
    ) -> None:
        self._garantir_os_editavel()
        item = self._garantir_item_peca_pertence_os(item)

        item.marcar_como_pendente()
        
    @staticmethod
    def _validar_profissional(profissional: Profissional) -> Profissional:
        if not isinstance(profissional, Profissional):
            raise TypeError("O profissional informado deve ser do tipo Profissional.")

        return profissional  


    @staticmethod
    def _validar_cliente(cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise TypeError("O campo cliente deve ser do tipo Cliente")

        return cliente
    

    @staticmethod
    def _validar_veiculo(veiculo: Veiculo) -> Veiculo:
        if not isinstance(veiculo, Veiculo):
            raise TypeError("O campo veiculo deve ser do tipo Veiculo")

        return veiculo
    

    @staticmethod
    def _validar_vinculo_cliente_veiculo(cliente: Cliente, veiculo: Veiculo) -> None:
        if veiculo.cliente is not cliente:
            raise ValueError("O veículo informado não pertence ao cliente da Ordem de Serviço.")
    

    @staticmethod
    def _validar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
        if not isinstance(valor, str):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo str.")

        valor = valor.strip()

        if not valor:
            raise ValueError(f"O campo {nome_campo} é obrigatório.")

        return valor
    

    @staticmethod
    def _validar_profissional_responsavel(profissional: Profissional | None) -> Profissional | None:
        if profissional is not None and not isinstance(profissional, Profissional):
            raise TypeError("O campo profissional_responsavel deve ser do tipo Profissional ou None.")

        return profissional
    

    @staticmethod
    def _validar_quilometragem(quilometragem: int | None) -> int | None:
        if quilometragem is None:
            return None

        if isinstance(quilometragem, bool) or not isinstance(quilometragem, int):
            raise TypeError("O campo quilometragem deve ser do tipo int ou None.")

        if quilometragem < 0:
            raise ValueError("O campo quilometragem não pode ser um valor negativo.")

        return quilometragem
    

    @staticmethod
    def _normalizar_texto_opcional(valor: str | None, nome_campo: str) -> str | None:
        if valor is None:
            return None

        if not isinstance(valor, str):
            raise TypeError(f"O campo {nome_campo} deve ser do tipo str ou None.")

        valor = valor.strip()

        return valor or None
    

    @staticmethod
    def _validar_data_prevista_saida(data_prevista_saida: datetime | None) -> datetime | None:
        if data_prevista_saida is None:
            return None

        if not isinstance(data_prevista_saida, datetime):
            raise TypeError("O campo data_prevista_saida deve ser do tipo datetime ou None.")

        if data_prevista_saida.tzinfo is None:
            raise ValueError("O campo data_prevista_saida deve possuir timezone.")

        return data_prevista_saida

