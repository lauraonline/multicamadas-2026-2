# Matriz de rastreabilidade

Os IDs e critérios seguem [requisitos.md](requisitos.md): 13 RF, 7 RN, 7 RNF e 5 complementos. Esta consolidação preserva o catálogo da E2 e incorpora evidências da implementação atual, sem reutilizar os IDs para funcionalidades diferentes.

**Evidência** significa código ou teste inspecionado, não execução bem-sucedida nesta revisão. **Planejado** indica validação ainda necessária. A [arquitetura](arquitetura.md) distingue implementação e evolução. ADRs com quatro dígitos documentam escolhas atuais; a série `adr-001` a `adr-006` registra o projeto anterior.

## Requisitos funcionais

| ID | Requisito | Componente / decisão atual | Evidência e lacuna |
|---|---|---|---|
| RF01 | Manter pacientes | PacienteController, PacienteService, Cpf; ADR 0006 | CpfTest e roteiro etapa 2; validar fluxo completo de manutenção. |
| RF02 | Profissionais e especialidades | ProfissionalController, ProfissionalService; ADR 0006 | Modelo exige uma especialidade; roteiro etapa 6. Múltiplas especialidades da proposta E2 não estão implementadas. |
| RF03 | Definir disponibilidade | AgendaService.horariosLivres | Parcial: grade fixa; não existe configuração individual por profissional. Planejado: faixas, dias e bloqueio de alterações incompatíveis. |
| RF04 | Marcar consulta | AgendaService.agendar, Consulta.agendar; ADR 0002 | FluxoDaClinicaTest.agendaEDetectaConflito e ConsultaTest; concorrência pendente. |
| RF05 | Remarcar ou cancelar | Consulta.cancelar, AgendaService.remarcar | Cancelamento existe; remarcação lança MissaoPendenteException (E3-1). Planejado: falha no destino preserva origem. |
| RF06 | Impedir conflito | Consulta.conflitaCom, AgendaService | ConsultaTest e agendaEDetectaConflito verificam domínio/fluxo sequencial; corrida entre requisições não está protegida (E3-5). |
| RF07 | Registrar atendimento | ProntuarioService, Atendimento; ADR 0002 | AtendimentoTest; escrita exige responsável. Ver divergências RN03/RN05. |
| RF08 | Emitir prescrição | Prescricao, missão E3-2 | Esqueleto; PrescricaoTest está desativado. missoesRespondem501 confirma pendência, não conclusão. |
| RF09 | Solicitar exames | Evolução de Prontuário | Pendente: não há implementação de solicitação e histórico de status no código inspecionado. |
| RF10 | Histórico clínico | ProntuarioService.doPaciente; ADR 0004 | prontuarioRestritoAProfissionais; parcial, sem prescrições/exames e sem controle de vínculo clínico na leitura. |
| RF11 | Autenticação e perfis | AuthController, AutenticacaoService, SecurityConfig; ADR 0004/0005 | exigeAutenticacao, recusaSenhaErrada, prontuarioRestritoAProfissionais; portal do paciente pendente (E3-4). |
| RF12 | Auditar prontuário | AuditoriaService, ProntuarioService; ADR 0003 | leituraDeProntuarioEhAuditada; escrita síncrona em transação própria. Validar falhas e negativas. |
| RF13 | Relatórios gerenciais | Missão E3-3 | Pendente; PainelService resume o dia, mas não substitui relatórios por período/profissional/especialidade. |
| RF-E01 | Agendamento por WhatsApp | Proposta E2; sem adaptador atual | Planejado: assinatura, vínculo de identidade, deduplicação, confirmação pós-commit e isolamento de falhas. |

## Regras de negócio

| ID | Regra | Evidência atual / decisão | Verificação necessária ou divergência |
|---|---|---|---|
| RN01 | CPF único entre ativos | Paciente.cpf tem unique=true; Cpf/PacienteService; ADR 0006 | Restrição é mais forte: inclui inativos. Planejado: corrida de cadastros e normalização. |
| RN02 | Sem duas AGENDADAS no mesmo horário | Consulta.conflitaCom e AgendaService | Considera todos os estados não cancelados; falta garantia concorrente. Planejado: duas conexões com barreira no PostgreSQL. |
| RN03 | Atender somente consulta de hoje ou anterior | ProntuarioService.iniciar e Consulta.iniciarAtendimento | Não há validação da data; confirmar chegada não a substitui. Planejado: hoje/passado/futuro com relógio controlado. |
| RN04 | Prescrição/exame vinculados a atendimento | Prescricao possui atendimentoId, mas é esqueleto | Pendente: regras e persistência que impeçam registros órfãos. |
| RN05 | Prontuário somente por anexação | Atendimento.finalizar; AtendimentoTest.finalizadoEhImutavel | Parcial: aberto permite sobrescrita, não há complementos nem proteção SQL de somente anexação demonstrada. |
| RN06 | Paciente vê próprios dados; recepção sem conteúdo clínico | SecurityConfig; ADR 0004 | Rota do prontuário bloqueia recepção; portal pendente. Revisar também alertas clínicos expostos no cadastro/agenda. |
| RN07 | Cancelar apenas AGENDADA | Consulta.cancelar; ConsultaTest.regrasDeCancelamento | Diverge: aceita CONFIRMADA. O teste do comportamento atual não comprova aderência ao requisito. |
| RN-E01 | Nome da mãe como informação auxiliar | Proposta não implementada | Validar com a clínica; nunca usar isoladamente como autenticação. |
| RN-E02 | Não agendar no passado | Consulta.agendar; Clock em AgendaService | ConsultaTest; planejar fronteiras de dia e zona da clínica (hoje usa zona padrão do servidor). |

## Requisitos não funcionais

| ID | Meta do catálogo | Componente / decisão | Evidência e verificação pendente |
|---|---|---|---|
| RNF01 | Negar e auditar 100% dos acessos sem permissão | SecurityConfig, AuditoriaService; ADR 0004/0003 | Teste de bloqueio de administrador existe; auditoria de todas as negativas não está implementada. CQ01: ampliar perfis e IDs manipulados. |
| RNF02 | Trilha disponível em até 1 minuto | AuditoriaService com REQUIRES_NEW; ADR 0003 | leituraDeProntuarioEhAuditada; CQ02: medir prazo e falhas, sem presumir garantia sob carga. |
| RNF03 | Busca de paciente P95 <2 s | PacienteService e persistência; ADR 0006 | Sem ensaio de carga nesta revisão. CQ03: definir carga e registrar percentis; Raio-X auxilia, mas não comprova a meta. |
| RNF04 | Agenda >=99% nas 12 h/dia do mês | Processo único; H2 padrão ou perfil PostgreSQL | CQ04: monitoramento prolongado; persistência em PostgreSQL não garante disponibilidade. |
| RNF05 | Extensão em até 5 dias/equipe sem alterar núcleos | APIs modulares; ADR 0001/0002 | ArquiteturaTest verifica limites e ciclos; CQ05 deve medir esforço real de extensão. |
| RNF06 | Agendar em <=1 min e <=5 cliques | Interface estática e Agenda | Roteiro etapa 3; CQ06: ensaio com usuários e contagem desde a tela inicial. |
| RNF07 | Senhas com hash e sal | BCryptPasswordEncoder em SecurityConfig; ADR 0005 | Evidência de configuração; CQ07: revisar persistência e ausência de senhas nos logs. |
| RNF-E01 | Busca paciente/profissional <=3 s | Cadastro e persistência | CQ08: medir as duas buscas; manter também P95 <2 s para pacientes. |
| RNF-E02 | Recuperação <=30 min | Operação; perfil PostgreSQL | CQ09: ensaio de backup/restore; H2 padrão perde dados no reinício. Não comprovado. |

## Leitura inversa e plano de validação

| Módulo / elemento atual | Requisitos relacionados |
|---|---|
| cadastro | RF01/RF02; RN01; RNF03/RNF-E01 |
| agenda | RF03-RF06; RN02/RN07/RN-E02; RNF04/RNF06 |
| prontuario | RF07-RF10; RN03-RN06; RNF01/RNF02 (inclui pendências) |
| seguranca | RF11; RN06; RNF01/RNF07 |
| auditoria | RF12; RNF01/RNF02 |
| painel | Resumo diário adicional; não satisfaz sozinho RF13 |
| APIs dos módulos / ArchUnit | RNF05 |
| Persistência e operação | Integridade, RNF04/RNF-E02 |

Chegada, ciclo de atendimento, resumo diário e consulta administrativa de auditoria são capacidades atuais complementares, sem renumerar RF01-RF13. Portal é parte da evolução de RF11/RN06; relatórios e prescrições mantêm RF13 e RF08.

Preservam-se da E2 os ensaios de concorrência, falha de remarcação, integridade clínica, totalizadores com base conhecida, segurança do bot e recuperação. Os protocolos CQ01-CQ09 estão nos [cenários](cenarios-qualidade.md); referências a Redis/outbox nesses materiais são alvos de evolução, não evidências atuais. Registrar ambiente, revisão do código, data, dados sintéticos e resultados. Não usar pacientes reais nos ensaios.
