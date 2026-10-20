# Documentação de Visão e Requisitos: Sistema SaúdeCerta

---

## 1. Visão do Produto e Problema

### Contexto e Problema Atual
A **Clínica SaúdeCerta** é uma unidade de saúde de médio porte que conta com cerca de vinte profissionais de diversas especialidades. Atualmente, a gestão de agendamentos é feita por meio de planilhas compartilhadas e os prontuários dos pacientes são mantidos fisicamente em papel. 

Esse cenário operacional gera falhas graves e recorrentes:
* **Conflito de agendas:** Ocorrência de marcações duplas para o mesmo profissional no mesmo horário.
* **Ineficiência operacional:** Lentidão na localização do histórico do paciente e alto nível de retrabalho na recepção durante reagendamentos ou cancelamentos.
* **Insegurança e vulnerabilidade de dados:** Risco direto no manuseio de dados sensíveis de saúde, visto que os arquivos físicos não possuem rastreabilidade de acesso (auditoria de quem acessou o quê).

### Visão do Produto
A direção da clínica contratou o desenvolvimento de um sistema web multicamadas com integração via WhatsApp para digitalizar e automatizar todo o fluxo de atendimento — desde a marcação de consultas até o registro de prontuários e prescrições. 

O sistema tem como objetivo garantir a segurança e a privacidade dos dados de saúde, além de utilizar a arquitetura **monólito modular** que permita o crescimento contínuo do software sem necessidade de reescrita.

---

## 2. Stakeholders e Atores

### Stakeholders (Interessados no Negócio)
* **Direção/Gerência da Clínica:** Busca eficiência operacional, redução de custos com retrabalho, controle de agendamentos e conformidade legal com a proteção de dados sensíveis.
* **Recepcionistas:** Querem agilidade no atendimento, redução do retrabalho e eliminação de conflitos de horários.
* **Médicos e Profissionais da Saúde:** Desejam acesso rápido e seguro à agenda diária e ao prontuário digital do paciente.
* **Pacientes:** Buscam facilidade, praticidade e autonomia para agendar, consultar, remarcar ou desmarcar suas consultas sem complicação.

### Atores do Sistema

#### Atores Principais (Usuários Diretos)
* **Paciente:** Interage com o sistema (via chat interativo no WhatsApp ou interface web) para realizar autoatendimento de consultas.
* **Médico / Profissional de Saúde:** Acessa a plataforma para consultar horários e registrar atendimentos/prontuários.
* **Recepcionista / Operador:** Atua na gestão e suporte aos agendamentos e cadastros na recepção.

#### Atores Secundários (Sistemas Externos e Infraestrutura)
* **Plataforma/API do WhatsApp (Meta API / Provedor de Mensageria):** Atua como o canal de comunicação primário, interceptando mensagens e exibindo menus interativos/formulários ao paciente.
* **Banco de Dados (PostgreSQL/MySQL):** Responsável pelo armazenamento seguro, validação de credenciais e integridade das informações de saúde.
* **Servidor de Autenticação:** Responsável por gerenciar o controle de acesso, a emissão de tokens de sessão (JWT) para os profissionais de saúde e recepcionistas, e a validação das credenciais de login dos usuários, garantindo que apenas pessoas autorizadas manipulem dados sensíveis de saúde e prontuários.

---

## 3. Requisitos Funcionais (RF) e Não Funcionais (RNF)

### Requisitos Funcionais (RF)

| Identificador | Descrição |
| :--- | :--- |
| **RF 01** | Cadastrar perfis para pacientes. |
| **RF 02** | Cadastrar perfis para profissionais da saúde. |
| **RF 03** | Definir dias e horários de disponibilidade para profissionais da saúde. |
| **RF 04** | Marcar consultas entre pacientes e profissionais da saúde. |
| **RF 05** | Remarcar e desmarcar consultas previamente agendadas. |

### Requisitos Não Funcionais (RNF)

| Identificador | Categoria | Descrição |
| :--- | :--- | :--- |
| **RNF 01** | Desempenho | Ao buscar por um paciente ou profissional da saúde, os resultados da busca devem ser exibidos na tela em até 3 segundos. |
| **RNF 02** | Disponibilidade e Recuperabilidade | O sistema deve ser capaz de se recuperar totalmente de um período de indisponibilidade em até 30 minutos. |

---

## 4. Regras de Negócio (RN) e Drivers Arquiteturais

| Identificador | Nome | Descrição |
| :--- | :--- | :--- |
| **RN 01** | Identificação Secundária do Paciente | Para fins de validação/autenticação no atendimento, o paciente deve ser identificado e confirmado pelo nome da mãe em vez do CPF. |
| **RN 02** | Bloqueio de Horário Duplo | Um profissional da saúde não pode ter duas consultas com status `AGENDADA` no mesmo horário. |
| **RN 03** | Validação Temporal | Só é permitido realizar agendamentos para consultas com data e horário iguais ou futuros em relação ao momento corrente. |
| **RN 04** | Validação para Cancelamento | O cancelamento de uma consulta exige estritamente que o seu status atual seja `AGENDADA`. |

---

## 5. Escolha Justificada do Estilo Arquitetural Inicial

**Decisão:** Adotar o estilo arquitetural de **Monólito Modular**.

O sistema será implantado como uma unidade única de implantação (*deploy*), mas internamente seu código-fonte será rigidamente estruturado em módulos independentes com responsabilidades bem isoladas:

* **Módulo de Cadastro e Stakeholders:** Gestão de perfis (Pacientes, Médicos, Recepcionistas).
* **Módulo de Agenda:** Gestão de disponibilidade, marcações, reagendamentos e cancelamentos.
* **Módulo de Prontuário:** Histórico clínico e registro de consultas.
* **Módulo de Segurança e Autenticação:** Controle de acessos, permissões e auditoria.

### Justificativa Estratégica

* **Eficiência para Equipes Pequenas e Agilidade de Entrega:** Permite focar o esforço da equipe nas regras de negócio e na experiência do usuário (via web e WhatsApp), reduzindo drasticamente o tempo gasto com configurações complexas de infraestrutura e gerenciamento de microsserviços.
* **Baixa Complexidade Operacional:** Sendo uma única aplicação, o processo de compilação, teste, deploy e monitoramento é significativamente mais simples, garantindo alta produtividade no estágio inicial da aplicação.
* **Arquitetura Evolutiva (Evolutividade e Preparação para Extração Futura):** Ao manter o desacoplamento estrito entre os módulos (usando interfaces bem definidas, contratos claros e comunicação interna desacoplada), o sistema garante que, caso haja necessidade futura de dimensionamento ou isolamento de um domínio específico (como transformar o módulo de Agenda ou Prontuário em um microsserviço), isso poderá ser feito de forma cirúrgica e sem a necessidade de reescrever o sistema do zero.

### Consequências e Trade-offs

#### (+) Vantagens (Positivas)
* Alta velocidade no ciclo de desenvolvimento e implantação (*Time-to-Market*).
* Simplicidade no monitoramento e gerenciamento da aplicação.
* Fronteiras de domínio limpas, pavimentando o caminho para uma futura arquitetura distribuída (microsserviços), se o volume de acessos exigir.

#### (−) Desvantagens e Mitigação (Negativas)
* **Risco de Acoplamento:** Exige disciplina rígida de arquitetura e código para evitar que os módulos façam chamadas diretas ou dependências indesejadas entre suas camadas internas.
* **Mitigação:** Serão aplicadas boas práticas de arquitetura limpa (*Clean Architecture* / *Domain-Driven Design*) e testes para manter os limites entre os módulos sempre preservados.
