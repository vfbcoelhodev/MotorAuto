# 🚗 Modelo do Domínio

Este documento descreve as principais entidades, enums, relacionamentos, regras de negócio e decisões técnicas já validadas para o sistema **MotorAuto**.

> **Importante:** este é um documento vivo. Deve ser atualizado sempre que uma regra de negócio for criada, alterada ou removida.

---

## Convenções

- **Obrigatório:** deve ser informado para que a entidade seja válida.
- **Opcional:** pode ser omitido.
- **Gerado automaticamente:** definido pelo sistema ou pela persistência.
- **Calculado:** derivado de outros dados do domínio e não mantido como fonte independente de verdade.
- ✅ **Implementada e testada**
- 🟡 **Modelagem validada**
- ⏳ **Em definição**

---

# Visão geral do domínio

| Estrutura | Tipo | Situação |
|---|---|---|
| Cliente | Entidade | ✅ Implementada e testada |
| Veículo | Entidade | ✅ Implementada e testada |
| Profissional | Entidade | ✅ Implementada e testada |
| Ordem de Serviço | Entidade | 🟡 Modelagem validada |
| ItemServico | Composição da OS | 🟡 Modelagem validada |
| ItemPeca | Composição da OS | 🟡 Modelagem validada |
| Pagamento | Entidade | 🟡 Modelagem validada |
| FuncaoProfissional | Enum | ✅ Implementado e testado |
| StatusOrdemServico | Enum | 🟡 Modelagem validada |
| SituacaoAprovacaoItem | Enum | 🟡 Modelagem validada |
| SituacaoOrcamento | Enum calculado/conceitual | 🟡 Modelagem validada |
| FormaPagamento | Enum | 🟡 Modelagem validada |
| SituacaoPagamento | Enum calculado/conceitual | 🟡 Modelagem validada |

---

# Relacionamentos

```text
Cliente (1) ───────── possui ───────────────► Veículo (N)
Cliente (1) ───────── solicita ─────────────► Ordem de Serviço (N)
Veículo (1) ───────── recebe ───────────────► Ordem de Serviço (N)
Profissional (1) ──── pode ser responsável ► Ordem de Serviço (N)

Ordem de Serviço (1)
        ├──────── contém ───────────────► ItemServico (N)
        ├──────── utiliza ──────────────► ItemPeca (N)
        └──────── possui ───────────────► Pagamento (0..N)

ItemServico ───────── usa ──────────────► SituacaoAprovacaoItem
ItemPeca ──────────── usa ──────────────► SituacaoAprovacaoItem
Pagamento ─────────── usa ──────────────► FormaPagamento
Ordem de Serviço ──── usa ──────────────► StatusOrdemServico
```

Na abertura da OS, o veículo deverá pertencer ao cliente informado. A OS preservará historicamente o cliente daquele atendimento mesmo que o veículo seja transferido posteriormente.

---

# Cliente

Representa uma pessoa física ou empresa atendida pela oficina.

## Atributos

### Obrigatórios
- `nome`
- `telefone`

### Opcionais
- `possui_whatsapp`
- `cpf`
- `endereco`
- `observacoes`

### Gerados automaticamente
- `id`
- `data_cadastro`
- `ativo`

## Regras de negócio

**RN-CLI-001** — Todo cliente deve possuir nome.  
**RN-CLI-002** — Todo cliente deve possuir telefone.  
**RN-CLI-003** — Nome e telefone devem ser normalizados, removendo espaços excedentes nas extremidades.  
**RN-CLI-004** — CPF, endereço e observações são opcionais.  
**RN-CLI-005** — Textos opcionais contendo apenas espaços devem virar `None`.  
**RN-CLI-006** — Todo cliente inicia ativo.  
**RN-CLI-007** — Clientes com histórico não devem ser excluídos fisicamente.  
**RN-CLI-008** — O cadastro poderá ser ativado ou desativado, preservando o histórico.  
**RN-CLI-009** — A data de cadastro será preenchida automaticamente.  
**RN-CLI-010** — O identificador será gerado pela persistência.  
**RN-CLI-011** — Nome e telefone somente poderão ser alterados pela interface pública.  
**RN-CLI-012** — Alterações respeitarão as mesmas validações da criação.  
**RN-CLI-013** — Uma tentativa inválida não poderá modificar o estado anterior.

## Interface pública

Consultas: `nome`, `telefone`, `cpf`, `endereco`, `observacoes`, `possui_whatsapp`, `ativo`, `data_cadastro`.

Comportamentos: `atualizar_nome()`, `atualizar_telefone()`, `atualizar_cpf()`, `atualizar_endereco()`, `atualizar_observacoes()`, `ativar_whatsapp()`, `desativar_whatsapp()`, `ativar()`, `desativar()`.

---

# Veículo

Representa um veículo pertencente a um cliente e que poderá possuir histórico de Ordens de Serviço.

## Atributos

### Obrigatórios
- `cliente`
- `marca`
- `modelo`

### Opcionais
- `ano`
- `placa`
- `combustivel`
- `observacoes`

### Gerados automaticamente
- `id`

## Regras de negócio

**RN-VEI-001** — Todo veículo deve estar associado a um cliente válido.  
**RN-VEI-002** — Marca é obrigatória.  
**RN-VEI-003** — Modelo é obrigatório.  
**RN-VEI-004** — Marca e modelo devem ser normalizados.  
**RN-VEI-005** — Ano é opcional.  
**RN-VEI-006** — Quando informado, ano deve ser inteiro entre `1886` e `2100`.  
**RN-VEI-007** — Placa é opcional.  
**RN-VEI-008** — A placa informada será normalizada para maiúsculas, sem espaços e sem hífen.  
**RN-VEI-009** — A unicidade da placa será garantida pela persistência.  
**RN-VEI-010** — Combustível e observações são opcionais.  
**RN-VEI-011** — Textos opcionais contendo apenas espaços devem virar `None`.  
**RN-VEI-012** — Quilometragem não pertence ao cadastro do veículo.  
**RN-VEI-013** — Quilometragem será registrada em cada OS.  
**RN-VEI-014** — O histórico de quilometragem será obtido pelas OS.  
**RN-VEI-015** — Transferência de propriedade não apaga o histórico.  
**RN-VEI-016** — Marca, modelo e ano são características estáveis.  
**RN-VEI-017** — Alterações nesses campos serão tratadas como correções cadastrais.  
**RN-VEI-018** — Correção inválida não modifica o estado anterior.  
**RN-VEI-019** — Atributos sujeitos a regras devem permanecer protegidos.  
**RN-VEI-020** — Alterações ocorrerão pela interface pública.

## Interface pública

Consultas: `cliente`, `marca`, `modelo`, `ano`, `placa`, `combustivel`, `observacoes`.

Comportamentos: `corrigir_marca()`, `corrigir_modelo()`, `corrigir_ano()`, `atualizar_placa()`, `atualizar_combustivel()`, `atualizar_observacoes()`, `transferir_propriedade()`.

---

# Profissional

Representa um colaborador da oficina responsável por atendimento, execução, auxílio operacional ou gerenciamento.

## Atributos

### Obrigatórios
- `nome`
- `telefone`
- `funcao`

### Opcionais
- `observacoes`

### Gerados automaticamente
- `id`
- `data_cadastro`
- `ativo`

## Regras de negócio

**RN-PRO-001** — Nome é obrigatório.  
**RN-PRO-002** — Telefone é obrigatório.  
**RN-PRO-003** — Função válida é obrigatória.  
**RN-PRO-004** — Funções permitidas: Mecânico, Atendente, Gerente e Auxiliar.  
**RN-PRO-005** — Função será representada por `FuncaoProfissional`.  
**RN-PRO-006** — Nome e telefone serão normalizados.  
**RN-PRO-007** — Observações são opcionais.  
**RN-PRO-008** — Observações vazias serão normalizadas para `None`.  
**RN-PRO-009** — Todo profissional inicia ativo.  
**RN-PRO-010** — Profissional com histórico não deverá ser excluído fisicamente.  
**RN-PRO-011** — Poderá ser desativado preservando associações anteriores.  
**RN-PRO-012** — Data de cadastro será automática.  
**RN-PRO-013** — ID será gerado pela persistência.  
**RN-PRO-014** — Atributos sujeitos a regras permanecerão protegidos.  
**RN-PRO-015** — Alterações ocorrerão pela interface pública.  
**RN-PRO-016** — Alteração inválida não modifica o estado anterior.

## Interface pública

Consultas: `nome`, `telefone`, `funcao`, `observacoes`, `ativo`, `data_cadastro`.

Comportamentos: `atualizar_nome()`, `atualizar_telefone()`, `alterar_funcao()`, `atualizar_observacoes()`, `ativar()`, `desativar()`.

---

# Ordem de Serviço

Representa o atendimento desde a entrada do veículo até seu encerramento operacional, incluindo diagnóstico, orçamento, aprovações, execução, peças, valores e pagamentos.

## Atributos

### Obrigatórios na abertura
- `cliente`
- `veiculo`
- `defeito_relatado`

### Opcionais
- `profissional_responsavel`
- `quilometragem`
- `diagnostico`
- `observacoes`
- `data_prevista_saida`

### Gerados automaticamente
- `id`
- `numero`
- `data_entrada`
- `status`
- `data_saida` — preenchida quando o veículo efetivamente deixar a oficina

### Composições
- `itens_servico`
- `itens_peca`
- `pagamentos`

### Financeiro armazenado
- `desconto`

### Calculados
- `situacao_orcamento`
- `total_orcado`
- `total_aprovado`
- `total_recusado`
- `total_bruto`
- `total_final`
- `total_pago`
- `saldo_restante`
- `situacao_pagamento`

## Regras de negócio

### Abertura e histórico

**RN-OS-001** — Toda OS deve possuir referência direta a um cliente.  
**RN-OS-002** — Toda OS deve possuir referência direta a um veículo.  
**RN-OS-003** — Na abertura, o veículo deverá pertencer ao cliente associado à OS.  
**RN-OS-004** — A OS preservará historicamente o cliente do atendimento, mesmo após transferência futura do veículo.  
**RN-OS-005** — Defeito relatado é obrigatório.  
**RN-OS-006** — Quilometragem é opcional na abertura e poderá ser informada depois.  
**RN-OS-007** — A OS poderá ser aberta sem profissional responsável.  
**RN-OS-008** — Um profissional poderá ser atribuído posteriormente.  
**RN-OS-009** — Diagnóstico é opcional e não substitui o defeito relatado.

### Identificação e datas

**RN-OS-010** — O número da OS será único, sequencial, automático e imutável.  
**RN-OS-011** — A geração do número será responsabilidade da persistência.  
**RN-OS-012** — `data_entrada` será preenchida automaticamente na criação.  
**RN-OS-013** — `data_saida` representa o momento em que o veículo efetivamente deixa a oficina.  
**RN-OS-014** — `data_saida` permanece `None` enquanto o veículo estiver fisicamente na oficina.  
**RN-OS-015** — Na entrega normal, `registrar_entrega()` altera o status para `ENTREGUE` e preenche `data_saida`.  
**RN-OS-016** — Uma OS `CANCELADA` poderá permanecer com `data_saida = None` enquanto o veículo ainda estiver na oficina.  
**RN-OS-017** — Na retirada de veículo de OS `CANCELADA`, `data_saida` será preenchida sem alterar o status.

### Status e transições

**RN-OS-018** — Toda OS inicia `ABERTA`.

Fluxo principal:

```text
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

**RN-OS-019** — Status será alterado somente por comportamentos específicos da entidade.  
**RN-OS-020** — Retornos controlados serão permitidos enquanto a OS não estiver em estado terminal.  
**RN-OS-021** — Retornos previstos:
- `AGUARDANDO_APROVACAO → EM_DIAGNOSTICO`
- `EM_EXECUCAO → AGUARDANDO_APROVACAO`
- `EM_EXECUCAO → EM_DIAGNOSTICO`
- `CONCLUIDA → EM_EXECUCAO`

**RN-OS-022** — `ENTREGUE` e `CANCELADA` são estados terminais do fluxo operacional.  
**RN-OS-023** — Uma OS poderá ser cancelada antes da entrega por desistência, cancelamento do atendimento ou outra interrupção que impeça a conclusão normal.  
**RN-OS-024** — O cancelamento ocorrerá por comportamento explícito, como `cancelar()`.  
**RN-OS-025** — Estados terminais bloqueiam alterações operacionais normais.  
**RN-OS-026** — Correções operacionais posteriores dependerão de mecanismo futuro específico de reabertura/auditoria.  
**RN-OS-027** — Estado operacional e situação financeira são independentes. Uma OS terminal poderá continuar recebendo pagamentos enquanto houver saldo em aberto.

### Orçamento e aprovação

**RN-OS-028** — O orçamento fará parte da própria OS no MVP.  
**RN-OS-029** — Serviços e peças serão itens estruturados.  
**RN-OS-030** — A aprovação poderá ser parcial.  
**RN-OS-031** — Cada item terá `PENDENTE`, `APROVADO` ou `RECUSADO`.  
**RN-OS-032** — `situacao_orcamento` será calculada a partir dos itens.  
**RN-OS-033** — Sem itens, a situação geral será `PENDENTE`.  
**RN-OS-034** — Existindo pelo menos um item `PENDENTE`, a situação geral será `PENDENTE`.  
**RN-OS-035** — Com todos os itens decididos:
- todos aprovados → `APROVADO`;
- todos recusados → `RECUSADO`;
- aprovados + recusados → `PARCIALMENTE_APROVADO`.

**RN-OS-036** — Itens recusados serão preservados no histórico.

### Inclusão, alteração e remoção

**RN-OS-037** — Itens poderão ser adicionados, alterados ou removidos em `ABERTA`, `EM_DIAGNOSTICO`, `AGUARDANDO_APROVACAO` ou `EM_EXECUCAO`, respeitando suas regras específicas.  
**RN-OS-038** — Em `CONCLUIDA`, `ENTREGUE` ou `CANCELADA`, itens ficam bloqueados para alterações normais.  
**RN-OS-039** — Itens `PENDENTE` ou `APROVADO` poderão ser removidos enquanto a OS permitir.  
**RN-OS-040** — Itens `RECUSADO` não poderão ser excluídos enquanto permanecerem recusados.  
**RN-OS-041** — A interface poderá oferecer lixeira, mas a validação será responsabilidade da OS.  
**RN-OS-042** — A interface não manipulará diretamente as coleções internas.

### Conclusão

**RN-OS-043** — A OS não poderá ser concluída com itens `PENDENTE`.  
**RN-OS-044** — Poderá ser concluída sem serviços executados quando todos os itens forem recusados.  
**RN-OS-045** — Serviços que compõem a cobrança deverão estar aprovados e executados.  
**RN-OS-046** — `CONCLUIDA` significa que o trabalho terminou; o veículo poderá continuar na oficina.

### Totais do orçamento

**RN-OS-047** — `total_orcado` é a soma atual dos itens que permanecem registrados na OS como componentes do orçamento.  
**RN-OS-048** — Item removido deixa de compor `total_orcado`.  
**RN-OS-049** — Item recusado permanece registrado e continua compondo `total_orcado`.  
**RN-OS-050** — O MVP não preservará versões completas anteriores do orçamento.  
**RN-OS-051** — `total_aprovado` será calculado pelos itens aprovados.  
**RN-OS-052** — `total_recusado` será calculado pelos itens recusados.  
**RN-OS-053** — Totais calculados não poderão ser alterados diretamente.

### Total bruto, desconto e TOTAL FINAL DA OS

**RN-OS-054** — `total_bruto` será calculado pelos itens efetivamente executados/cobrados.  
**RN-OS-055** — `ItemServico` compõe `total_bruto` somente quando `APROVADO` e `executado = True`.  
**RN-OS-056** — `ItemPeca` compõe `total_bruto` quando `APROVADO` e permanece na OS.  
**RN-OS-057** — Itens pendentes ou recusados não compõem o total bruto/final.  
**RN-OS-058** — Serviço aprovado mas não executado não será cobrado.  
**RN-OS-059** — Desconto será opcional e aplicado sobre o total bruto.  
**RN-OS-060** — Desconto será `Decimal` e inicia em `Decimal("0.00")`.  
**RN-OS-061** — Desconto será concedido manualmente; forma de pagamento não concede desconto automaticamente.  
**RN-OS-062** — A forma de pagamento poderá ser considerada na negociação.  
**RN-OS-063** — Desconto não poderá ser negativo nem superior ao total bruto.  
**RN-OS-064** — Desconto poderá ser concedido/alterado apenas antes de estado terminal.  
**RN-OS-065** — Alteração de desconto será rejeitada se fizer `TOTAL FINAL DA OS < total_pago`.  
**RN-OS-066** — Nenhuma operação que altere itens, aprovações, quantidades, valores ou desconto poderá fazer `TOTAL FINAL DA OS < total_pago`.  
**RN-OS-067** — O domínio preservará o invariante:

```text
0 <= total_pago <= TOTAL FINAL DA OS
```

**RN-OS-068** — O **TOTAL FINAL DA OS** será:

```text
TOTAL FINAL DA OS = total_bruto - desconto
```

**RN-OS-069** — Na interface, **TOTAL FINAL DA OS** será a informação financeira principal e ficará em evidência.

### Pagamentos

**RN-OS-070** — A OS poderá possuir zero ou vários pagamentos.  
**RN-OS-071** — Pagamentos poderão ocorrer em formas e datas diferentes.  
**RN-OS-072** — `total_pago` será a soma dos pagamentos registrados.  
**RN-OS-073** — `saldo_restante = TOTAL FINAL DA OS - total_pago`.  
**RN-OS-074** — A soma dos pagamentos nunca poderá ultrapassar o `TOTAL FINAL DA OS`.  
**RN-OS-075** — Um novo pagamento somente será aceito se:

```text
total_pago + novo_pagamento <= TOTAL FINAL DA OS
```

**RN-OS-076** — `situacao_pagamento` será calculada, não armazenada como fonte independente.  
**RN-OS-077** — Se `TOTAL FINAL DA OS = R$ 0,00`, a situação será `PAGO`, mesmo sem pagamentos registrados.  
**RN-OS-078** — Para total final maior que zero e `total_pago = 0`, situação será `PENDENTE`.  
**RN-OS-079** — Para `0 < total_pago < TOTAL FINAL DA OS`, situação será `PARCIAL`.  
**RN-OS-080** — Para `total_pago = TOTAL FINAL DA OS`, situação será `PAGO`.  
**RN-OS-081** — Quando total final for zero, a interface poderá exibir a observação secundária **“Sem valor a receber”**.  
**RN-OS-082** — A OS poderá ser `ENTREGUE` ou `CANCELADA` com saldo em aberto.  
**RN-OS-083** — Pagamentos posteriores poderão ser registrados em OS terminal enquanto houver saldo.  
**RN-OS-084** — Pagamento posterior não altera o status operacional.  
**RN-OS-085** — No MVP, o MotorAuto registra pagamentos, mas não processa transações financeiras externas.

## Interface pública prevista

Consultas: `cliente`, `veiculo`, `profissional_responsavel`, `quilometragem`, `defeito_relatado`, `diagnostico`, `observacoes`, `numero`, `data_entrada`, `data_prevista_saida`, `data_saida`, `status`, `itens_servico`, `itens_peca`, `pagamentos`, `situacao_orcamento`, `total_orcado`, `total_aprovado`, `total_recusado`, `total_bruto`, `desconto`, `total_final`, `total_pago`, `saldo_restante`, `situacao_pagamento`.

Comportamentos previstos: `atribuir_profissional()`, `atualizar_quilometragem()`, `registrar_diagnostico()`, `atualizar_observacoes()`, `adicionar_item_servico()`, `remover_item_servico()`, `adicionar_item_peca()`, `remover_item_peca()`, `conceder_desconto()`, `registrar_pagamento()`, `iniciar_diagnostico()`, `aguardar_aprovacao()`, `iniciar_execucao()`, `concluir()`, `registrar_entrega()`, `cancelar()`, `registrar_saida_cancelada()`.

---

# ItemServico

Representa um serviço individual apresentado no orçamento e, quando aprovado, potencialmente executado.

## Atributos

### Obrigatórios
- `descricao`
- `valor`

### Gerados automaticamente
- `id`
- `situacao_aprovacao = PENDENTE`
- `executado = False`

## Regras de negócio

**RN-ITS-001** — Descrição é obrigatória e normalizada.  
**RN-ITS-002** — Valor é obrigatório.  
**RN-ITS-003** — Valor será `Decimal`; `float` não será aceito pelo domínio.  
**RN-ITS-004** — Valor não poderá ser negativo.  
**RN-ITS-005** — `Decimal("0.00")` será permitido para cortesia, garantia ou serviço sem cobrança.  
**RN-ITS-006** — Todo item inicia `PENDENTE`.  
**RN-ITS-007** — Enquanto `executado = False`, poderá transitar entre `PENDENTE`, `APROVADO` e `RECUSADO`.  
**RN-ITS-008** — Item recusado será preservado enquanto permanecer recusado.  
**RN-ITS-009** — Antes da execução, o cliente poderá mudar sua decisão.  
**RN-ITS-010** — Todo item inicia `executado = False`.  
**RN-ITS-011** — Apenas serviço `APROVADO` poderá ser marcado como executado.  
**RN-ITS-012** — `PENDENTE` ou `RECUSADO` não poderá ser executado.  
**RN-ITS-013** — Após `executado = True`, aprovação não poderá mais mudar.  
**RN-ITS-014** — Serviço executado permanecerá `APROVADO`.  
**RN-ITS-015** — Descrição e valor poderão ser alterados enquanto a OS permitir.  
**RN-ITS-016** — A OS decide se seu status permite a alteração.

## Interface pública prevista

Consultas: `descricao`, `valor`, `situacao_aprovacao`, `executado`.

Comportamentos: `corrigir_descricao()`, `alterar_valor()`, `aprovar()`, `recusar()`, `marcar_como_pendente()`, `marcar_como_executado()`.

---

# ItemPeca

Representa peça, material ou insumo apresentado no orçamento.

## Atributos

### Obrigatórios
- `descricao`
- `quantidade`
- `valor_unitario`

### Gerados automaticamente
- `id`
- `situacao_aprovacao = PENDENTE`

### Calculados
- `subtotal`

## Regras de negócio

**RN-ITP-001** — Descrição é obrigatória e normalizada.  
**RN-ITP-002** — Quantidade é obrigatória e deverá chegar ao domínio como `Decimal`.  
**RN-ITP-003** — Quantidade poderá ser inteira ou fracionada, como `0.5`, `1.5` ou `3.75`.  
**RN-ITP-004** — Quantidade deverá ser maior que zero.  
**RN-ITP-005** — Valor unitário é obrigatório e deverá chegar ao domínio como `Decimal`.  
**RN-ITP-006** — `float` não será aceito para valores/quantidades fracionárias do domínio.  
**RN-ITP-007** — Valor unitário não poderá ser negativo.  
**RN-ITP-008** — Valor unitário zero será permitido para cortesia/garantia.  
**RN-ITP-009** — `subtotal = quantidade × valor_unitario`.  
**RN-ITP-010** — Subtotal é calculado e não pode ser alterado diretamente.  
**RN-ITP-011** — Todo item inicia `PENDENTE`.  
**RN-ITP-012** — Enquanto a OS permitir, poderá transitar entre `PENDENTE`, `APROVADO` e `RECUSADO`.  
**RN-ITP-013** — Peça recusada poderá voltar para pendente ou aprovada.  
**RN-ITP-014** — Peça recusada não poderá ser excluída enquanto permanecer recusada.  
**RN-ITP-015** — Descrição, quantidade e valor unitário poderão ser alterados enquanto a OS permitir.  
**RN-ITP-016** — Item pendente ou aprovado poderá ser removido enquanto a OS permitir.  
**RN-ITP-017** — Não haverá estado `utilizada` no MVP; peça aprovada que deixe de ser necessária poderá ser removida antes do fechamento.

## Interface pública prevista

Consultas: `descricao`, `quantidade`, `valor_unitario`, `subtotal`, `situacao_aprovacao`.

Comportamentos: `corrigir_descricao()`, `alterar_quantidade()`, `alterar_valor_unitario()`, `aprovar()`, `recusar()`, `marcar_como_pendente()`.

---

# Pagamento

Entidade que representa um recebimento efetivamente realizado e associado a uma Ordem de Serviço.

## Atributos

### Obrigatórios
- `valor`
- `forma_pagamento`

### Opcionais
- `observacoes`

### Gerados automaticamente
- `id`
- `data_pagamento`

## Regras de negócio

**RN-PAG-001** — Valor deverá ser maior que zero.  
**RN-PAG-002** — Valor deverá chegar ao domínio como `Decimal`; `float` não será aceito.  
**RN-PAG-003** — Forma de pagamento deverá ser uma `FormaPagamento` válida.  
**RN-PAG-004** — Data será registrada quando o pagamento for efetivado.  
**RN-PAG-005** — Observações são opcionais.  
**RN-PAG-006** — Uma OS poderá possuir múltiplos pagamentos.  
**RN-PAG-007** — Pagamentos da mesma OS poderão usar formas diferentes.  
**RN-PAG-008** — No MVP, o registro é manual e informativo; o MotorAuto não processará a transação.

## Interface pública prevista

Consultas: `valor`, `forma_pagamento`, `data_pagamento`, `observacoes`.

---

# Enums do domínio

## FuncaoProfissional

```text
MECANICO = "Mecânico"
ATENDENTE = "Atendente"
GERENTE = "Gerente"
AUXILIAR = "Auxiliar"
```

## StatusOrdemServico

```text
ABERTA = "Aberta"
EM_DIAGNOSTICO = "Em diagnóstico"
AGUARDANDO_APROVACAO = "Aguardando aprovação"
EM_EXECUCAO = "Em execução"
CONCLUIDA = "Concluída"
ENTREGUE = "Entregue"
CANCELADA = "Cancelada"
```

## SituacaoAprovacaoItem

```text
PENDENTE = "Pendente"
APROVADO = "Aprovado"
RECUSADO = "Recusado"
```

## SituacaoOrcamento

```text
PENDENTE = "Pendente"
APROVADO = "Aprovado"
PARCIALMENTE_APROVADO = "Parcialmente aprovado"
RECUSADO = "Recusado"
```

Sem itens ou com pelo menos um item pendente, a situação será `PENDENTE`.

## FormaPagamento

Valores iniciais previstos para o MVP:

```text
DINHEIRO = "Dinheiro"
PIX = "Pix"
CARTAO_DEBITO = "Cartão de débito"
CARTAO_CREDITO = "Cartão de crédito"
```

## SituacaoPagamento

```text
PENDENTE = "Pendente"
PARCIAL = "Parcial"
PAGO = "Pago"
```

A situação é calculada. `TOTAL FINAL DA OS = 0` resulta em `PAGO`.

---

# Regras financeiras consolidadas

```text
total_orcado
→ soma atual dos itens que permanecem registrados na OS

total_aprovado
→ soma dos itens aprovados

total_recusado
→ soma dos itens recusados

total_bruto
→ serviços aprovados e executados
  + peças aprovadas que permanecem na OS

TOTAL FINAL DA OS
→ total_bruto - desconto

total_pago
→ soma dos pagamentos

saldo_restante
→ TOTAL FINAL DA OS - total_pago
```

Invariante:

```text
0 <= total_pago <= TOTAL FINAL DA OS
```

Situação:

```text
TOTAL FINAL DA OS = 0
→ PAGO
→ interface: "Sem valor a receber"

TOTAL FINAL DA OS > 0 e total_pago = 0
→ PENDENTE

0 < total_pago < TOTAL FINAL DA OS
→ PARCIAL

total_pago = TOTAL FINAL DA OS
→ PAGO
```

---

# Decisões técnicas e de domínio

**DT-001 — Telefone do cliente:** obrigatório.  
**DT-002 — Quilometragem:** pertence à OS, não ao veículo.  
**DT-003 — Ano do veículo:** utilizar apenas um campo `ano`.  
**DT-004 — Validação no domínio:** regras protegidas pelas entidades.  
**DT-005 — Encapsulamento:** alterações por interface pública.  
**DT-006 — Correções do veículo:** marca, modelo e ano podem ser corrigidos.  
**DT-007 — Limites de ano:** `1886` a `2100`.  
**DT-008 — Placa:** maiúsculas, sem espaços e sem hífen.  
**DT-009 — Função do profissional:** representada por Enum.  
**DT-010 — Funções permitidas:** Mecânico, Atendente, Gerente e Auxiliar.  
**DT-011 — Exclusão lógica:** clientes/profissionais com histórico são desativados.  
**DT-012 — Salário/comissão:** não pertencem a `Profissional`; ficam para futuro módulo de gestão de pessoas/contratos.  
**DT-013 — Quilometragem da OS:** opcional na abertura.  
**DT-014 — Fluxo da OS:** fluxo principal com retornos controlados e `CANCELADA` como encerramento excepcional.  
**DT-015 — Defeito relatado:** obrigatório.  
**DT-016 — Diagnóstico:** opcional e separado do defeito relatado.  
**DT-017 — Quantidades fracionadas:** usar `Decimal`.  
**DT-018 — Número da OS:** único, sequencial, automático, imutável e gerado pela persistência.  
**DT-019 — Serviços e peças:** representados por `ItemServico` e `ItemPeca`.  
**DT-020 — Valores monetários:** usar `Decimal`; `float` não será aceito pelo domínio.  
**DT-021 — Totais:** calculados sempre que possível.  
**DT-022 — Orçamento:** permanece dentro da OS no MVP.  
**DT-023 — Aprovação:** individual por item.  
**DT-024 — Recusados:** preservados no histórico.  
**DT-025 — Terminologia:** expressão oficial é **TOTAL FINAL DA OS**.  
**DT-026 — Desconto:** opcional, monetário e manual; forma de pagamento pode influenciar negociação, mas não concede desconto automaticamente.  
**DT-027 — Pagamentos:** coleção de entidades `Pagamento`.  
**DT-028 — FormaPagamento:** Enum no MVP.  
**DT-029 — Situação financeira:** calculada.  
**DT-030 — Integrações futuras:** avaliar APIs de adquirentes, operadoras e gateways; MVP registra manualmente.  
**DT-031 — Estados terminais:** `ENTREGUE` e `CANCELADA` são terminais operacionalmente.  
**DT-032 — Data de saída:** representa a saída física do veículo.  
**DT-033 — Pagamento como entidade:** cada recebimento possui identidade e dados próprios.  
**DT-034 — Total final zero:** situação `PAGO`; interface pode mostrar **“Sem valor a receber”**.  
**DT-035 — Total orçado atual:** soma dos itens que permanecem registrados; sem versionamento completo no MVP.  
**DT-036 — Cancelamento:** `CANCELADA` encerra excepcionalmente o fluxo operacional.  
**DT-037 — Saída após cancelamento:** pode ser registrada posteriormente sem alterar `CANCELADA`.  
**DT-038 — Operacional x financeiro:** status operacional e situação financeira são independentes.  
**DT-039 — Invariante financeiro:** `0 <= total_pago <= TOTAL FINAL DA OS`.  
**DT-040 — Decimal na fronteira:** valores monetários e quantidades fracionárias devem chegar ao domínio como `Decimal`; conversão é responsabilidade das camadas externas.  
**DT-041 — Histórico cliente/veículo:** OS preserva o cliente do atendimento mesmo após transferência futura do veículo.

---

# Histórico de implementação

## Cliente
- ✅ Modelagem validada.
- ✅ Entidade implementada.
- ✅ Testes automatizados concluídos.
- ✅ Commit e publicação no GitHub concluídos.

## Veículo
- ✅ Modelagem validada.
- ✅ Entidade implementada.
- ✅ Testes automatizados concluídos.
- ✅ Commit e publicação no GitHub concluídos.

## Profissional
- ✅ Modelagem validada.
- ✅ `FuncaoProfissional` implementado.
- ✅ Entidade implementada.
- ✅ Testes automatizados concluídos.
- ✅ Commit e publicação no GitHub concluídos.

## Ordem de Serviço e estruturas relacionadas
- ✅ Modelagem conceitual da `OrdemServico` validada para o MVP.
- ✅ Modelagem de `ItemServico` validada.
- ✅ Modelagem de `ItemPeca` validada.
- ✅ Modelagem de `Pagamento` validada e classificada como entidade.
- ✅ Fluxo, retornos controlados e cancelamento definidos.
- ✅ Orçamento e aprovação parcial definidos.
- ✅ Totais, desconto, pagamentos e invariantes financeiros definidos.
- ✅ Independência entre estado operacional e situação financeira definida.
- ✅ Três rodadas de revisão conceitual concluídas.
- ⏳ Enums relacionados ainda serão implementados.
- ⏳ Novas entidades/composições ainda serão implementadas.
- ⏳ Testes automatizados correspondentes ainda serão criados.

---

# Próxima etapa

Implementação incremental do núcleo da Ordem de Serviço:

```text
SituacaoAprovacaoItem
StatusOrdemServico
FormaPagamento
SituacaoPagamento
SituacaoOrcamento
        ↓
ItemServico
        ↓
ItemPeca
        ↓
Pagamento
        ↓
OrdemServico
        ↓
Testes automatizados incrementais
```

A sequência poderá ser refinada conforme as dependências reais aparecerem no código.

---

# Observações

- Mudanças de regras de negócio devem ser registradas neste documento antes ou junto da alteração no código.
- Detalhes internos de implementação permanecem preferencialmente no código-fonte.
- A interface gráfica deve permanecer desacoplada das regras de negócio.
- A interface poderá oferecer ações intuitivas, mas as validações pertencem ao domínio.
- A arquitetura continuará mantendo regras de negócio independentes da interface e da persistência, favorecendo futura evolução do MotorAuto para outras interfaces e integrações.
