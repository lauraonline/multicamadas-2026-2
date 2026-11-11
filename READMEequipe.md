# SaúdeCerta — Sistema de Gestão de Clínica

**Equipe:** Core4 Tech  
**Instituição:** Instituto Federal de Educação, Ciência e Tecnologia do Pará (IFPA) — Campus Belém  
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas  
**Disciplina:** Desenvolvimento de Aplicações Multicamadas (TEADS0347)  
**Turma:** C795NL · **Período:** 2026.2  
**Docente:** Márcio Goes do Nascimento  
**Repositório:** https://github.com/lauraonline/multicamadas-2026-2

## Equipe

- Laura Alves
- Gabriel Prado Brandão
- Adinayane Souza
- Ruan William Leão

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

## 3. Requisitos funcionais (RF)

A numeração **RF01–RF13** corresponde ao **guia oficial do estudo de caso**. Os complementos concebidos pela equipe usam o prefixo `RF-E` para não alterar essa rastreabilidade.

| ID | Requisito | Critério de aceitação resumido |
|---|---|---|
| **RF01** | Cadastrar e manter pacientes. | Nome, CPF e nascimento válidos são persistidos; o paciente aparece na busca. |
| **RF02** | Cadastrar profissionais e vinculá-los a especialidades. | Cada profissional possui pelo menos uma especialidade. |
| **RF03** | Definir disponibilidade dos profissionais. | Dias e faixas de horário definidos geram opções marcáveis. |
| **RF04** | Marcar consulta. | Paciente, profissional e horário livre produzem consulta `AGENDADA`. |
| **RF05** | Remarcar ou cancelar consulta. | Uma consulta `AGENDADA` pode ser alterada; o horário anterior é liberado. |
| **RF06** | Impedir conflito de horário. | Agendamento duplicado de um profissional no mesmo horário é recusado. |
| **RF07** | Registrar atendimento no prontuário. | Queixa, evolução e conduta são vinculadas à consulta e ao paciente. |
| **RF08** | Emitir prescrição. | Prescrição vinculada ao atendimento contém medicamento, dose e posologia. |
| **RF09** | Solicitar exames. | Solicitações são vinculadas ao atendimento e possuem acompanhamento de status. |
| **RF10** | Consultar histórico do paciente. | Profissional autorizado consulta atendimentos, prescrições e exames em ordem cronológica. |
| **RF11** | Autenticar usuários e aplicar perfis. | Recursos são disponibilizados conforme os papéis de recepção, profissional, administrador e paciente. |
| **RF12** | Registrar auditoria de acesso ao prontuário. | Todo acesso ou alteração registra usuário, paciente, data/hora e ação. |
| **RF13** | Gerar relatórios gerenciais. | Relatórios exibem totalizadores por período, profissional e especialidade. |

### 3.1 Requisito complementar da equipe

| ID | Proposta | Verificação planejada |
|---|---|---|
| **RF-E01** | Solicitar e confirmar agendamentos por chatbot no WhatsApp. | O webhook inicia a conversa; a aplicação valida disponibilidade e regras; a confirmação só ocorre após a persistência da consulta. |

O WhatsApp **não** terá acesso irrestrito a prontuários nem será usado para expor informações clínicas sensíveis sem uma decisão específica de segurança. O agendamento pelo chatbot compartilha o mesmo caso de uso da aplicação web.

## 4. Requisitos não funcionais (RNF)

Os códigos **RNF01–RNF07** e seus critérios seguem o guia. As metas adicionais da equipe aparecem separadamente com prefixo `RNF-E`.

| ID | Atributo | Cenário e medida verificável |
|---|---|---|
| **RNF01** | Segurança e privacidade | Perfil sem permissão tenta abrir prontuário: acesso negado e tentativa registrada em **100%** dos casos. |
| **RNF02** | Auditabilidade | Acesso ao prontuário registra usuário, paciente, data/hora e ação; registro disponível ao administrador em **até 1 minuto**. |
| **RNF03** | Desempenho | Busca por paciente, sob carga normal, retorna em **menos de 2 s no percentil 95**. |
| **RNF04** | Disponibilidade | Agenda disponível por **pelo menos 99% do tempo mensal** durante as **12 h/dia** de funcionamento. |
| **RNF05** | Modificabilidade | Inclusão futura de faturamento sem modificar o núcleo da agenda/prontuário, com esforço estimado de **até 5 dias/equipe**. |
| **RNF06** | Usabilidade | Marcação simples pela recepção em **até 1 minuto e no máximo 5 cliques** a partir da tela inicial. |
| **RNF07** | Segurança das credenciais | Senhas nunca armazenadas em texto simples; uso de **hash com sal** (por exemplo, BCrypt), confirmado em revisão de código. |

### 4.1 Metas complementares da equipe

| ID | Meta | Relação com o guia |
|---|---|---|
| **RNF-E01** | Busca por paciente **ou profissional** em até **3 segundos**. | O guia define, adicionalmente, a meta mais rigorosa para busca de paciente: menos de 2 s no P95 sob carga normal (RNF03). Os critérios de carga e percentis devem ser explicitados nos testes. |
| **RNF-E02** | Recuperação após indisponibilidade em **até 30 minutos**. | Meta de recuperabilidade que complementa, mas não substitui, a disponibilidade mensal exigida por RNF04. |

## 5. Regras de negócio (RN)

Os identificadores **RN01–RN07** mantêm o conteúdo do guia. Propostas da Core4 Tech são registradas como `RN-E`.

| ID | Regra |
|---|---|
| **RN01** | O CPF identifica unicamente o paciente: não podem existir dois cadastros ativos com o mesmo CPF. |
| **RN02** | Um profissional não pode ter duas consultas com status `AGENDADA` no mesmo horário. |
| **RN03** | Só é possível registrar atendimento de consultas cuja data seja **hoje ou anterior**. |
| **RN04** | Prescrições e solicitações de exame só existem vinculadas a um atendimento. |
| **RN05** | O prontuário é de **somente anexação**: registros não são apagados, apenas complementados. |
| **RN06** | Paciente visualiza somente os próprios dados; recepção não acessa conteúdo clínico do prontuário. |
| **RN07** | O cancelamento exige consulta com status `AGENDADA`. |

### 5.1 Regras complementares propostas pela equipe

| ID | Proposta | Situação |
|---|---|---|
| **RN-E01** | Utilizar o nome da mãe como informação auxiliar de confirmação de identidade no atendimento. | **A validar**: não substitui o CPF como identificador único nem constitui, isoladamente, autenticação segura. |
| **RN-E02** | Não permitir novos agendamentos em data/horário anteriores ao momento atual. | Complemento proposto: não deve ser confundido com RN03, que trata de **registro de atendimento**. |

> **Importante:** no README original, `RN01` se referia ao nome da mãe, `RN03` à proibição de agendar no passado e `RN04` ao cancelamento. Esses códigos conflitavam com o guia oficial. Nesta versão, o cancelamento é `RN07`; as propostas da equipe permanecem documentadas sem sobrescrever o guia.

## 6. Drivers arquiteturais

Drivers são requisitos cuja satisfação influencia diretamente a estrutura, os componentes, a persistência e a implantação da solução.

| Prioridade | Driver | Base | Implicação para a arquitetura |
|---|---|---|---|
| Muito alta | Segurança e privacidade | RNF01, RNF07, RN06, RF11 | RBAC, menor privilégio, credenciais protegidas e isolamento do conteúdo clínico. |
| Muito alta | Auditoria do prontuário | RNF02, RF12, RN05 | Trilhas de acesso rastreáveis, consultáveis e resistentes à perda. |
| Muito alta | Integridade da agenda | RF04–RF06, RN02, RN07 | Transações e proteção contra condições de corrida; cache não decide a ocupação definitiva. |
| Alta | Desempenho e usabilidade | RNF03, RNF06, RNF-E01 | Busca indexada, paginação e fluxos de agendamento objetivos. |
| Alta | Disponibilidade e recuperação | RNF04, RNF-E02 | Monitoramento, tratamento de falhas, backup e restauração. |
| Alta | Modificabilidade | RNF05 | Baixo acoplamento, módulos delimitados e contratos estáveis. |
| Complementar | Atendimento por mensagens | RF-E01, decisão sobre Redis | Adaptador de webhooks e armazenamento transitório de sessões, sem replicar as regras do domínio. |

**Trade-offs a aprofundar na E2:** segurança × facilidade de uso; auditoria × latência; simplicidade da implantação × resiliência; Redis × custo operacional de mais um componente.

## 7. Estilo arquitetural inicial

**Decisão:** **monólito modular multicamadas**, com princípios de **arquitetura hexagonal (Ports & Adapters)**.

A aplicação de negócio será implantada inicialmente como uma única unidade em Java/Spring Boot, estruturada internamente por módulos. PostgreSQL e Redis são serviços de dados de apoio; sua existência **não** transforma o núcleo em microsserviços. A integração com WhatsApp atua como adaptador externo.

### 7.1 Organização em camadas

| Camada | Responsabilidade | Exemplos indicativos |
|---|---|---|
| Apresentação/adaptadores de entrada | Endpoints web/REST, webhooks, validação de entrada, DTOs. | Spring Web, Bean Validation. |
| Aplicação | Coordenação de casos de uso e transações. | Serviços de aplicação, `@Transactional`. |
| Domínio | Entidades, regras RN01–RN07, invariantes e portas. | Entidades e interfaces independentes de infraestrutura. |
| Infraestrutura/adaptadores de saída | Repositórios, persistência, integração com WhatsApp e Redis. | Spring Data JPA, PostgreSQL, Redis. |
| Transversal | Autenticação, autorização, auditoria, tratamento de erros e observabilidade. | Spring Security, logs, monitoramento. |

### 7.2 Módulos de negócio

- **Cadastros:** pacientes, profissionais e especialidades.
- **Agenda:** disponibilidade e marcação, remarcação ou cancelamento de consultas.
- **Atendimento/Prontuário:** evolução clínica e histórico do paciente.
- **Prescrições/Exames:** artefatos vinculados a atendimentos.
- **Segurança/Auditoria:** autenticação, autorização e registro de acessos.
- **Relatórios:** indicadores gerenciais básicos.

O **chatbot/WhatsApp** é uma integração que invoca funcionalidades da Agenda, e não um domínio paralelo de agendamento.

### 7.3 Justificativa e limites

- **Versus microsserviços desde o início:** menor complexidade de rede, implantação, transações e observabilidade para a equipe e a clínica neste momento.
- **Versus monólito sem modularização:** fronteiras de responsabilidade favorecem manutenção, testes e uma possível extração de serviço no Projeto Final.
- **Ports & Adapters:** permite trocar infraestrutura e canais de entrada com menor impacto nas regras do domínio.
- **Riscos:** o monólito pode se acoplar excessivamente sem disciplina; uma instância central é um ponto de falha a tratar; a integração com Redis e WhatsApp introduz dependências externas.

## 8. Tecnologias e integrações previstas

| Componente | Tecnologia / abordagem | Estado da decisão |
|---|---|---|
| Aplicação de negócio e API | **Java + Spring Boot** | Referência do guia e atividades da equipe. |
| Persistência transacional | **PostgreSQL** | Selecionado nos artefatos C4 da equipe. |
| Sessões transitórias do chatbot e cache | **Redis**, com expiração de sessões (TTL) | Decisão explicitada pela equipe na Aula 3. |
| Canal de mensagens | **WhatsApp Business API (Meta)**, com webhooks | Integração complementar definida pela equipe. |
| Controle de acesso | Autenticação e perfis/RBAC; Spring Security é uma opção indicada pelo guia. | Definir detalhes na etapa de projeto. |
| Interface web | Tecnologia de frontend ainda não especificada nos materiais. | Em aberto. |

A escolha do Redis foi documentada pela equipe como **ADR-001 — Adoção do Redis para gerenciamento do estado das conversas do chatbot**. O ganho esperado é reduzir consultas e gravações de estado transitório no PostgreSQL; em contrapartida, surge um serviço adicional a configurar e monitorar.

> O guia apresenta um **ADR-001 sobre monólito modular como exemplo**, mas esse exemplo **não substitui nem renumera** o ADR-001 já produzido pela Core4 Tech sobre Redis. A documentação arquitetural completa e os demais ADRs pertencem à E2.

## 9. Entregas e evolução do projeto

| Etapa | Conteúdo principal | Situação documental |
|---|---|---|
| **E1 — Visão e Requisitos** | Problema, escopo, stakeholders, RF, RNF, RN, drivers e estilo inicial. | Documento PDF elaborado; esta versão do README sintetiza seu conteúdo. |
| **E2 — Projeto Arquitetural** | C4 (contexto, contêineres, componentes), modelo, cenários de qualidade, ADRs e rastreabilidade. | Projeto documentado em [docs/](docs/README.md), com C4, domínio, cenários, seis ADRs, matriz e PDF consolidado; implementação e validação nas etapas seguintes. |
| **E3 — Protótipo** | Spring Boot em camadas, API REST de cadastro/consulta/atendimento e testes das regras centrais. | Etapa posterior. |
| **Projeto Final** | Extração de pelo menos um serviço, componentes reutilizáveis e auditoria assíncrona funcional. | Etapa posterior. |

**Nota:** itens planejados nesta seção não significam funcionalidades implementadas. Não há, nos materiais fornecidos, comprovação de implementação ou testes executados.

## 10. Documentação e referências

A documentação está organizada em [docs/](docs/README.md), conforme o guia de organização do repositório.

- **E1:** [visão](docs/visao.md), [requisitos](docs/requisitos.md) e [PDF original](docs/SaudeCerta_E1_Visao_e_Requisitos_Core4Tech.pdf).
- **E2:** [PDF consolidado](docs/SaudeCerta_E2_Projeto_Arquitetural_Core4Tech.pdf), [arquitetura e C4](docs/arquitetura.md), [diagramas editáveis](docs/arquitetura.drawio), [domínio](docs/modelo-dominio.md), [cenários de qualidade](docs/cenarios-qualidade.md), [ADRs](docs/adr/README.md) e [rastreabilidade](docs/rastreabilidade.md).
- [Referências, organização e encaminhamento da entrega](docs/referencias.md).

As decisões da E2 descrevem a arquitetura alvo; não significam que o protótipo já implemente os requisitos. Instruções para regenerar e validar o PDF estão no [índice documental](docs/README.md).

Materiais utilizados na elaboração:

1. **[G]** IFPA — *Guia do Estudo de Caso SaúdeCerta (detalhado)*, turma C795NL, 2026.2; referência para o escopo e os identificadores oficiais.
2. **[A2]** Core4 Tech — *Atividade em Equipe, Aula 2: Fundamentos e Visões Arquiteturais*.
3. **[A3]** Core4 Tech — *Atividade em Equipe, Aula 3: Documentação da Arquitetura: C4 e ADR*.
4. **[C4]** Core4 Tech — *SaúdeCerta: Documentação da Arquitetura (C4 e ADR)*, apresentação da Aula 3.
5. **[R]** README anterior do projeto — base para a visão e para propostas complementares da equipe.

### Pontos detalhados na E2 e validação futura

- Como confirmar a identidade de pacientes no canal WhatsApp sem considerar o nome da mãe como credencial suficiente.
- Validar por teste concorrente a estratégia transacional detalhada no [ADR-003](docs/adr/adr-003.md).
- Medir atraso e testar falhas da auditoria durável proposta no [ADR-005](docs/adr/adr-005.md).
- Validar frontend, autenticação e recuperação propostos na [E2](docs/arquitetura.md) e seus [cenários mensuráveis](docs/cenarios-qualidade.md).
- Limites de exposição de dados pessoais e clínicos em serviços externos de mensageria.

---

*SaúdeCerta • Core4 Tech • IFPA Campus Belém • 2026.2*