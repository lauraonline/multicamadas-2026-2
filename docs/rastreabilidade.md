# Matriz de rastreabilidade requisitos ↔ arquitetura

Cobertura: 13 RF oficiais, 7 RN, 7 RNF e 5 complementos da equipe (32 linhas). IDs e critérios seguem [requisitos](requisitos.md). Componentes M e contêineres C são os identificadores dos C4 e da [arquitetura](arquitetura.md). V identifica verificação planejada; CQ identifica [cenário de qualidade](cenarios-qualidade.md). Nenhum V representa teste executado nesta E2.

| Requisito | Componente / tática | Decisão | Verificação planejada |
|---|---|---|---|
| RF01 | M-CAD / C-PG | [ADR-003](adr/adr-003.md) | V-CAD: cadastro válido, busca e CPF duplicado ativo recusado. |
| RF02 | M-CAD / C-PG | [ADR-002](adr/adr-002.md); [ADR-003](adr/adr-003.md) | V-CAD: impedir profissional sem especialidade; permitir múltiplas. |
| RF03 | M-AGE | [ADR-003](adr/adr-003.md) | V-AGENDA: gerar slots só na faixa; impedir alteração que invalide consulta. |
| RF04 | M-AGE / C-PG | [ADR-003](adr/adr-003.md) | V-AGENDA: 201 após commit; slot livre vira AGENDADA. |
| RF05 | M-AGE / C-PG | [ADR-003](adr/adr-003.md) | V-AGENDA: remarcação/cancelamento libera origem; falha mantém origem. |
| RF06 | M-AGE / C-PG | [ADR-003](adr/adr-003.md) | V-AGENDA: disputa concorrente tem uma confirmação e um conflito. |
| RF07 | M-PRO / M-AGE | [ADR-003](adr/adr-003.md); [ADR-005](adr/adr-005.md) | V-DOM: atendimento com queixa/evolução/conduta; consulta REALIZADA atomicamente. |
| RF08 | M-PRE | [ADR-003](adr/adr-003.md) | V-DOM: prescrição exige atendimento e ao menos um item com dose/posologia. |
| RF09 | M-PRE | [ADR-003](adr/adr-003.md) | V-DOM: exame vinculado e histórico de status preservado. |
| RF10 | M-PRO / M-SEG | [ADR-004](adr/adr-004.md); [ADR-005](adr/adr-005.md) | V-DOM/V-SEG: histórico cronológico autorizado; auditoria anterior à liberação. |
| RF11 | M-SEG | [ADR-004](adr/adr-004.md) | V-SEG/V-CRED: autenticação, perfis e propriedade do recurso. |
| RF12 | M-AUD / C-PG | [ADR-005](adr/adr-005.md) | V-AUD: campos completos, sem perda e projeção idempotente. |
| RF13 | M-REL / M-AGE | [ADR-002](adr/adr-002.md); [ADR-004](adr/adr-004.md) | V-REL: totalizadores corretos por período/profissional/especialidade, sem texto clínico. |
| RF-E01 | M-ENT / M-AGE / M-INF / C-REDIS | [ADR-001](adr/adr-001.md); [ADR-003](adr/adr-003.md); [ADR-004](adr/adr-004.md); [ADR-005](adr/adr-005.md) | V-BOT: assinatura inválida recusada; webhook repetido cria uma consulta; confirmação pós-commit; falhas isoladas. |
| RN01 | M-CAD / C-PG | [ADR-003](adr/adr-003.md) | V-CAD: corrida de CPF ativo resulta em um cadastro; normalização preserva unicidade. |
| RN02 | M-AGE / C-PG | [ADR-003](adr/adr-003.md) | V-AGENDA: marcações simultâneas web/bot no mesmo slot. |
| RN03 | M-PRO | [ADR-003](adr/adr-003.md) | V-DOM: atender hoje/passado permitido; consulta futura rejeitada com relógio controlado. |
| RN04 | M-PRE / C-PG | [ADR-003](adr/adr-003.md) | V-DOM: impedir prescrição/exame órfão por regra e FK. |
| RN05 | M-PRO / M-PRE / C-PG | [ADR-003](adr/adr-003.md); [ADR-005](adr/adr-005.md) | V-DOM: sem exclusão/alteração clínica; complemento preserva original; permissão SQL restrita. |
| RN06 | M-SEG / M-PRO | [ADR-004](adr/adr-004.md) | V-SEG: paciente de outro ID e recepção bloqueados. |
| RN07 | M-AGE | [ADR-003](adr/adr-003.md) | V-AGENDA: cancelar REALIZADA/CANCELADA recusado; corrida cancelar/atender consistente. |
| RN-E01 | M-SEG / M-CAD | [ADR-004](adr/adr-004.md) | V-SEG: nome da mãe nunca concede sessão nem acesso; proposta auxiliar a validar. |
| RN-E02 | M-AGE | [ADR-003](adr/adr-003.md) | V-AGENDA: agendamento passado recusado; fronteira de dia na zona da clínica. |
| RNF01 | M-SEG / M-PRO / M-AUD | [ADR-004](adr/adr-004.md); [ADR-005](adr/adr-005.md) | CQ01 / V-SEG: 100% de negativas; auditoria de tentativas. |
| RNF02 | M-AUD / C-PG | [ADR-005](adr/adr-005.md) | CQ02 / V-AUD: trilha consultável em <=60 s. |
| RNF03 | M-CAD / C-PG | [ADR-003](adr/adr-003.md); [ADR-006](adr/adr-006.md) | CQ03 / V-PERF: busca de paciente P95 <2 s. |
| RNF04 | C-APP / C-PG / M-INF | [ADR-001](adr/adr-001.md); [ADR-006](adr/adr-006.md) | CQ04 / V-DISP: agenda >=99% durante 12 h/dia no mês. |
| RNF05 | Todos os módulos de C-APP | [ADR-002](adr/adr-002.md) | CQ05 / V-MOD: extensão em até 5 dias/equipe sem mudar núcleos. |
| RNF06 | C-WEB / M-AGE | [ADR-002](adr/adr-002.md); [ADR-004](adr/adr-004.md) | CQ06 / V-UX: <=1 min e <=5 cliques. |
| RNF07 | M-SEG / C-PG | [ADR-004](adr/adr-004.md) | CQ07 / V-CRED: hash com sal, sem senha em texto. |
| RNF-E01 | M-CAD / C-PG | [ADR-003](adr/adr-003.md); [ADR-006](adr/adr-006.md) | CQ08 / V-PERF: máximo <=3 s no ensaio, mantendo RNF03. |
| RNF-E02 | C-APP / C-PG / operação | [ADR-006](adr/adr-006.md) | CQ09 / V-REC: recuperação <=30 min. |

## Leitura inversa: arquitetura → requisitos

| Elemento | Requisitos atendidos |
|---|---|
| C-WEB / M-ENT | RF01-RF13 conforme perfil; RF-E01 pelo webhook; RNF06 |
| M-CAD | RF01/RF02; RN01; RNF03; RNF-E01 |
| M-AGE | RF03-RF06, RF13; RN02/RN07; RN-E02; RNF04/RNF06 |
| M-PRO | RF07/RF10; RN03/RN05/RN06; RNF01/RNF02 |
| M-PRE | RF08/RF09; RN04/RN05 |
| M-SEG | RF11; RN06/RN-E01; RNF01/RNF07 |
| M-AUD | RF12; RNF01/RNF02; suporte à preservação de RN05 |
| M-REL | RF13 |
| M-INF / C-PG | Persistência e integridade dos RF01-RF13; RN01-RN05/RN07; RNF02-RNF04/RNF07; RNF-E01/E02 |
| C-REDIS / WhatsApp | RF-E01; isolamento de falhas protege RNF04 |
| C-APP / fronteiras e operação | RNF05; RNF04/RNF-E02 |

## Evidências esperadas na E3/PF

V-CAD/V-DOM: testes de domínio e integração; V-AGENDA: PostgreSQL com duas conexões e barreira concorrente; V-REL: base sintética de totais conhecidos; V-BOT: provedor simulado, repetição, assinatura, vínculo e falhas. V-SEG/V-CRED/V-AUD/V-PERF/V-DISP/V-MOD/V-UX/V-REC usam os protocolos dos cenários. Armazenar ambiente, revisão de código, dados sintéticos, resultados e data; não usar pacientes reais nos ensaios.
