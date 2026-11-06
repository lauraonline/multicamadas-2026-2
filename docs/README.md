# Documentação SaúdeCerta

## E1 - Visão e requisitos

- [Visão](visao.md)
- [Catálogo de requisitos e drivers](requisitos.md)
- [PDF original da E1](SaudeCerta_E1_Visao_e_Requisitos_Core4Tech.pdf)

## E2 - Projeto arquitetural

- [PDF consolidado](SaudeCerta_E2_Projeto_Arquitetural_Core4Tech.pdf)
- [Arquitetura, camadas, componentes e fluxos](arquitetura.md)
- [C4 e domínio editáveis no diagrams.net](arquitetura.drawio)
- [Modelo de domínio](modelo-dominio.md)
- [Cenários de qualidade](cenarios-qualidade.md)
- [Seis ADRs](adr/README.md)
- [Matriz de rastreabilidade](rastreabilidade.md)
- [Referências e organização da entrega](referencias.md)

## Reprodução e validação

Requer Python 3, reportlab, Pillow e PyMuPDF. Em ambiente virtual: `python -m pip install -r docs/scripts/requirements.txt`. Da raiz: `python docs/scripts/gerar_e2.py` gera drawio, PNGs e PDF a partir dos Markdown e de diagramas/modelos.json. Não requer fontes/, rede nem aplicação Java em execução após instalar dependências. Valide com `python docs/scripts/validar_e2.py`. Edite modelos.json para alterar elementos/posições dos diagramas e regenere; alterações só no drawio exportado serão substituídas.

O PDF inclui a arquitetura, o modelo, todos os cenários, os seis ADRs, a matriz e as referências. Os PNGs também estão embutidos nos Markdown para leitura direta no GitHub. A validação estrutural não comprova RNFs; esses testes ficam planejados para E3/PF. A revisão visual do PDF deve ser repetida após mudanças de layout.
