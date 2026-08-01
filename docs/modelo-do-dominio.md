# 🚗 Modelo do Domínio

Este documento descreve as principais entidades do sistema **MotorAuto**, seus atributos, relacionamentos e regras de negócio.

> **Importante:** este documento é um artefato vivo do projeto e poderá sofrer alterações durante o desenvolvimento, conforme novas necessidades forem identificadas.

## Convenções

- *(obrigatório)* → Campo obrigatório.
- *(gerado automaticamente)* → Campo preenchido pelo sistema.
- ⏳ → Entidade ainda em modelagem.
- ✅ → Entidade validada.

---

# Entidades

- Cliente ✅
- Veículo ✅
- Profissional ⏳
- Ordem de Serviço ⏳
- Serviço ⏳
- Peça ⏳
- Forma de Pagamento ⏳

---

# Relacionamentos

```text
Cliente (1)
        │
        └──────── possui ───────► Veículo (N)

Cliente (1)
        │
        └──────── solicita ─────► Ordem de Serviço (N)

Veículo (1)
        │
        └──────── possui ───────► Ordem de Serviço (N)

Ordem de Serviço (1)
        │
        ├──────── contém ───────► Serviço (N)
        │
        ├──────── utiliza ──────► Peça (N)
        │
        └──────── executada por ► Profissional (1)
```

---

# Cliente

Representa uma pessoa física ou empresa atendida pela oficina.

## Atributos

- id *(gerado automaticamente)*
- nome *(obrigatório)*
- telefone *(obrigatório)*
- possui_whatsapp
- cpf
- endereco
- data_cadastro *(gerado automaticamente)*
- observacoes
- ativo

## Regras de Negócio

- Todo cliente deve possuir nome.
- Todo cliente deve possuir telefone.
- O identificador é gerado automaticamente.
- A data de cadastro é preenchida automaticamente pelo sistema.
- Clientes não serão excluídos fisicamente do sistema.
- Clientes poderão ser desativados.

---

# Veículo

Representa um veículo pertencente a um cliente e que poderá possuir um histórico de Ordens de Serviço.

## Atributos

- id *(gerado automaticamente)*
- marca *(obrigatório)*
- modelo *(obrigatório)*
- ano
- placa
- combustivel
- observacoes

## Regras de Negócio

- Todo veículo deve possuir marca.
- Todo veículo deve possuir modelo.
- Todo veículo pertence a um único cliente.
- A placa, quando informada, deverá ser única.
- A quilometragem não será armazenada no cadastro do veículo.
- A quilometragem será registrada em cada Ordem de Serviço.

---

# Profissional

Representa o funcionário responsável pela execução dos serviços.

## Atributos (preliminares)

- id
- nome
- telefone
- funcao
- ativo

## Regras de Negócio

> Em definição.

---

# Ordem de Serviço

Representa um atendimento realizado pela oficina.

## Atributos (preliminares)

- id
- cliente
- veículo
- profissional_responsavel
- data_entrada
- data_saida
- quilometragem
- defeito_relatado
- observacoes
- valor_total
- forma_pagamento
- status

## Regras de Negócio

> Em definição.

---

# Serviço

Representa um serviço executado durante uma Ordem de Serviço.

## Atributos (preliminares)

- id
- descricao
- valor_mao_obra

## Regras de Negócio

> Em definição.

---

# Peça

Representa uma peça utilizada durante um serviço.

## Atributos (preliminares)

- id
- descricao
- quantidade
- valor_unitario

## Regras de Negócio

> Em definição.

---

# Forma de Pagamento

Representa a forma utilizada para quitar uma Ordem de Serviço.

## Atributos (preliminares)

- id
- descricao

## Regras de Negócio

> Em definição.

---

# Decisões de Projeto

## Cliente

- Nome é obrigatório.
- Telefone é obrigatório.
- CPF é opcional.
- Endereço é opcional.
- O cadastro utiliza exclusão lógica através do atributo `ativo`.

---

## Veículo

- Marca é obrigatória.
- Modelo é obrigatório.
- Será utilizado apenas um campo **Ano**.
- A quilometragem não pertence ao cadastro do veículo.
- O histórico de quilometragem será obtido através das Ordens de Serviço.

---

# Observações

Este documento será atualizado durante todo o desenvolvimento do MotorAuto.

Sempre que uma nova regra de negócio for descoberta ou uma decisão importante for tomada, ela deverá ser registrada aqui antes da implementação no código.
# Histórico de Decisões

## DT-001
Telefone obrigatório para cadastro de cliente.

## DT-002
A quilometragem pertence à Ordem de Serviço.

## DT-003
Utilizar apenas um campo "Ano" no cadastro do veículo.