# 🚗 Modelo do Domínio

Este documento descreve as principais entidades do sistema **MotorAuto**, seus atributos, relacionamentos, regras de negócio e decisões já validadas.

> **Importante:** este é um documento vivo. Ele deverá ser atualizado sempre que uma regra de negócio for criada, alterada ou removida durante o desenvolvimento.

---

## Convenções

- **Obrigatório:** o valor deve ser informado para que a entidade seja válida.
- **Opcional:** o valor pode ser omitido.
- **Gerado automaticamente:** o valor será definido pelo sistema ou pela camada de persistência.
- ✅ **Implementada e testada:** entidade já existente no código e coberta por testes automatizados.
- 🟡 **Modelagem validada:** regras definidas, mas implementação ainda não iniciada ou concluída.
- ⏳ **Em definição:** entidade ainda não possui modelagem completa.

---

# Visão geral das entidades

| Entidade | Situação |
|---|---|
| Cliente | ✅ Implementada e testada |
| Veículo | ✅ Implementada e testada |
| Profissional | 🟡 Modelagem validada |
| Ordem de Serviço | ⏳ Em definição |
| Serviço | ⏳ Em definição |
| Peça | ⏳ Em definição |
| Forma de Pagamento | ⏳ Em definição |

---

# Relacionamentos

```text
Cliente (1)
        │
        └──────── possui ─────────────► Veículo (N)

Cliente (1)
        │
        └──────── solicita ───────────► Ordem de Serviço (N)

Veículo (1)
        │
        └──────── recebe ─────────────► Ordem de Serviço (N)

Profissional (1)
        │
        └──────── é responsável por ──► Ordem de Serviço (N)

Ordem de Serviço (1)
        │
        ├──────── contém ─────────────► Serviço (N)
        │
        ├──────── utiliza ────────────► Peça (N)
        │
        └──────── possui ─────────────► Forma de Pagamento
```

> Os relacionamentos acima representam a visão inicial do domínio e poderão ser refinados durante a modelagem da Ordem de Serviço.

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

### Validação

**RN-CLI-001** — Todo cliente deve possuir nome.

**RN-CLI-002** — Todo cliente deve possuir telefone.

**RN-CLI-003** — Nome e telefone devem ser normalizados antes de serem armazenados, removendo espaços excedentes nas extremidades.

**RN-CLI-004** — CPF, endereço e observações são opcionais.

**RN-CLI-005** — Campos textuais opcionais contendo apenas espaços devem ser convertidos para `None`.

### Estado

**RN-CLI-006** — Todo cliente inicia ativo.

**RN-CLI-007** — Clientes não devem ser excluídos fisicamente quando possuírem histórico.

**RN-CLI-008** — O cadastro poderá ser ativado ou desativado, preservando seu histórico.

### Cadastro

**RN-CLI-009** — A data de cadastro será preenchida automaticamente pelo sistema.

**RN-CLI-010** — O identificador será gerado pela camada de persistência.

### Encapsulamento

**RN-CLI-011** — Nome e telefone somente poderão ser alterados pelos métodos públicos da entidade.

**RN-CLI-012** — As alterações cadastrais deverão respeitar as mesmas validações aplicadas no momento da criação.

**RN-CLI-013** — Uma tentativa de alteração inválida não poderá modificar o estado anterior da entidade.

## Interface pública

### Consultas

- `nome`
- `telefone`
- `cpf`
- `endereco`
- `observacoes`
- `possui_whatsapp`
- `ativo`
- `data_cadastro`

### Comportamentos

- `atualizar_nome()`
- `atualizar_telefone()`
- `atualizar_cpf()`
- `atualizar_endereco()`
- `atualizar_observacoes()`
- `ativar_whatsapp()`
- `desativar_whatsapp()`
- `ativar()`
- `desativar()`

---

# Veículo

Representa um veículo pertencente a um cliente e que poderá possuir um histórico de Ordens de Serviço.

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

### Validação

**RN-VEI-001** — Todo veículo deve estar associado a um cliente válido.

**RN-VEI-002** — Todo veículo deve possuir marca.

**RN-VEI-003** — Todo veículo deve possuir modelo.

**RN-VEI-004** — Marca e modelo devem ser normalizados antes de serem armazenados.

**RN-VEI-005** — Ano é opcional.

**RN-VEI-006** — Quando informado, o ano deve ser um número inteiro entre `1886` e `2100`.

**RN-VEI-007** — Placa é opcional.

**RN-VEI-008** — Quando informada, a placa deve ser normalizada para letras maiúsculas, sem espaços e sem hífen.

**RN-VEI-009** — A unicidade da placa será garantida posteriormente pela camada de persistência.

**RN-VEI-010** — Combustível e observações são opcionais.

**RN-VEI-011** — Campos textuais opcionais contendo apenas espaços devem ser convertidos para `None`.

### Histórico

**RN-VEI-012** — A quilometragem não será armazenada no cadastro do veículo.

**RN-VEI-013** — A quilometragem será registrada em cada Ordem de Serviço.

**RN-VEI-014** — O histórico de quilometragem será obtido pelas Ordens de Serviço do veículo.

**RN-VEI-015** — A transferência de propriedade não deverá apagar o histórico do veículo.

### Correções cadastrais

**RN-VEI-016** — Marca, modelo e ano representam características estáveis do veículo.

**RN-VEI-017** — Alterações em marca, modelo ou ano serão tratadas como correções cadastrais.

**RN-VEI-018** — Uma tentativa de correção inválida não poderá alterar o estado anterior da entidade.

### Encapsulamento

**RN-VEI-019** — Atributos que possuem regras de negócio ou métodos de alteração deverão permanecer protegidos.

**RN-VEI-020** — Alterações deverão ocorrer somente pelos métodos públicos da entidade.

## Interface pública

### Consultas

- `cliente`
- `marca`
- `modelo`
- `ano`
- `placa`
- `combustivel`
- `observacoes`

### Comportamentos

- `corrigir_marca()`
- `corrigir_modelo()`
- `corrigir_ano()`
- `atualizar_placa()`
- `atualizar_combustivel()`
- `atualizar_observacoes()`
- `transferir_propriedade()`

---

# Profissional

Representa um colaborador da oficina responsável pelo atendimento, execução de serviços, auxílio operacional ou gerenciamento das atividades.

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

## Funções permitidas

- Mecânico
- Atendente
- Gerente
- Auxiliar

## Regras de negócio

### Validação

**RN-PRO-001** — Todo profissional deve possuir nome.

**RN-PRO-002** — Todo profissional deve possuir telefone.

**RN-PRO-003** — Todo profissional deve possuir uma função válida.

**RN-PRO-004** — As únicas funções permitidas são Mecânico, Atendente, Gerente e Auxiliar.

**RN-PRO-005** — A função será representada por um `Enum`, evitando valores inválidos e diferenças de escrita.

**RN-PRO-006** — Nome e telefone devem ser normalizados antes de serem armazenados.

**RN-PRO-007** — Observações são opcionais.

**RN-PRO-008** — Observações contendo apenas espaços devem ser convertidas para `None`.

### Estado

**RN-PRO-009** — Todo profissional inicia ativo.

**RN-PRO-010** — Profissionais não deverão ser excluídos fisicamente quando estiverem associados ao histórico da oficina.

**RN-PRO-011** — Quando necessário, o profissional deverá ser desativado, preservando suas associações anteriores.

### Cadastro

**RN-PRO-012** — A data de cadastro será preenchida automaticamente pelo sistema.

**RN-PRO-013** — O identificador será gerado pela camada de persistência.

### Encapsulamento

**RN-PRO-014** — Os atributos que possuem regras de negócio ou métodos de alteração deverão permanecer protegidos.

**RN-PRO-015** — As alterações cadastrais deverão ocorrer somente pelos métodos públicos da entidade.

**RN-PRO-016** — Uma tentativa de alteração inválida não poderá modificar o estado anterior da entidade.

## Interface pública prevista

### Consultas

- `nome`
- `telefone`
- `funcao`
- `observacoes`
- `ativo`
- `data_cadastro`

### Comportamentos

- `atualizar_nome()`
- `atualizar_telefone()`
- `alterar_funcao()`
- `atualizar_observacoes()`
- `ativar()`
- `desativar()`

---

# Ordem de Serviço

Representa um atendimento realizado pela oficina.

## Atributos preliminares

- `id`
- `cliente`
- `veiculo`
- `profissional_responsavel`
- `data_entrada`
- `data_prevista_saida`
- `data_saida`
- `quilometragem`
- `defeito_relatado`
- `diagnostico`
- `observacoes`
- `valor_total`
- `forma_pagamento`
- `situacao_pagamento`
- `status`

## Regras de negócio

> Em definição.

---

# Serviço

Representa um serviço executado em uma Ordem de Serviço.

## Atributos preliminares

- `id`
- `descricao`
- `valor_mao_obra`

## Regras de negócio

> Em definição.

---

# Peça

Representa uma peça utilizada em uma Ordem de Serviço.

## Atributos preliminares

- `id`
- `descricao`
- `quantidade`
- `valor_unitario`

## Regras de negócio

> Em definição.

---

# Forma de Pagamento

Representa a forma utilizada para quitar uma Ordem de Serviço.

## Atributos preliminares

- `id`
- `descricao`

## Regras de negócio

> Em definição.

---

# Decisões técnicas e de domínio

## DT-001 — Telefone do cliente

O telefone é obrigatório para o cadastro de clientes.

## DT-002 — Quilometragem

A quilometragem pertence à Ordem de Serviço, não ao cadastro do veículo.

## DT-003 — Ano do veículo

Será utilizado apenas um campo `ano`, priorizando agilidade no cadastro.

## DT-004 — Validação no domínio

As regras de negócio devem ser protegidas pelas entidades, independentemente da interface ou da origem dos dados.

## DT-005 — Encapsulamento

Atributos que possuem regras de negócio ou métodos de alteração deverão ser protegidos e modificados somente pela interface pública da entidade.

## DT-006 — Correções cadastrais do veículo

Marca, modelo e ano poderão ser corrigidos pelos métodos próprios da entidade.

## DT-007 — Limites de ano

O ano do veículo, quando informado, deverá estar entre `1886` e `2100`.

## DT-008 — Normalização de placa

A placa será armazenada em letras maiúsculas, sem espaços e sem hífen.

## DT-009 — Função do profissional

A função do profissional será representada por um `Enum`.

## DT-010 — Funções permitidas

As funções permitidas são Mecânico, Atendente, Gerente e Auxiliar.

## DT-011 — Exclusão lógica

Clientes e profissionais deverão ser desativados em vez de excluídos quando possuírem histórico associado.

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

- ✅ Atributos definidos.
- ✅ Regras de negócio validadas.
- ✅ Interface pública prevista.
- ⏳ Estudo e definição do `Enum`.
- ⏳ Implementação.
- ⏳ Testes automatizados.

---

# Próxima etapa

Estudar o conceito de `Enum` e utilizá-lo para representar as funções permitidas da entidade `Profissional`.

---

# Observações

Este documento deverá ser revisado antes da implementação de cada entidade.

Mudanças nas regras de negócio devem ser registradas aqui antes ou junto da alteração correspondente no código.

Detalhes internos de implementação, como nomes de métodos privados, permanecerão documentados no código-fonte e não farão parte obrigatória deste modelo de domínio.
