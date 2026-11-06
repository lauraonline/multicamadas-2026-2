# Cenários de qualidade e plano de verificação

As medidas oficiais vêm do guia, seção 8, e da E1. Ambiente e cargas abaixo são hipóteses de teste propostas na E2, não medições reais. Cada cenário contém fonte, estímulo, ambiente, artefato, resposta e medida. IDs V referenciam a matriz.

## CQ01 - Segurança e privacidade (RNF01 / RN06)

**Fonte:** recepcionista, paciente de outro cadastro ou usuário sem sessão. **Estímulo:** obter prontuário por URL ou API com ID adulterado. **Ambiente:** funcionamento normal e falha do gravador de auditoria. **Artefato:** M-SEG/M-PRO/M-AUD. **Resposta:** negar sem conteúdo clínico; persistir tentativa; na falha de persistência, manter bloqueio e alertar. **Medida:** 100% dos acessos indevidos negados e registrados quando o armazenamento estiver operacional; indisponibilidade que impeça registrar é incidente explícito, não sucesso do RNF.

**V-SEG:** matriz automatizada de quatro perfis, próprios/terceiros, leitura/escrita e URLs diretas; verificar corpo/headers/logs sem vazamento e evento durável da negativa. Validar também administrador sem privilégio clínico. ADR-004/005. Trade-off: checagem contextual custa processamento, mas preserva menor privilégio sem confirmações extras na marcação simples.

## CQ02 - Auditabilidade (RNF02 / RF12)

**Fonte:** profissional autorizado. **Estímulo:** abrir ou alterar prontuário. **Ambiente:** operação normal, reinício após commit e falha temporária do worker. **Artefato:** outbox PostgreSQL e M-AUD. **Resposta:** persistir evento antes da liberação; projetar trilha de modo idempotente. **Medida:** evento com usuário, paciente, data/hora e ação consultável pelo administrador em até 60 s desde a requisição; zero eventos de acessos liberados perdidos.

**V-AUD:** executar 1.000 acessos, interromper worker por 20 s, reiniciar e comparar IDs entre requisições e trilha; medir maior atraso, reprocessar lote e exigir uma entrada por eventoId. Polling proposto de 5 s, alerta aos 30 s e suspensão de novas leituras clínicas ao atingir 45 s de atraso, preservando tempo para drenagem. Falha maior pode violar a meta e deve contar como incidente. ADR-005. Escrita mínima durável permanece no caminho crítico, apesar da projeção assíncrona.

## CQ03 - Desempenho de busca (RNF03)

**Fonte:** recepcionistas. **Estímulo:** buscar pacientes pelo nome. **Ambiente proposto:** 100 mil pacientes sintéticos, 20 profissionais, 20 sessões concorrentes, 5 buscas/s por 15 min após 2 min de aquecimento; aplicação 2 vCPU/4 GiB, PostgreSQL 2 vCPU/4 GiB na mesma região; navegador e latência de rede registrados no relatório. **Artefato:** M-CAD/RepositorioCadastro, índice de nome normalizado e paginação de 20 resultados. **Resposta:** retornar resultados ordenados com projeção mínima. **Medida:** P95 menor que 2 s do envio no navegador à exibição, sob essa carga normal a validar.

**V-PERF:** registrar amostras, P50/P95/P99, erros, consultas SQL e plano de execução. Consultas por prefixo/nome precisam de índice compatível; substring exigirá estratégia específica e nova medição. Evitar N+1; busca não utiliza dados clínicos. ADR-003/006. O ensaio não substitui medição com volume real e não promete P95 em sobrecarga.

## CQ04 - Disponibilidade (RNF04)

**Fonte:** usuários da agenda e monitor externo. **Estímulo:** utilizar agenda durante as 12 h diárias de funcionamento. **Ambiente:** mês de operação; manutenção dentro da janela conta como indisponibilidade. **Artefato:** C-APP/C-PG, rede e recuperação. **Resposta:** listar e confirmar consultas válidas. **Medida:** disponibilidade mensal >= 99%; A = (minutos previstos - minutos indisponíveis) / minutos previstos. Para 30 dias com operação diária de 12 h: 21.600 min, orçamento de falha 216 min; ajustar aos dias efetivamente operados.

**V-DISP:** sondas a cada minuto e registros de incidentes delimitando início/fim; falha do bot isolado não torna agenda web indisponível, mas é registrada como falha de canal. Redis/provedor fora do ar não bloqueiam web. Separar falha de negócio esperada (409) de indisponibilidade. Ensaio de desligamento é evidência parcial; só observação mensal comprova RNF04. ADR-001/006.

## CQ05 - Modificabilidade (RNF05)

**Fonte:** equipe responsável pela evolução. **Estímulo:** adicionar módulo futuro de faturamento. **Ambiente:** contratos públicos de Agenda/Prontuário estabilizados. **Artefato:** módulos e portas de aplicação. **Resposta:** novo módulo usa eventos/consultas públicas sem modificar núcleo de agenda/prontuário. **Medida:** estimativa e ensaio de até 5 dias/equipe; hipótese de escopo mínimo: registrar cobrança a partir de AtendimentoRegistrado e listar cobranças, sem convênio, pagamento ou regras fiscais.

**V-MOD:** comparar diff dos núcleos, contratos, testes de dependência e registro de esforço da equipe; mudanças só em composição/configuração e no módulo novo. Não multiplicar automaticamente 5 dias por quatro integrantes; registrar como esforço coletivo conforme critério do guia. Se o escopo real exigir novos eventos ou mudar o núcleo, rever estimativa explicitamente. ADR-002.

## CQ06 - Usabilidade (RNF06)

**Fonte:** recepcionista autenticada. **Estímulo:** marcar consulta simples para paciente existente. **Ambiente:** tela inicial com busca e agenda integradas, horário livre, dados válidos. **Artefato:** C-WEB/M-AGE. **Resposta:** paciente selecionado, profissional/especialidade e slot escolhidos, confirmação visível. **Medida:** até 60 s e no máximo 5 cliques desde a tela inicial.

**V-UX:** observar cinco participantes representativos após orientação breve, três tarefas cada, registrar tempo e cliques por tarefa. Fluxo proposto: selecionar paciente (1), especialidade (2), profissional (3), slot (4), confirmar (5), com busca focada inicialmente e digitação incluída no tempo. Conflito de horário retorna opções preservando dados e é cenário alternativo medido à parte. Não incluir novo cadastro/login na marcação simples, mas avaliar esses fluxos separadamente. ADR-002/004.

## CQ07 - Credenciais (RNF07)

**Fonte:** revisor e testador. **Estímulo:** criar usuário e autenticar. **Ambiente:** banco de teste, falhas de login e logs habilitados. **Artefato:** M-SEG, encoder e repositório. **Resposta:** persistir hash com sal; comparar pela biblioteca; não devolver senha/hash na API. **Medida:** nenhuma senha em texto simples no banco/logs; duas contas com mesma senha têm hashes distintos e validáveis.

**V-CRED:** revisão de código e amostragem de banco, logs e DTOs; verificar biblioteca de hash, custo calibrado, expiração de sessão, CSRF e limite de tentativas. ADR-004. Hash mais custoso aumenta proteção e latência; calibrar sob carga antes de fixar parâmetro.

## CQ08 - Busca complementar (RNF-E01)

**Fonte:** recepção. **Estímulo:** buscar paciente ou profissional. **Ambiente:** mesmo ensaio CQ03. **Artefato:** M-CAD. **Resposta:** exibir resultados paginados. **Medida:** todas as buscas do ensaio em até 3 s; para pacientes também cumprir P95 < 2 s. **V-PERF:** registrar máximo por tipo de busca. A meta de 3 s não é relaxada para P95 nem substitui RNF03. ADR-003/006.

## CQ09 - Recuperabilidade (RNF-E02)

**Fonte:** falha da aplicação ou do banco. **Estímulo:** perda de instância/armazenamento primário. **Ambiente:** cópia de teste com backup e WAL em local independente e infraestrutura secundária pronta. **Artefato:** C-APP/C-PG e runbook. **Resposta:** restaurar e validar agenda, integridade e auditoria. **Medida:** RTO <= 30 min do início da falha ao serviço validado; RPO proposto <= 5 min, sujeito à aceitação.

**V-REC:** destruir apenas instância de ensaio, restaurar cópia, medir cronologia completa e comparar consultas/eventos com último WAL disponível. Falha durante gravação não pode produzir consulta parcial. Incluir tempo de detecção e intervenção. Resultado acima de 30 min exige revisar infraestrutura/plano; não presumir que backup diário atende RPO. ADR-006.
