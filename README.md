# SaúdeCerta

Sistema de gestão de clínica usado como estudo de caso da disciplina **Desenvolvimento de Aplicações Multicamadas** (IFPA, 2026.2, turma da noite).

É uma aplicação completa e pequena: API REST em Java/Spring Boot, banco relacional e interface web. Ela funciona, mas está **incompleta de propósito**: quatro funcionalidades respondem "missão pendente" e esperam pela sua equipe.

> Todas as pessoas, CPFs e registros clínicos dos dados de demonstração são fictícios. O projeto é material de aula e não deve ser usado com dados reais.

## Por onde começar

1. **[ROTEIRO.md](ROTEIRO.md)** — como rodar no seu computador e o que explorar, passo a passo.
2. **[docs/arquitetura.md](docs/arquitetura.md)** — o mapa do sistema (C4, camadas, módulos).
3. **[MISSOES.md](MISSOES.md)** — o que a equipe precisa construir, com critérios de aceite.

## Rodar em uma linha

```
mvn spring-boot:run
```

Depois abra <http://localhost:8080>. Requisitos: JDK 17 ou mais novo e Maven (ou uma IDE que já traga o Maven). Detalhes e solução de problemas no roteiro.

| Usuário | Perfil | O que enxerga |
|---|---|---|
| `recepcao` | Recepção | agenda, pacientes |
| `ana`, `rafael` | Profissional de saúde | atendimentos do dia, prontuário |
| `admin` | Administração | profissionais, auditoria |
| `joana` | Paciente | portal (missão E3-4) |

Senha de todos: `saude123`.

## Tecnologias

Java 17+, Spring Boot 3.5 (Web, Data JPA, Validation, Security com JWT, AOP), H2 em memória (PostgreSQL opcional), springdoc-openapi, JUnit 5, AssertJ e ArchUnit. A interface é HTML, CSS e JavaScript puros, servidos pela própria aplicação, sem etapa de build.

## Onde está cada assunto da disciplina

| Assunto | Onde olhar |
|---|---|
| Camadas (apresentação, aplicação, persistência) | módulo `cadastro`; Raio-X no rodapé da interface |
| Arquitetura hexagonal (portas e adaptadores) | módulos `agenda` e `prontuario` |
| Padrões: Repository, Service, DTO, Facade, injeção de dependência | `*Repository`, `*Service`, `*Resposta`/`*Info`, `*Fachada` |
| API REST (recursos, verbos, códigos de status, Problem Details) | controllers, `TratadorDeErros`, `docs/api.http`, `/swagger-ui.html` |
| Atributos de qualidade: segurança, auditabilidade, testabilidade | `SecurityConfig`, módulo `auditoria`, `src/test` |
| Decisões e tradeoffs | `docs/adr/` |
| Rastreabilidade requisito → decisão → componente → teste | `docs/rastreabilidade.md` |
| Arquitetura verificada por teste | `ArquiteturaTest` (ArchUnit) |
| Base para serviços e reutilização (Projeto Final) | pacotes `api` de cada módulo; missões PF |

## Estrutura

```
src/main/java/br/edu/ifpa/saudecerta/
  cadastro/      pacientes, profissionais, especialidades   (camadas)
  agenda/        consultas                                  (hexagonal)
  prontuario/    atendimentos e histórico clínico           (hexagonal)
  auditoria/     trilha de quem fez o quê
  seguranca/     login, token JWT, perfis de acesso
  painel/        resumo do dia (só leitura, compõe outros módulos)
  compartilhado/ erros da API, relógio e Raio-X
  demo/          dados de demonstração
src/main/resources/static/   interface web
src/test/java/               testes de domínio, de arquitetura e de integração
docs/                        arquitetura, ADRs, rastreabilidade, requisições prontas
```
