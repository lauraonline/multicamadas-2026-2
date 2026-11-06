# E1 - Visão do produto

Síntese do README existente e da E1 original, preservada integralmente no [PDF da E1](SaudeCerta_E1_Visao_e_Requisitos_Core4Tech.pdf).

## 1. Visão geral

O **SaúdeCerta** é um sistema web multicamadas para uma clínica de médio porte, com aproximadamente vinte profissionais de diferentes especialidades. Sua proposta é centralizar cadastros, disponibilidade dos profissionais, agendamentos, atendimentos e prontuários eletrônicos, preservando a privacidade dos dados de saúde e a rastreabilidade das operações.

Atualmente, a clínica utiliza planilhas compartilhadas para agendamentos e mantém prontuários em papel. Esse funcionamento provoca:

- **Conflitos de agenda:** consultas marcadas simultaneamente para o mesmo profissional.
- **Retrabalho e demora:** dificuldade de localizar históricos, remarcar ou cancelar consultas.
- **Riscos à privacidade:** ausência de controles consistentes e de registros de acesso ao conteúdo clínico.

A solução busca oferecer um fluxo seguro e ágil, da marcação ao registro da consulta. Como **extensão proposta pela equipe**, o paciente poderá solicitar e confirmar agendamentos por um chatbot integrado ao WhatsApp, respeitando as mesmas regras de negócio da aplicação web.

### 1.1 Objetivos

1. Evitar agendamentos conflitantes, inclusive quando houver solicitações simultâneas.
2. Informatizar o prontuário e restringir os dados clínicos aos perfis autorizados.
3. Registrar e disponibilizar trilhas de auditoria dos acessos ao prontuário.
4. Simplificar agendamentos, remarcações e cancelamentos para recepção e pacientes.
5. Permitir evolução por módulos sem reescrever o núcleo do sistema.

### 1.2 Escopo

**Incluído no produto:**

- Cadastros de pacientes, profissionais e especialidades.
- Agenda de disponibilidade, marcação, remarcação e cancelamento de consultas.
- Registro de atendimentos e prontuário eletrônico.
- Prescrições e solicitações de exames vinculadas a atendimentos.
- Autenticação, autorização por perfil e auditoria de prontuários.
- Relatórios gerenciais básicos.
- **Extensão da equipe:** agendamento e confirmação por WhatsApp.

**Fora do escopo inicial:** faturamento e integração com convênios, integração com laboratórios externos para laudos, telemedicina e assinatura digital com certificado ICP-Brasil. Esses itens são possibilidades de evolução futura, não entregas assumidas nesta etapa.

## 2. Stakeholders e atores

### 2.1 Stakeholders

| Interessado | Interesse principal |
|---|---|
| Pacientes | Consultar dados próprios e solicitar, acompanhar, remarcar ou cancelar consultas. |
| Recepcionistas | Operar cadastros e agendas rapidamente, sem conflito de horários. |
| Profissionais de saúde | Consultar agenda e histórico autorizado, registrar atendimento, prescrever e solicitar exames. |
| Gerência/direção | Melhorar a operação, acompanhar relatórios e assegurar proteção dos dados. |

### 2.2 Atores e sistemas externos

| Ator ou integração | Papel no SaúdeCerta |
|---|---|
| Paciente | Interage com a aplicação e, na extensão da equipe, com o chatbot de agendamento. |
| Recepcionista | Cadastra pacientes e administra agendamentos; não visualiza conteúdo clínico. |
| Profissional de saúde | Consulta a própria agenda, acessa prontuários autorizados e registra atendimentos. |
| Administrador | Administra usuários, especialidades, relatórios e auditoria conforme permissões. |
| WhatsApp Business API (externo) | Transporta mensagens e webhooks do fluxo de agendamento. |

**Distinção arquitetural:** PostgreSQL e Redis são componentes de infraestrutura, não atores humanos. O chatbot é um canal/adaptador do sistema; não substitui as regras de autorização, integridade ou agendamento.
