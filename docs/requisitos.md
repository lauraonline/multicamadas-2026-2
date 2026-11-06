# E1 - Catálogo de requisitos

Base: [E1 original](SaudeCerta_E1_Visao_e_Requisitos_Core4Tech.pdf), pp. 4-8, e guia oficial, pp. 2-3. IDs oficiais preservados; extensões da equipe usam `-E`.

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
