# Projeto 1 - Indice Hash Estatico

## 1. Objetivo
Construir uma aplicacao com interface grafica que simula um indice hash estatico sobre uma tabela de dados paginada em memoria, permitindo comparar busca por indice versus table scan.

## 2. Escopo
O sistema deve:
- Carregar arquivo `.txt` com palavras unicas (1 palavra por linha).
- Organizar registros em paginas com tamanho configuravel.
- Construir indice hash estatico com `NB` buckets e capacidade `FR`.
- Executar busca por indice de uma chave.
- Executar table scan para comparacao.
- Exibir metricas de colisao, overflow, custo (leituras de paginas) e tempo.
- Exibir visualmente paginas, buckets e processo de busca.

## 3. Glossario
- Registro/Tupla: palavra lida do arquivo.
- Chave de busca: palavra usada para localizar registro.
- Pagina: bloco logico com N registros.
- Bucket: estrutura do indice hash que guarda pares `(chave -> endereco_pagina)`.
- FR: capacidade do bucket.
- NB: quantidade total de buckets.
- Colisao: tentativa de inserir em bucket cheio (excede FR).
- Overflow: uso de estrutura/estrategia de transbordamento.
- Table scan: leitura sequencial de paginas ate encontrar chave.

## 4. Regras de Negocio (RN)
- RN01: arquivo deve conter uma palavra por linha.
- RN02: cada palavra e chave unica.
- RN03: suportar aproximadamente 466.000 palavras.
- RN04: tamanho da pagina informado na interface.
- RN05: tamanho da pagina deve ser `> 0`.
- RN06: divisao em paginas depende do tamanho informado.
- RN07: numero de paginas calculado automaticamente.
- RN08: `NB > NR / FR` (NR = numero de registros).
- RN09: `FR` definido pela equipe.
- RN10: funcao hash mapeia chave para bucket.
- RN11: funcao hash escolhida/projetada pela equipe.
- RN12: construcao do indice percorre paginas e registros.
- RN13: para cada registro, armazenar `(chave, endereco_pagina)` no bucket resultante.
- RN14: contabilizar colisoes apenas quando bucket estiver cheio (exceder FR).
- RN15: implementar estrategia de resolucao de colisoes.
- RN16: implementar tratamento de overflow.
- RN17: implementar algoritmo de resolucao de overflow.
- RN18: interface deve possuir campo para chave de busca.
- RN19: busca por indice aplica hash, localiza bucket, recupera pagina e valida tupla.
- RN20: table scan habilitado apos informar chave.
- RN21: table scan le pagina por pagina ate encontrar chave.
- RN22: mostrar diferenca de tempo entre busca por indice e table scan.
- RN23: estimar custo em leituras de paginas.
- RN24: calcular/exibir taxa de colisoes (%).
- RN25: calcular/exibir taxa de overflow (%).
- RN26: interface grafica obrigatoria.
- RN27: interface deve ilustrar paginas, buckets, processo de busca e localizacao do registro.

## 5. Requisitos Funcionais (RF)

### RF01 - Carga de dados
- Selecionar arquivo `.txt`.
- Carregar palavras e informar total.
- Tratar arquivo vazio/ilegivel.

### RF02 - Paginacao
- Receber tamanho de pagina.
- Validar entrada (`> 0`).
- Dividir registros em paginas.
- Exibir total de paginas.
- Exibir primeira e ultima pagina:
  - numero da pagina
  - primeiros 5 registros

### RF03 - Estrutura do indice hash
- Definir `FR`.
- Calcular `NB` respeitando `NB > NR / FR`.
- Criar `NB` buckets com capacidade `FR`.
- Validar e impedir configuracao invalida.

### RF04 - Funcao hash
- Implementar funcao deterministica.
- Garantir retorno no intervalo `[0, NB-1]`.

### RF05 - Construcao do indice
- Percorrer paginas e registros.
- Inserir pares `(chave, endereco_pagina)` no indice.
- Tratar colisoes e overflow.
- Exibir tempo de construcao.

### RF06 - Busca por indice
- Informar chave de busca.
- Exibir:
  - chave encontrada/nao encontrada
  - numero da pagina
  - custo estimado (leituras de paginas)

### RF07 - Table scan
- Executar varredura sequencial por paginas.
- Exibir registros/paginas lidos ate encontrar chave.
- Exibir pagina encontrada e custo (paginas lidas).

### RF08 - Comparativo indice x scan
- Exibir tempo da busca por indice.
- Exibir tempo do table scan.
- Exibir diferenca percentual de tempo.
- Exibir custo estimado de ambos.

### RF09 - Metricas
- Exibir taxa de colisoes (%).
- Exibir taxa de overflow (%).

### RF10 - Visualizacao grafica
- Exibir conteudo de buckets.
- Destacar bucket acessado durante busca.
- Destacar pagina acessada durante busca.

## 6. Requisitos Nao Funcionais (RNF)
- RNF01: suportar pelo menos 466.000 registros sem travar.
- RNF02: exibir tempo de construcao do indice.
- RNF03: implementacao pode ser em qualquer linguagem.
- RNF04: interface deve ser visual (desktop ou web); terminal puro nao e aceito.
- RNF05: comportamento deterministico para mesma entrada.

## 7. Criterios de Aceitacao Consolidados
- CA01-CA03: carga correta de arquivo e tratamento de erro.
- CA04-CA05: entrada valida de tamanho de pagina.
- CA06-CA07: paginacao e exibicao de primeira/ultima pagina.
- CA08-CA10: calculo/criacao de buckets e validacao de `NB`.
- CA11-CA12: funcao hash deterministica e em faixa valida.
- CA13-CA14: indice completo e tempo de construcao exibido.
- CA15-CA16: colisoes tratadas e contabilizadas.
- CA17-CA18: overflow tratado e contabilizado.
- CA19-CA20: busca por indice com resultado e custo.
- CA21-CA22: table scan com leitura e custo exibidos.
- CA23-CA24: comparativo de tempo/custo e diferenca percentual.
- CA25-CA26: metricas de colisao/overflow exibidas.
- CA27-CA29: visualizacao grafica de paginas, buckets e busca.

## 8. Formulas de Referencia
- Numero de paginas: `ceil(NR / tam_pagina)`
- Regra de buckets: `NB > NR / FR`
- Taxa de colisoes (%): `(insercoes_em_bucket_cheio / NR) * 100`
- Taxa de overflow (%): `(buckets_com_overflow / NB) * 100`
- Custo indice (estimado): `leituras_bucket + leituras_pagina`
- Custo table scan: `paginas_lidas_ate_encontrar`
- Diferenca percentual de tempo (%): `((t_scan - t_indice) / t_scan) * 100`

## 9. Premissas e Pendencias Tecnicas
- Definir algoritmo de hash oficial da equipe.
- Definir estrategia de resolucao de colisao/overflow:
  - opcao recomendada para o projeto: encadeamento em area de overflow por bucket.
- Definir stack da interface (web ou desktop).
- Definir dataset padrao para demonstracao e testes.

## 10. Checklist de Pronto para Implementacao
- [ ] Requisitos revisados e aprovados pela equipe.
- [ ] Estrategia de hash e overflow definida.
- [ ] Layout da interface (wireframe simples) definido.
- [ ] Plano de testes com casos de busca encontrada/nao encontrada definido.
- [ ] Criterios de desempenho minimo definidos para 466k registros.
