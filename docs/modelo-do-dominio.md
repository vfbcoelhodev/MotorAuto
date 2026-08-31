# 🚗 Modelo do Domínio --- MotorAuto

Este documento descreve as principais entidades, enums, relacionamentos,
regras de negócio e decisões técnicas já validadas e implementadas no
domínio do **MotorAuto**.

> **Importante:** este é um documento vivo. Deve ser atualizado sempre
> que uma regra de negócio for criada, alterada ou removida.

------------------------------------------------------------------------

## Convenções

-   **Obrigatório:** deve ser informado para que a entidade seja válida.
-   **Opcional:** pode ser omitido.
-   **Gerado automaticamente:** definido pelo sistema ou pela
    persistência.
-   **Calculado:** derivado de outros dados do domínio e não mantido
    como fonte independente de verdade.
-   **Raiz do agregado:** entidade responsável por coordenar alterações
    e preservar invariantes dos objetos que pertencem ao agregado.
-   ✅ **Implementada e testada**
-   🟡 **Modelagem validada / integração pendente**
-   ⏳ **Em definição**

------------------------------------------------------------------------

# Visão geral do domínio

  ----------------------------------------------------------------------------
  Estrutura                    Tipo                    Situação
  ---------------------------- ----------------------- -----------------------
  Cliente                      Entidade                ✅ Implementada e
                                                       testada

  Veículo                      Entidade                ✅ Implementada e
                                                       testada

  Profissional                 Entidade                ✅ Implementada e
                                                       testada

  OrdemServico                 Entidade / raiz do      ✅ Implementada e
                               agregado da OS          testada

  ItemServico                  Composição da OS        ✅ Implementada e
                                                       testada

  ItemPeca                     Composição da OS        ✅ Implementada e
                                                       testada

  Pagamento                    Entidade                ✅ Implementada e
                                                       testada

  MovimentacaoCreditoCliente   Entidade                ✅ Implementada e
                                                       testada

  ContaCreditoCliente          Entidade                ✅ Implementada e
                                                       testada

  FuncaoProfissional           Enum                    ✅ Implementado e
                                                       testado

  StatusOrdemServico           Enum                    ✅ Implementado e
                                                       testado

  SituacaoAprovacaoItem        Enum                    ✅ Implementado e
                                                       testado

  SituacaoOrcamento            Enum calculado          ✅ Implementado e
                                                       testado

  FormaPagamento               Enum                    ✅ Implementado e
                                                       testado

  SituacaoPagamento            Enum calculado          ✅ Implementado e
                                                       testado

  TipoMovimentacaoCredito      Enum                    ✅ Implementado e
                                                       testado
  ----------------------------------------------------------------------------

> Na última execução da suíte completa desta etapa, **262 testes
> automatizados passaram**.

------------------------------------------------------------------------

# Relacionamentos

``` text
Cliente (1) ───────── possui ───────────────► Veículo (N)
Cliente (1) ───────── solicita ─────────────► OrdemServico (N)
Cliente (1) ───────── possui ───────────────► ContaCreditoCliente (1)

Veículo (1) ───────── recebe ───────────────► OrdemServico (N)
Profissional (1) ──── pode ser responsável ► OrdemServico (N)

OrdemServico (1)
        ├──────── contém ───────────────► ItemServico (N)
        ├──────── utiliza ──────────────► ItemPeca (N)
        └──────── possui ───────────────► Pagamento (0..N)

ContaCreditoCliente (1)
        └──────── possui ───────────────► MovimentacaoCreditoCliente (N)

MovimentacaoCreditoCliente
        ├──────── usa ──────────────────► TipoMovimentacaoCredito
        ├──────── pode referenciar ─────► FormaPagamento
        └──────── pode referenciar ─────► OrdemServico

ItemServico ───────── usa ──────────────► SituacaoAprovacaoItem
ItemPeca ──────────── usa ──────────────► SituacaoAprovacaoItem
Pagamento ─────────── usa ──────────────► FormaPagamento
OrdemServico ──────── usa ──────────────► StatusOrdemServico
```

Na abertura da OS, o veículo deve pertencer ao cliente informado. A OS
preserva historicamente o cliente daquele atendimento mesmo que o
veículo seja transferido posteriormente.

------------------------------------------------------------------------

# Cliente

Representa uma pessoa física ou empresa atendida pela oficina.

## Atributos

### Obrigatórios

-   `nome`
-   `telefone`

### Opcionais

-   `possui_whatsapp`
-   `cpf`
-   `endereco`
-   `observacoes`

### Gerados automaticamente

-   `id`
-   `data_cadastro`
-   `ativo`

## Regras de negócio

**RN-CLI-001** --- Todo cliente deve possuir nome.\
**RN-CLI-002** --- Todo cliente deve possuir telefone.\
**RN-CLI-003** --- Nome e telefone devem ser normalizados, removendo
espaços excedentes nas extremidades.\
**RN-CLI-004** --- CPF, endereço e observações são opcionais.\
**RN-CLI-005** --- Textos opcionais contendo apenas espaços devem virar
`None`.\
**RN-CLI-006** --- Todo cliente inicia ativo.\
**RN-CLI-007** --- Clientes com histórico não devem ser excluídos
fisicamente.\
**RN-CLI-008** --- O cadastro pode ser ativado ou desativado,
preservando o histórico.\
**RN-CLI-009** --- A data de cadastro é preenchida automaticamente.\
**RN-CLI-010** --- O identificador será gerado pela persistência.\
**RN-CLI-011** --- Alterações sujeitas a regras devem ocorrer pela
interface pública.\
**RN-CLI-012** --- Alterações respeitam as mesmas validações da
criação.\
**RN-CLI-013** --- Uma tentativa inválida não pode modificar o estado
anterior.

## Interface pública

Consultas: `nome`, `telefone`, `cpf`, `endereco`, `observacoes`,
`possui_whatsapp`, `ativo`, `data_cadastro`.

Comportamentos: `atualizar_nome()`, `atualizar_telefone()`,
`atualizar_cpf()`, `atualizar_endereco()`, `atualizar_observacoes()`,
`ativar_whatsapp()`, `desativar_whatsapp()`, `ativar()`, `desativar()`.

------------------------------------------------------------------------

# Veículo

Representa um veículo pertencente a um cliente e que poderá possuir
histórico de Ordens de Serviço.

## Atributos

### Obrigatórios

-   `cliente`
-   `marca`
-   `modelo`

### Opcionais

-   `ano`
-   `placa`
-   `combustivel`
-   `observacoes`

### Gerados automaticamente

-   `id`

## Regras de negócio

**RN-VEI-001** --- Todo veículo deve estar associado a um cliente
válido.\
**RN-VEI-002** --- Marca é obrigatória.\
**RN-VEI-003** --- Modelo é obrigatório.\
**RN-VEI-004** --- Marca e modelo devem ser normalizados.\
**RN-VEI-005** --- Ano é opcional.\
**RN-VEI-006** --- Quando informado, ano deve ser inteiro entre `1886` e
`2100`.\
**RN-VEI-007** --- Placa é opcional.\
**RN-VEI-008** --- A placa informada é normalizada para maiúsculas, sem
espaços e sem hífen.\
**RN-VEI-009** --- A unicidade da placa será garantida pela
persistência.\
**RN-VEI-010** --- Combustível e observações são opcionais.\
**RN-VEI-011** --- Textos opcionais contendo apenas espaços devem virar
`None`.\
**RN-VEI-012** --- Quilometragem não pertence ao cadastro do veículo.\
**RN-VEI-013** --- Quilometragem é registrada em cada OS.\
**RN-VEI-014** --- O histórico de quilometragem será obtido pelas OS.\
**RN-VEI-015** --- Transferência de propriedade não apaga o histórico.\
**RN-VEI-016** --- Marca, modelo e ano são características estáveis.\
**RN-VEI-017** --- Alterações nesses campos são tratadas como correções
cadastrais.\
**RN-VEI-018** --- Correção inválida não modifica o estado anterior.\
**RN-VEI-019** --- Atributos sujeitos a regras permanecem protegidos.\
**RN-VEI-020** --- Alterações ocorrem pela interface pública.

## Interface pública

Consultas: `cliente`, `marca`, `modelo`, `ano`, `placa`, `combustivel`,
`observacoes`.

Comportamentos: `corrigir_marca()`, `corrigir_modelo()`,
`corrigir_ano()`, `atualizar_placa()`, `atualizar_combustivel()`,
`atualizar_observacoes()`, `transferir_propriedade()`.

------------------------------------------------------------------------

# Profissional

Representa um colaborador da oficina responsável por atendimento,
execução, auxílio operacional ou gerenciamento.

## Atributos

### Obrigatórios

-   `nome`
-   `telefone`
-   `funcao`

### Opcionais

-   `observacoes`

### Gerados automaticamente

-   `id`
-   `data_cadastro`
-   `ativo`

## Regras de negócio

**RN-PRO-001** --- Nome é obrigatório.\
**RN-PRO-002** --- Telefone é obrigatório.\
**RN-PRO-003** --- Função válida é obrigatória.\
**RN-PRO-004** --- Funções permitidas: Mecânico, Atendente, Gerente e
Auxiliar.\
**RN-PRO-005** --- Função é representada por `FuncaoProfissional`.\
**RN-PRO-006** --- Nome e telefone são normalizados.\
**RN-PRO-007** --- Observações são opcionais.\
**RN-PRO-008** --- Observações vazias são normalizadas para `None`.\
**RN-PRO-009** --- Todo profissional inicia ativo.\
**RN-PRO-010** --- Profissional com histórico não deve ser excluído
fisicamente.\
**RN-PRO-011** --- Pode ser desativado preservando associações
anteriores.\
**RN-PRO-012** --- Data de cadastro é automática.\
**RN-PRO-013** --- ID será gerado pela persistência.\
**RN-PRO-014** --- Atributos sujeitos a regras permanecem protegidos.\
**RN-PRO-015** --- Alterações ocorrem pela interface pública.\
**RN-PRO-016** --- Alteração inválida não modifica o estado anterior.

## Interface pública

Consultas: `nome`, `telefone`, `funcao`, `observacoes`, `ativo`,
`data_cadastro`.

Comportamentos: `atualizar_nome()`, `atualizar_telefone()`,
`alterar_funcao()`, `atualizar_observacoes()`, `ativar()`,
`desativar()`.

------------------------------------------------------------------------

# OrdemServico

Representa o atendimento desde a entrada do veículo até seu encerramento
operacional, incluindo diagnóstico, orçamento, aprovações, execução,
peças, valores e pagamentos.

A `OrdemServico` é a **raiz do agregado da OS**. Depois que
`ItemServico` e `ItemPeca` pertencem a uma OS, as alterações oficiais
nesses itens devem ser coordenadas pela própria `OrdemServico`, que
valida o estado operacional e a associação do item antes de delegar a
alteração ao objeto correspondente.

## Atributos

### Obrigatórios na abertura

-   `cliente`
-   `veiculo`
-   `defeito_relatado`

### Opcionais

-   `profissional_responsavel`
-   `quilometragem`
-   `diagnostico`
-   `observacoes`
-   `data_prevista_saida`

### Gerados automaticamente

-   `id`
-   `numero`
-   `data_entrada`
-   `status`
-   `data_saida` --- preenchida quando o veículo efetivamente deixa a
    oficina

### Composições

-   `itens_servico`
-   `itens_peca`
-   `pagamentos`

### Financeiro armazenado

-   `desconto`

### Calculados

-   `situacao_orcamento`
-   `total_orcado`
-   `total_aprovado`
-   `total_recusado`
-   `total_bruto`
-   `total_final`
-   `total_recebido`
-   `saldo_restante`
-   `valor_excedente`
-   `situacao_pagamento`

## Regras de negócio

### Abertura e histórico

**RN-OS-001** --- Toda OS deve possuir referência direta a um cliente.\
**RN-OS-002** --- Toda OS deve possuir referência direta a um veículo.\
**RN-OS-003** --- Na abertura, o veículo deve pertencer ao cliente
associado à OS.\
**RN-OS-004** --- A OS preserva historicamente o cliente do atendimento,
mesmo após transferência futura do veículo.\
**RN-OS-005** --- Defeito relatado é obrigatório e normalizado.\
**RN-OS-006** --- Quilometragem é opcional na abertura e pode ser
informada depois.\
**RN-OS-007** --- Quando informada, quilometragem deve ser inteira, não
negativa e `bool` não é aceito como quilometragem.\
**RN-OS-008** --- A OS pode ser aberta sem profissional responsável.\
**RN-OS-009** --- Um profissional válido pode ser atribuído
posteriormente.\
**RN-OS-010** --- Diagnóstico é opcional e não substitui o defeito
relatado.\
**RN-OS-011** --- Observações são opcionais e textos opcionais vazios
são normalizados para `None`.

### Identificação e datas

**RN-OS-012** --- O número da OS será único, sequencial, automático e
imutável.\
**RN-OS-013** --- A geração do número é responsabilidade da
persistência.\
**RN-OS-014** --- `data_entrada` é preenchida automaticamente na
criação.\
**RN-OS-015** --- Datas do domínio que representam instantes devem
possuir informação de timezone.\
**RN-OS-016** --- `data_saida` representa o momento em que o veículo
efetivamente deixa a oficina.\
**RN-OS-017** --- `data_saida` permanece `None` enquanto o veículo
estiver fisicamente na oficina.\
**RN-OS-018** --- Na entrega normal, `registrar_entrega()` altera o
status para `ENTREGUE` e preenche `data_saida`.\
**RN-OS-019** --- Uma OS `CANCELADA` pode permanecer com
`data_saida = None` enquanto o veículo ainda estiver na oficina.\
**RN-OS-020** --- Na retirada de veículo de OS `CANCELADA`,
`registrar_saida_cancelada()` preenche `data_saida` sem alterar o status
`CANCELADA`.\
**RN-OS-021** --- A saída de uma OS cancelada só pode ser registrada uma
vez.

### Status e transições

**RN-OS-022** --- Toda OS inicia `ABERTA`.

Fluxo principal:

``` text
ABERTA
  ↓
EM_DIAGNOSTICO
  ↓
AGUARDANDO_APROVACAO
  ↓
EM_EXECUCAO
  ↓
CONCLUIDA
  ↓
ENTREGUE
```

`CANCELADA` representa encerramento excepcional antes da entrega.

**RN-OS-023** --- Status é alterado somente por comportamentos
específicos da entidade.\
**RN-OS-024** --- Retornos controlados são permitidos enquanto a OS
estiver em estados compatíveis.\
**RN-OS-025** --- Retornos previstos: -
`AGUARDANDO_APROVACAO → EM_DIAGNOSTICO` -
`EM_EXECUCAO → AGUARDANDO_APROVACAO` - `EM_EXECUCAO → EM_DIAGNOSTICO` -
`CONCLUIDA → EM_EXECUCAO`

**RN-OS-026** --- `ENTREGUE` e `CANCELADA` são estados terminais do
fluxo operacional.\
**RN-OS-027** --- Uma OS pode ser cancelada antes da entrega por
desistência, cancelamento do atendimento ou outra interrupção que impeça
a conclusão normal.\
**RN-OS-028** --- O cancelamento ocorre por `cancelar()`.\
**RN-OS-029** --- Uma OS já `ENTREGUE` ou já `CANCELADA` não pode ser
cancelada novamente.\
**RN-OS-030** --- Estados terminais bloqueiam alterações operacionais
normais.\
**RN-OS-031** --- Atribuição de profissional, atualização de
quilometragem, diagnóstico e observações são bloqueados em `ENTREGUE` e
`CANCELADA`.\
**RN-OS-032** --- Alterações normais dos itens são bloqueadas em
`CONCLUIDA`, `ENTREGUE` e `CANCELADA`.\
**RN-OS-033** --- `CONCLUIDA` ainda admite retorno explícito para
`EM_EXECUCAO` por `reabrir_execucao()`.\
**RN-OS-034** --- Estado operacional e situação financeira são
independentes.

### OrdemServico como raiz do agregado

**RN-OS-035** --- A OS controla oficialmente a inclusão, remoção e
alteração de seus `ItemServico` e `ItemPeca`.\
**RN-OS-036** --- Antes de alterar um item, a OS deve validar que o item
pertence à sua coleção.\
**RN-OS-037** --- Um item que não pertence à OS não pode ser alterado
por comportamentos da OS.\
**RN-OS-038** --- A OS valida se seu estado permite a alteração antes de
delegar a regra interna ao item.\
**RN-OS-039** --- As coleções públicas de itens e pagamentos são
expostas de forma que não permitam manipulação direta da coleção
interna.\
**RN-OS-040** --- A aplicação/UI deve utilizar os comportamentos da OS
para alterar itens já vinculados ao agregado.

### Orçamento e aprovação

**RN-OS-041** --- O orçamento faz parte da própria OS no MVP.\
**RN-OS-042** --- Serviços e peças são itens estruturados.\
**RN-OS-043** --- A aprovação pode ser parcial.\
**RN-OS-044** --- Cada item possui `PENDENTE`, `APROVADO` ou
`RECUSADO`.\
**RN-OS-045** --- `situacao_orcamento` é calculada a partir dos itens.\
**RN-OS-046** --- Sem itens, a situação geral é `PENDENTE`.\
**RN-OS-047** --- Existindo pelo menos um item `PENDENTE`, a situação
geral é `PENDENTE`.\
**RN-OS-048** --- Com todos os itens decididos: - todos aprovados →
`APROVADO`; - todos recusados → `RECUSADO`; - aprovados + recusados →
`PARCIALMENTE_APROVADO`.

**RN-OS-049** --- Itens recusados são preservados no histórico.

### Inclusão, alteração e remoção de itens

**RN-OS-050** --- Itens podem ser adicionados, alterados ou removidos
enquanto a OS estiver editável e respeitando as regras específicas do
item.\
**RN-OS-051** --- Em `CONCLUIDA`, `ENTREGUE` ou `CANCELADA`, os itens
ficam bloqueados para alterações normais.\
**RN-OS-052** --- Itens `PENDENTE` ou `APROVADO` podem ser removidos
enquanto a OS permitir.\
**RN-OS-053** --- Itens `RECUSADO` não podem ser excluídos enquanto
permanecerem recusados.\
**RN-OS-054** --- A interface pode oferecer ações intuitivas como
lixeira, mas a validação pertence à OS.\
**RN-OS-055** --- A interface não manipula diretamente as coleções
internas.\
**RN-OS-056** --- Um `ItemServico` só pode ser marcado como executado
pela OS quando a própria OS estiver `EM_EXECUCAO`.\
**RN-OS-057** --- Além da regra da OS, o próprio `ItemServico` deve
satisfazer suas regras internas para ser executado.

### Início da execução e conclusão

**RN-OS-058** --- A execução só pode iniciar quando o orçamento estiver
`APROVADO` ou `PARCIALMENTE_APROVADO`.\
**RN-OS-059** --- A execução não pode iniciar enquanto houver item
pendente.\
**RN-OS-060** --- Um orçamento totalmente recusado não inicia execução.\
**RN-OS-061** --- A OS não pode ser concluída com itens `PENDENTE`.\
**RN-OS-062** --- A OS pode ser concluída sem execução quando todos os
itens forem recusados.\
**RN-OS-063** --- Serviços aprovados que compõem a cobrança devem estar
executados antes da conclusão.\
**RN-OS-064** --- `CONCLUIDA` significa que o trabalho terminou; o
veículo pode continuar fisicamente na oficina.

### Totais do orçamento

**RN-OS-065** --- `total_orcado` é a soma atual dos itens que permanecem
registrados na OS como componentes do orçamento.\
**RN-OS-066** --- Item removido deixa de compor `total_orcado`.\
**RN-OS-067** --- Item recusado permanece registrado e continua compondo
`total_orcado`.\
**RN-OS-068** --- O MVP não preserva versões completas anteriores do
orçamento.\
**RN-OS-069** --- `total_aprovado` é calculado pelos itens aprovados.\
**RN-OS-070** --- `total_recusado` é calculado pelos itens recusados.\
**RN-OS-071** --- Item pendente não compõe `total_aprovado` nem
`total_recusado`.\
**RN-OS-072** --- Totais calculados não podem ser alterados diretamente.

### Total bruto, desconto e TOTAL FINAL DA OS

**RN-OS-073** --- `total_bruto` é calculado pelos itens efetivamente
executados/cobrados.\
**RN-OS-074** --- `ItemServico` compõe `total_bruto` somente quando
`APROVADO` e `executado = True`.\
**RN-OS-075** --- `ItemPeca` compõe `total_bruto` quando `APROVADO` e
permanece na OS.\
**RN-OS-076** --- Itens pendentes ou recusados não compõem o total
bruto/final.\
**RN-OS-077** --- Serviço aprovado mas não executado não é cobrado.\
**RN-OS-078** --- Desconto é opcional e aplicado sobre o total bruto.\
**RN-OS-079** --- Desconto é `Decimal` e inicia em `Decimal("0.00")`.\
**RN-OS-080** --- Desconto é concedido manualmente; forma de pagamento
não concede desconto automaticamente.\
**RN-OS-081** --- A forma de pagamento pode ser considerada na
negociação, sem alterar automaticamente a regra de desconto.\
**RN-OS-082** --- Desconto não pode ser negativo nem superior ao total
bruto.\
**RN-OS-083** --- Desconto pode ser concedido/alterado apenas enquanto a
OS permitir alteração financeira correspondente.\
**RN-OS-084** --- O **TOTAL FINAL DA OS** é:

``` text
TOTAL FINAL DA OS = total_bruto - desconto
```

**RN-OS-085** --- Na interface, **TOTAL FINAL DA OS** é a informação
financeira principal.

### Pagamentos, total recebido e excedente

**RN-OS-086** --- A OS pode possuir zero ou vários pagamentos.\
**RN-OS-087** --- Pagamentos podem ocorrer em formas e datas
diferentes.\
**RN-OS-088** --- `total_recebido` é a soma dos pagamentos registrados
na OS.\
**RN-OS-089** --- `saldo_restante` nunca é negativo e é calculado por:

``` text
saldo_restante = max(TOTAL FINAL DA OS - total_recebido, 0)
```

**RN-OS-090** --- `valor_excedente` nunca é negativo e é calculado por:

``` text
valor_excedente = max(total_recebido - TOTAL FINAL DA OS, 0)
```

**RN-OS-091** --- No registro de um novo pagamento comum, o valor não
pode ultrapassar o saldo restante existente naquele momento.\
**RN-OS-092** --- Um pagamento comum não pode ser registrado quando não
houver saldo a receber.\
**RN-OS-093** --- A forma `CREDITO_CLIENTE` não pode ser registrada
diretamente pelo comportamento comum `registrar_pagamento()`.\
**RN-OS-094** --- O uso de crédito do cliente exige coordenação com
`ContaCreditoCliente`, evitando criar crédito ou consumo sem a
movimentação correspondente.\
**RN-OS-095** --- Após pagamentos já registrados, uma redução posterior
do total final pode fazer `total_recebido > total_final`.\
**RN-OS-096** --- A redução do total final não é rejeitada apenas por
gerar excedente.\
**RN-OS-097** --- Quando `total_recebido > total_final`, a diferença é
representada por `valor_excedente`.\
**RN-OS-098** --- O excedente não é automaticamente inserido na conta do
cliente pela entidade `OrdemServico`; essa coordenação pertence à camada
de aplicação.\
**RN-OS-099** --- A conversão de excedente em crédito do cliente deve
ser registrada por movimentação própria, preservando rastreabilidade.\
**RN-OS-100** --- `situacao_pagamento` é calculada, não armazenada como
fonte independente.\
**RN-OS-101** --- Se `TOTAL FINAL DA OS = R$ 0,00`, a situação é `PAGO`,
mesmo sem pagamentos.\
**RN-OS-102** --- Para total final maior que zero e
`total_recebido = 0`, a situação é `PENDENTE`.\
**RN-OS-103** --- Para `0 < total_recebido < TOTAL FINAL DA OS`, a
situação é `PARCIAL`.\
**RN-OS-104** --- Para `total_recebido >= TOTAL FINAL DA OS`, a situação
é `PAGO`.\
**RN-OS-105** --- Quando total final for zero, a interface pode exibir
**"Sem valor a receber"**.\
**RN-OS-106** --- No MVP, o MotorAuto registra pagamentos, mas não
processa transações financeiras externas.

## Interface pública

Consultas: `cliente`, `veiculo`, `profissional_responsavel`,
`quilometragem`, `defeito_relatado`, `diagnostico`, `observacoes`,
`numero`, `data_entrada`, `data_prevista_saida`, `data_saida`, `status`,
`itens_servico`, `itens_peca`, `pagamentos`, `situacao_orcamento`,
`total_orcado`, `total_aprovado`, `total_recusado`, `total_bruto`,
`desconto`, `total_final`, `total_recebido`, `saldo_restante`,
`valor_excedente`, `situacao_pagamento`.

Comportamentos principais: - dados da OS: `atribuir_profissional()`,
`atualizar_quilometragem()`, `registrar_diagnostico()`,
`atualizar_observacoes()`; - itens: `adicionar_item_servico()`,
`remover_item_servico()`, `adicionar_item_peca()`,
`remover_item_peca()`; - alterações de serviço pela OS:
`corrigir_descricao_item_servico()`, `alterar_valor_item_servico()`,
`aprovar_item_servico()`, `recusar_item_servico()`,
`marcar_item_servico_como_pendente()`,
`marcar_item_servico_como_executado()`; - alterações de peça pela OS:
`corrigir_descricao_item_peca()`, `alterar_quantidade_item_peca()`,
`alterar_valor_unitario_item_peca()`, `aprovar_item_peca()`,
`recusar_item_peca()`, `marcar_item_peca_como_pendente()`; - financeiro:
`conceder_desconto()`, `registrar_pagamento()`; - fluxo:
`iniciar_diagnostico()`, `aguardar_aprovacao()`, `iniciar_execucao()`,
`concluir()`, `registrar_entrega()`, `cancelar()`,
`registrar_saida_cancelada()`, `retornar_para_diagnostico()`,
`retornar_para_aprovacao()`, `reabrir_execucao()`.

------------------------------------------------------------------------

# ItemServico

Representa um serviço individual apresentado no orçamento e, quando
aprovado, potencialmente executado.

## Atributos

### Obrigatórios

-   `descricao`
-   `valor`

### Gerados automaticamente

-   `id`
-   `situacao_aprovacao = PENDENTE`
-   `executado = False`

## Regras de negócio

**RN-ITS-001** --- Descrição é obrigatória e normalizada.\
**RN-ITS-002** --- Valor é obrigatório.\
**RN-ITS-003** --- Valor deve ser `Decimal`; `float` não é aceito pelo
domínio.\
**RN-ITS-004** --- Valor não pode ser negativo.\
**RN-ITS-005** --- `Decimal("0.00")` é permitido para cortesia, garantia
ou serviço sem cobrança.\
**RN-ITS-006** --- Todo item inicia `PENDENTE`.\
**RN-ITS-007** --- Enquanto `executado = False`, pode transitar entre
`PENDENTE`, `APROVADO` e `RECUSADO`, respeitando o contexto da OS.\
**RN-ITS-008** --- Item recusado é preservado enquanto permanecer
recusado.\
**RN-ITS-009** --- Antes da execução, o cliente pode mudar sua decisão.\
**RN-ITS-010** --- Todo item inicia `executado = False`.\
**RN-ITS-011** --- Apenas serviço `APROVADO` pode ser marcado como
executado.\
**RN-ITS-012** --- `PENDENTE` ou `RECUSADO` não pode ser executado.\
**RN-ITS-013** --- Após `executado = True`, a aprovação não pode mais
mudar.\
**RN-ITS-014** --- Serviço executado permanece `APROVADO`.\
**RN-ITS-015** --- Descrição e valor podem ser alterados enquanto a OS
permitir.\
**RN-ITS-016** --- Quando vinculado a uma OS, alterações oficiais devem
ser coordenadas pela `OrdemServico`.\
**RN-ITS-017** --- A OS é responsável por verificar se o item pertence
ao agregado e se o status permite a operação.

## Interface pública

Consultas: `descricao`, `valor`, `situacao_aprovacao`, `executado`.

Comportamentos internos do objeto: `corrigir_descricao()`,
`alterar_valor()`, `aprovar()`, `recusar()`, `marcar_como_pendente()`,
`marcar_como_executado()`.

------------------------------------------------------------------------

# ItemPeca

Representa peça, material ou insumo apresentado no orçamento.

## Atributos

### Obrigatórios

-   `descricao`
-   `quantidade`
-   `valor_unitario`

### Gerados automaticamente

-   `id`
-   `situacao_aprovacao = PENDENTE`

### Calculados

-   `subtotal`

## Regras de negócio

**RN-ITP-001** --- Descrição é obrigatória e normalizada.\
**RN-ITP-002** --- Quantidade é obrigatória e deve chegar ao domínio
como `Decimal`.\
**RN-ITP-003** --- Quantidade pode ser inteira ou fracionada, como
`0.5`, `1.5` ou `3.75`.\
**RN-ITP-004** --- Quantidade deve ser maior que zero.\
**RN-ITP-005** --- Valor unitário é obrigatório e deve chegar ao domínio
como `Decimal`.\
**RN-ITP-006** --- `float` não é aceito para valores/quantidades
fracionárias do domínio.\
**RN-ITP-007** --- Valor unitário não pode ser negativo.\
**RN-ITP-008** --- Valor unitário zero é permitido para
cortesia/garantia.\
**RN-ITP-009** --- `subtotal = quantidade × valor_unitario`.\
**RN-ITP-010** --- Subtotal é calculado e não pode ser alterado
diretamente.\
**RN-ITP-011** --- Todo item inicia `PENDENTE`.\
**RN-ITP-012** --- Enquanto a OS permitir, pode transitar entre
`PENDENTE`, `APROVADO` e `RECUSADO`.\
**RN-ITP-013** --- Peça recusada pode voltar para pendente ou aprovada.\
**RN-ITP-014** --- Peça recusada não pode ser excluída enquanto
permanecer recusada.\
**RN-ITP-015** --- Descrição, quantidade e valor unitário podem ser
alterados enquanto a OS permitir.\
**RN-ITP-016** --- Item pendente ou aprovado pode ser removido enquanto
a OS permitir.\
**RN-ITP-017** --- Não haverá estado `utilizada` no MVP.\
**RN-ITP-018** --- Quando vinculada a uma OS, alterações oficiais devem
ser coordenadas pela `OrdemServico`.\
**RN-ITP-019** --- A OS é responsável por verificar se a peça pertence
ao agregado e se o status permite a operação.

## Interface pública

Consultas: `descricao`, `quantidade`, `valor_unitario`, `subtotal`,
`situacao_aprovacao`.

Comportamentos internos do objeto: `corrigir_descricao()`,
`alterar_quantidade()`, `alterar_valor_unitario()`, `aprovar()`,
`recusar()`, `marcar_como_pendente()`.

------------------------------------------------------------------------

# Pagamento

Entidade que representa um recebimento efetivamente aplicado a uma Ordem
de Serviço.

## Atributos

### Obrigatórios

-   `valor`
-   `forma_pagamento`

### Opcionais

-   `observacoes`

### Gerados automaticamente

-   `id`
-   `data_pagamento`

## Regras de negócio

**RN-PAG-001** --- Valor deve ser maior que zero.\
**RN-PAG-002** --- Valor deve chegar ao domínio como `Decimal`; `float`
não é aceito.\
**RN-PAG-003** --- Forma de pagamento deve ser uma `FormaPagamento`
válida.\
**RN-PAG-004** --- Data é registrada quando o pagamento é efetivado.\
**RN-PAG-005** --- Observações são opcionais e normalizadas.\
**RN-PAG-006** --- Uma OS pode possuir múltiplos pagamentos.\
**RN-PAG-007** --- Pagamentos da mesma OS podem usar formas diferentes.\
**RN-PAG-008** --- No MVP, o registro é manual e informativo; o
MotorAuto não processa a transação.\
**RN-PAG-009** --- `CREDITO_CLIENTE` existe como forma de pagamento do
domínio, mas seu uso não ocorre pelo fluxo comum de
`registrar_pagamento()`.\
**RN-PAG-010** --- O uso de `CREDITO_CLIENTE` deve ser coordenado com a
conta de crédito para que débito da conta e aplicação na OS permaneçam
consistentes.

## Interface pública

Consultas: `valor`, `forma_pagamento`, `data_pagamento`, `observacoes`.

------------------------------------------------------------------------

# ContaCreditoCliente

Representa o saldo de crédito/haver mantido para um cliente.

A conta não armazena um saldo mutável independente como fonte de
verdade. O saldo deve ser derivado das movimentações registradas,
preservando rastreabilidade.

## Atributos

### Obrigatórios

-   `cliente`

### Gerados automaticamente

-   `id`

### Composição

-   `movimentacoes`

### Calculados

-   `saldo`

## Regras de negócio

**RN-CCC-001** --- Toda conta de crédito deve pertencer a um `Cliente`
válido.\
**RN-CCC-002** --- A conta mantém uma coleção de
`MovimentacaoCreditoCliente`.\
**RN-CCC-003** --- O saldo é consequência das movimentações, e não um
valor financeiro independente mantido manualmente.\
**RN-CCC-004** --- Entradas de crédito aumentam o saldo.\
**RN-CCC-005** --- Uso em OS reduz o saldo.\
**RN-CCC-006** --- Devoluções reduzem o saldo.\
**RN-CCC-007** --- Ajustes de OS decorrentes de excedente devem aumentar
o crédito disponível do cliente.\
**RN-CCC-008** --- Não pode ser registrada utilização ou devolução
superior ao saldo disponível.\
**RN-CCC-009** --- A conta valida o tipo da movimentação antes de
registrá-la no comportamento correspondente.\
**RN-CCC-010** --- Movimentações expostas publicamente não devem
permitir manipulação direta da coleção interna.\
**RN-CCC-011** --- Um valor entregue antecipadamente pelo cliente, antes
de existir cobrança definida na OS, deve ser registrado como crédito do
cliente e não como pagamento direto da OS.\
**RN-CCC-012** --- Após o total final estar definido, o crédito pode ser
utilizado para pagamento da OS por fluxo coordenado pela camada de
aplicação.\
**RN-CCC-013** --- Crédito remanescente pode permanecer disponível para
atendimentos futuros ou ser devolvido ao cliente por movimentação
própria.

## Interface pública

Consultas: `cliente`, `movimentacoes`, `saldo`.

Comportamentos: `registrar_credito()`, `utilizar_credito_em_os()`,
`registrar_devolucao()` e comportamento correspondente ao ajuste de OS,
conforme a implementação atual da entidade.

------------------------------------------------------------------------

# MovimentacaoCreditoCliente

Representa um lançamento individual no histórico financeiro da
`ContaCreditoCliente`.

Cada movimentação é imutável do ponto de vista histórico depois de
registrada: correções futuras devem ser tratadas por novas movimentações
apropriadas, evitando apagar a trilha financeira.

## Atributos

### Obrigatórios

-   `valor`
-   `tipo`

### Condicionais/opcionais

-   `forma_origem`
-   `ordem_servico`
-   `observacoes`

### Gerados automaticamente

-   `id`
-   data/hora da movimentação, conforme implementação

## Regras de negócio

**RN-MCC-001** --- `valor` deve ser `Decimal` positivo.\
**RN-MCC-002** --- `tipo` deve ser um `TipoMovimentacaoCredito` válido.\
**RN-MCC-003** --- Observações são opcionais e textos vazios são
normalizados para `None`.\
**RN-MCC-004** --- `forma_origem`, quando exigida pela natureza da
movimentação, deve ser uma `FormaPagamento` válida.\
**RN-MCC-005** --- `ordem_servico`, quando exigida pela natureza da
movimentação, deve ser uma `OrdemServico` válida.\
**RN-MCC-006** --- Uma entrada de crédito registra a origem financeira
real do valor recebido do cliente.\
**RN-MCC-007** --- Uso de crédito em OS deve manter referência à OS
correspondente.\
**RN-MCC-008** --- Devolução representa saída de valor da conta para o
cliente.\
**RN-MCC-009** --- Ajuste de OS representa crédito originado de valor
que já havia sido recebido na OS e se tornou excedente após redução do
total final.\
**RN-MCC-010** --- `CREDITO_CLIENTE` não deve ser tratado como origem
externa de uma entrada de crédito, evitando crédito circular.\
**RN-MCC-011** --- As combinações entre `tipo`, `forma_origem` e
`ordem_servico` devem respeitar as validações específicas implementadas
para cada tipo de movimentação.

## Interface pública

Consultas: `valor`, `tipo`, `forma_origem`, `ordem_servico`,
`observacoes` e data/hora da movimentação conforme implementação.

------------------------------------------------------------------------

# Enums do domínio

## FuncaoProfissional

``` text
MECANICO = "Mecânico"
ATENDENTE = "Atendente"
GERENTE = "Gerente"
AUXILIAR = "Auxiliar"
```

## StatusOrdemServico

``` text
ABERTA = "Aberta"
EM_DIAGNOSTICO = "Em diagnóstico"
AGUARDANDO_APROVACAO = "Aguardando aprovação"
EM_EXECUCAO = "Em execução"
CONCLUIDA = "Concluída"
ENTREGUE = "Entregue"
CANCELADA = "Cancelada"
```

## SituacaoAprovacaoItem

``` text
PENDENTE = "Pendente"
APROVADO = "Aprovado"
RECUSADO = "Recusado"
```

## SituacaoOrcamento

``` text
PENDENTE = "Pendente"
APROVADO = "Aprovado"
PARCIALMENTE_APROVADO = "Parcialmente aprovado"
RECUSADO = "Recusado"
```

Sem itens ou com pelo menos um item pendente, a situação é `PENDENTE`.

## FormaPagamento

``` text
DINHEIRO = "Dinheiro"
PIX = "Pix"
CARTAO_DEBITO = "Cartão de débito"
CARTAO_CREDITO = "Cartão de crédito"
CREDITO_CLIENTE = "Crédito do cliente"
```

`CREDITO_CLIENTE` representa consumo de saldo já existente na
`ContaCreditoCliente`; não representa uma nova entrada externa de
dinheiro.

## SituacaoPagamento

``` text
PENDENTE = "Pendente"
PARCIAL = "Parcial"
PAGO = "Pago"
```

A situação é calculada. `TOTAL FINAL DA OS = 0` resulta em `PAGO`. Se
`total_recebido` superar o total final por alteração posterior da OS, a
situação permanece `PAGO` e a diferença aparece em `valor_excedente`.

## TipoMovimentacaoCredito

Tipos consolidados no modelo de crédito:

``` text
CREDITO = "Crédito"
USO_EM_OS = "Uso em OS"
DEVOLUCAO = "Devolução"
AJUSTE_OS = "Ajuste OS"
```

> `AJUSTE_OS` é utilizado para rastrear crédito originado de excedente
> financeiro de uma OS após redução posterior do seu total final.

------------------------------------------------------------------------

# Regras financeiras consolidadas

## OrdemServico

``` text
total_orcado
→ soma atual dos serviços e peças que permanecem registrados na OS

total_aprovado
→ soma dos itens aprovados

total_recusado
→ soma dos itens recusados

total_bruto
→ serviços aprovados e executados
  + peças aprovadas que permanecem na OS

TOTAL FINAL DA OS
→ total_bruto - desconto

total_recebido
→ soma dos pagamentos efetivamente registrados na OS

saldo_restante
→ max(TOTAL FINAL DA OS - total_recebido, 0)

valor_excedente
→ max(total_recebido - TOTAL FINAL DA OS, 0)
```

Não existe mais o antigo invariante:

``` text
total_pago <= TOTAL FINAL DA OS
```

porque o total final pode diminuir **depois** de pagamentos já terem
sido recebidos.

O modelo atual separa os dois lados:

``` text
se total_recebido < total_final
→ existe saldo_restante

se total_recebido = total_final
→ saldo_restante = 0
→ valor_excedente = 0

se total_recebido > total_final
→ saldo_restante = 0
→ existe valor_excedente
```

Situação de pagamento:

``` text
TOTAL FINAL DA OS = 0
→ PAGO
→ interface pode exibir "Sem valor a receber"

TOTAL FINAL DA OS > 0 e total_recebido = 0
→ PENDENTE

0 < total_recebido < TOTAL FINAL DA OS
→ PARCIAL

total_recebido >= TOTAL FINAL DA OS
→ PAGO
```

## Crédito do cliente

Fluxo de entrada antecipada:

``` text
cliente entrega valor antecipadamente
        ↓
ContaCreditoCliente
        ↓
MovimentacaoCreditoCliente(CREDITO)
        ↓
saldo disponível do cliente aumenta
```

O valor não é aplicado diretamente à OS apenas por ter sido entregue
durante um atendimento.

Fluxo de uso:

``` text
TOTAL FINAL DA OS definido
        ↓
cliente possui saldo de crédito
        ↓
camada de aplicação coordena a operação
        ↓
MovimentacaoCreditoCliente(USO_EM_OS)
        +
Pagamento com FormaPagamento.CREDITO_CLIENTE
        ↓
saldo da conta diminui
e
total_recebido da OS aumenta
```

Fluxo de excedente:

``` text
OS já recebeu pagamentos
        ↓
total_final é reduzido
        ↓
total_recebido > total_final
        ↓
valor_excedente
        ↓
camada de aplicação
        ↓
MovimentacaoCreditoCliente(AJUSTE_OS)
        ↓
ContaCreditoCliente recebe o excedente
```

Depois disso, o cliente pode:

``` text
manter o crédito
→ utilizar em OS futura

ou

solicitar devolução
→ MovimentacaoCreditoCliente(DEVOLUCAO)
```

------------------------------------------------------------------------

# Responsabilidades entre camadas

## Domínio

Responsável por: - validar entidades e seus estados; - preservar
invariantes; - calcular totais; - controlar transições de status; -
controlar alterações dos itens da OS; - validar pagamentos
individuais; - validar movimentações de crédito; - calcular saldo da
conta de crédito.

## Camada de aplicação

Responsável por coordenar operações que envolvem mais de um
agregado/entidade independente, principalmente:

``` text
ContaCreditoCliente ↔ OrdemServico
```

Exemplos: - usar crédito do cliente em uma OS; - registrar de forma
consistente a movimentação `USO_EM_OS` e o pagamento
`CREDITO_CLIENTE`; - transformar `valor_excedente` de uma OS em
`AJUSTE_OS`; - evitar duplicidade ao converter um mesmo excedente em
crédito; - coordenar persistência/transação das duas alterações.

## Persistência

Responsável por: - gerar IDs; - gerar número sequencial/único da OS; -
garantir restrições que dependam do banco, como unicidade; - armazenar e
reconstruir entidades sem transferir regras de negócio para o banco.

## Interface

Responsável por: - coletar e apresentar dados; - converter entradas
externas para tipos adequados antes de chegar ao domínio; -
disponibilizar ações permitidas ao usuário; - exibir mensagens amigáveis
a partir das exceções/regras do domínio.

A interface não deve ser a única responsável por impedir operações
inválidas.

------------------------------------------------------------------------

# Decisões técnicas e de domínio

**DT-001 --- Telefone do cliente:** obrigatório.\
**DT-002 --- Quilometragem:** pertence à OS, não ao veículo.\
**DT-003 --- Ano do veículo:** utilizar apenas um campo `ano`.\
**DT-004 --- Validação no domínio:** regras protegidas pelas entidades.\
**DT-005 --- Encapsulamento:** alterações por interface pública.\
**DT-006 --- Correções do veículo:** marca, modelo e ano podem ser
corrigidos.\
**DT-007 --- Limites de ano:** `1886` a `2100`.\
**DT-008 --- Placa:** maiúsculas, sem espaços e sem hífen.\
**DT-009 --- Função do profissional:** representada por Enum.\
**DT-010 --- Funções permitidas:** Mecânico, Atendente, Gerente e
Auxiliar.\
**DT-011 --- Exclusão lógica:** clientes/profissionais com histórico são
desativados.\
**DT-012 --- Salário/comissão:** não pertencem a `Profissional`; ficam
para futuro módulo de gestão de pessoas/contratos.\
**DT-013 --- Quilometragem da OS:** opcional na abertura.\
**DT-014 --- Fluxo da OS:** fluxo principal com retornos controlados e
`CANCELADA` como encerramento excepcional.\
**DT-015 --- Defeito relatado:** obrigatório.\
**DT-016 --- Diagnóstico:** opcional e separado do defeito relatado.\
**DT-017 --- Quantidades fracionadas:** usar `Decimal`.\
**DT-018 --- Número da OS:** único, sequencial, automático, imutável e
gerado pela persistência.\
**DT-019 --- Serviços e peças:** representados por `ItemServico` e
`ItemPeca`.\
**DT-020 --- Valores monetários:** usar `Decimal`; `float` não é aceito
pelo domínio.\
**DT-021 --- Totais:** calculados sempre que possível.\
**DT-022 --- Orçamento:** permanece dentro da OS no MVP.\
**DT-023 --- Aprovação:** individual por item.\
**DT-024 --- Recusados:** preservados no histórico.\
**DT-025 --- Terminologia:** expressão oficial é **TOTAL FINAL DA OS**.\
**DT-026 --- Desconto:** opcional, monetário e manual; forma de
pagamento pode influenciar negociação, mas não concede desconto
automaticamente.\
**DT-027 --- Pagamentos:** coleção de entidades `Pagamento`.\
**DT-028 --- FormaPagamento:** Enum no MVP.\
**DT-029 --- Situação financeira:** calculada.\
**DT-030 --- Integrações futuras:** avaliar APIs de adquirentes,
operadoras e gateways; MVP registra manualmente.\
**DT-031 --- Estados terminais:** `ENTREGUE` e `CANCELADA` são terminais
operacionalmente.\
**DT-032 --- Data de saída:** representa a saída física do veículo.\
**DT-033 --- Pagamento como entidade:** cada recebimento possui
identidade e dados próprios.\
**DT-034 --- Total final zero:** situação `PAGO`; interface pode mostrar
**"Sem valor a receber"**.\
**DT-035 --- Total orçado atual:** soma dos itens que permanecem
registrados; sem versionamento completo no MVP.\
**DT-036 --- Cancelamento:** `CANCELADA` encerra excepcionalmente o
fluxo operacional.\
**DT-037 --- Saída após cancelamento:** pode ser registrada
posteriormente sem alterar `CANCELADA`.\
**DT-038 --- Operacional x financeiro:** status operacional e situação
financeira são independentes.\
**DT-039 --- `total_pago` substituído:** o conceito foi substituído por
`total_recebido`, permitindo representar excedentes posteriores.\
**DT-040 --- Decimal na fronteira:** valores monetários e quantidades
fracionárias devem chegar ao domínio como `Decimal`; conversão é
responsabilidade das camadas externas.\
**DT-041 --- Histórico cliente/veículo:** OS preserva o cliente do
atendimento mesmo após transferência futura do veículo.\
**DT-042 --- Excedente financeiro:** redução posterior do total final
pode gerar `valor_excedente`; isso não invalida a OS.\
**DT-043 --- Saldo restante:** nunca é negativo.\
**DT-044 --- Crédito do cliente:** valores antecipados podem ser
mantidos em uma `ContaCreditoCliente`.\
**DT-045 --- Entrada antecipada:** não é automaticamente pagamento da
OS; primeiro constitui crédito do cliente.\
**DT-046 --- Crédito como pagamento:** `CREDITO_CLIENTE` foi adicionado
a `FormaPagamento`.\
**DT-047 --- Uso de crédito:** deve ser coordenado com movimentação
`USO_EM_OS`.\
**DT-048 --- Devolução:** saída de crédito para o cliente é registrada
como `DEVOLUCAO`.\
**DT-049 --- Ajuste de OS:** excedente originado de redução posterior da
OS é convertido em crédito por `AJUSTE_OS`.\
**DT-050 --- Rastreabilidade do crédito:** saldo é derivado do histórico
de movimentações.\
**DT-051 --- Coordenação entre agregados:** operações que alteram
simultaneamente OS e conta de crédito pertencem à camada de aplicação.\
**DT-052 --- OrdemServico como raiz do agregado:** alterações oficiais
em `ItemServico` e `ItemPeca` vinculados à OS passam pela
`OrdemServico`.\
**DT-053 --- Coleções protegidas:** exposição pública de coleções não
deve permitir alteração direta da coleção interna.\
**DT-054 --- Serviço executado:** só pode ser marcado como executado
quando a OS estiver `EM_EXECUCAO` e o item satisfizer suas próprias
regras.\
**DT-055 --- Timezone:** datas que representam instantes do domínio
devem ser timezone-aware quando fornecidas externamente.

------------------------------------------------------------------------

# Histórico de implementação

## Cliente

-   ✅ Modelagem validada.
-   ✅ Entidade implementada.
-   ✅ Testes automatizados concluídos.
-   ✅ Commit e publicação concluídos.

## Veículo

-   ✅ Modelagem validada.
-   ✅ Entidade implementada.
-   ✅ Testes automatizados concluídos.
-   ✅ Commit e publicação concluídos.

## Profissional

-   ✅ Modelagem validada.
-   ✅ `FuncaoProfissional` implementado.
-   ✅ Entidade implementada.
-   ✅ Testes automatizados concluídos.
-   ✅ Commit e publicação concluídos.

## Itens, orçamento e pagamento

-   ✅ `SituacaoAprovacaoItem` implementado e testado.
-   ✅ `SituacaoOrcamento` implementado e testado.
-   ✅ `ItemServico` implementado e testado.
-   ✅ `ItemPeca` implementado e testado.
-   ✅ `FormaPagamento` implementado e testado.
-   ✅ `SituacaoPagamento` implementado e testado.
-   ✅ `Pagamento` implementado e testado.

## Crédito do cliente

-   ✅ `CREDITO_CLIENTE` incorporado às formas de pagamento.
-   ✅ `TipoMovimentacaoCredito` implementado e testado.
-   ✅ `MovimentacaoCreditoCliente` implementada e testada.
-   ✅ `ContaCreditoCliente` implementada e testada.
-   ✅ Regras de crédito, uso em OS, devolução e ajuste de OS modeladas.
-   🟡 Coordenação transacional entre conta de crédito e OS será
    responsabilidade da futura camada de aplicação.

## OrdemServico

-   ✅ Entidade implementada.
-   ✅ Fluxo operacional e retornos controlados implementados.
-   ✅ Cancelamento e saída de OS cancelada implementados.
-   ✅ Orçamento e aprovação parcial implementados.
-   ✅ Controle de alterações de `ItemServico` e `ItemPeca` pela OS
    implementado.
-   ✅ `total_orcado`, `total_aprovado`, `total_recusado` e
    `total_bruto` implementados.
-   ✅ Desconto e `total_final` implementados.
-   ✅ `total_recebido`, `saldo_restante` e `valor_excedente`
    implementados.
-   ✅ Regras de pagamento implementadas.
-   ✅ Testes automatizados da `OrdemServico` concluídos.
-   ✅ Suíte completa da etapa: **262 testes passando**.

------------------------------------------------------------------------

# Próxima etapa

O núcleo de domínio da Ordem de Serviço está implementado e coberto por
testes. A próxima evolução recomendada é iniciar a **camada de
aplicação**, começando pelos casos de uso que coordenam `OrdemServico` e
`ContaCreditoCliente`.

Prioridade sugerida:

``` text
Casos de uso / serviços de aplicação
        ↓
registrar entrada como crédito do cliente
        ↓
utilizar crédito em uma OS
        ↓
converter valor_excedente em AJUSTE_OS
        ↓
registrar devolução de crédito
        ↓
persistência SQLite / repositórios
        ↓
integração com interface PySide6
```

A camada de aplicação deve evitar duplicidade e garantir que operações
compostas sejam tratadas de forma consistente.

------------------------------------------------------------------------

# Observações

-   Mudanças de regras de negócio devem ser registradas neste documento
    antes ou junto da alteração no código.
-   Detalhes puramente internos de implementação permanecem
    preferencialmente no código-fonte.
-   A interface gráfica deve permanecer desacoplada das regras de
    negócio.
-   A interface pode oferecer ações intuitivas, mas as validações
    pertencem ao domínio.
-   `OrdemServico` coordena as alterações dos itens que pertencem ao seu
    agregado.
-   Operações que envolvem simultaneamente `OrdemServico` e
    `ContaCreditoCliente` devem ser coordenadas pela camada de
    aplicação.
-   A arquitetura continua mantendo regras de negócio independentes da
    interface e da persistência, favorecendo futura evolução do
    MotorAuto para outras interfaces e integrações.
