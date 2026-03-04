# Backlog Priorizado - Projeto Indice Hash
Legenda de status: `[x]` Concluido | `[ ]` Nao iniciado | `[~]` Parcial

## Fase 1 - Base obrigatoria (MVP)
- [~] B01: carregar arquivo TXT e validar formato. Feito: upload `.txt`, leitura com fallback de encoding, remocao de linhas vazias e validacao de duplicadas. Falta: validar estritamente "1 palavra por linha" (sem espacos internos) e diferenciar erro de arquivo ilegivel/corrompido.
- [x] B02: entrada de tamanho de pagina com validacao.
- [x] B03: dividir registros em paginas e exibir total.
- [x] B04: exibir primeira e ultima pagina (5 primeiros registros).
- [ ] B05: definir `FR`, calcular `NB` e criar buckets.
- [ ] B06: implementar funcao hash deterministica.
- [ ] B07: construir indice percorrendo pagina por pagina.
- [ ] B08: tratar colisao e overflow.
- [ ] B09: busca por indice com pagina e custo estimado.
- [ ] B10: table scan com pagina e custo.
- [ ] B11: comparar tempo e custo (indice x scan).
- [ ] B12: exibir taxa de colisao e overflow.

## Fase 2 - Interface e visualizacao
- [~] B13: tela de carga/configuracao. Feito: tela Streamlit com upload, tamanho de pagina, botao de processamento e metricas iniciais. Falta: organizar layout final da etapa completa (busca, buckets, comparativos e fluxo de uso consolidado).
- [ ] B14: painel de paginas (primeira/ultima + navegacao opcional).
- [ ] B15: painel de buckets e overflow.
- [ ] B16: destaque visual de bucket/pagina durante busca.
- [ ] B17: painel de metricas e comparativos.

## Fase 3 - Robustez e demostracao
- [ ] B18: testes com chaves existentes e inexistentes.
- [ ] B19: teste de volume com dataset grande (~466k).
- [~] B20: tratamento de erros (arquivo vazio, ilegivel, parametros invalidos). Feito: arquivo vazio, palavras duplicadas, ausencia de upload e tamanho de pagina invalido no nucleo. Falta: mensagens especificas para arquivo nao TXT/ilegivel em todos os cenarios e testes automatizados desses casos.
- [ ] B21: roteiro de apresentacao da equipe.

## Definicoes que devem ser fechadas agora
- [x] D01: stack de interface (web ou desktop).
- [ ] D02: valor inicial de `FR`.
- [ ] D03: estrategia de overflow (encadeamento, area extra etc.).
- [ ] D04: funcao hash oficial da equipe.
