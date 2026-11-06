# Referências, precedência e limites

Foram lidos os oito materiais de fontes/ (arquivos Zone.Identifier são metadados e não referências). A pasta permanece ignorada conforme alteração preexistente; a entrega final não depende dela para navegação ou geração do PDF.

| Código | Material local | Uso |
|---|---|---|
| G | Estudo_de_Caso_NOITE_SaudeCerta_DETALHADO_2.pdf, 6 páginas | RF/RN/RNF oficiais (pp. 2-3), modelo/camadas (p. 4), ADRs/matriz (p. 5), rubrica E2 (p. 6) |
| E1 | SaudeCerta_E1_Visao_e_Requisitos_Core4Tech.pdf, 10 páginas | Escopo e numeração consolidada; original copiado sem alterações para docs/ |
| A2 | Atividade_Aula2_SaudeCerta_NOITE.docx | Stakeholders, metas de 3 s/30 min, servidor secundário |
| A3 | Atividade_Aula3_SaudeCerta_NOITE.docx | Contêineres iniciais, WhatsApp e decisão Redis ADR-001 |
| S2 | SaudeCerta_Apresentacao.pptx | Visões 4+1 e prioridades da equipe |
| S3 | SaudeCerta_C4_ADR.pptx | C4 preliminar e justificativa Redis |
| R-Git | Um_Repositorio_por_Equipe.pptx.pdf, 11 páginas | Estrutura docs/visao.md, requisitos.md, arquitetura.drawio, adr/ e rastreabilidade.md (p. 5); branch/PR/tag (pp. 6-7) |
| R | README.md existente no início desta tarefa | Síntese E1 já revisada pela equipe; preservada e acrescida de links |

O guia e a E1 prevalecem na numeração oficial. A organização mais detalhada R-Git coloca ADRs em docs/adr/, em vez do caminho simplificado docs/adr-001.md da Aula 3. O ADR-001 de Redis é preservado; o exemplo de monólito do guia torna-se ADR-002, e auditoria é ADR-005. Referências do guia a ADR-002 no PF devem ser interpretadas como a decisão de auditoria, não como obrigação de renumerar a história da equipe.

A E2 refina o contexto para abranger todo o sistema, acrescenta o administrador omitido no slide preliminar e mantém WhatsApp fora da fronteira. Redis é obrigatório apenas para a extensão conversacional; agenda web não depende dele. Parâmetros novos (slots, TTL, RPO, ambiente de carga, sessão e frontend) são propostas explícitas, não requisitos atribuídos ao professor.

## Encaminhamento da entrega

Artefatos preparados na branch e2-docs. Após revisão da equipe: commits identificáveis, push da branch, PR revisado por colega, merge e tag/Release E2; então registrar link do mesmo repositório no AVA. Preparar arquivos não comprova publicação nem submissão. Não criar outro repositório ou substituir entregas anteriores.
