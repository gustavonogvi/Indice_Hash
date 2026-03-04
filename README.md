# Projeto 1 - Indice Hash Estatico

## Objetivo
Desenvolver uma aplicacao grafica que simula um indice hash estatico sobre dados armazenados em paginas de memoria, com foco em demonstrar o comportamento da indexacao e comparar seu desempenho com table scan.

De acordo com o enunciado do projeto, a aplicacao deve:
- carregar um arquivo `.txt` com palavras unicas (uma por linha);
- dividir os registros em paginas conforme o tamanho informado pelo usuario;
- construir um indice hash estatico com buckets, respeitando `FR` (capacidade por bucket) e `NB` (quantidade de buckets);
- aplicar uma funcao hash deterministica para mapear chaves aos buckets;
- implementar tratamento de colisoes e overflow;
- permitir busca por indice e busca sequencial (table scan) para a mesma chave;
- apresentar metricas de colisoes, overflow, custo estimado em leituras de paginas e diferenca de tempo entre os metodos de busca;
- exibir visualmente paginas, buckets e o processo de busca na interface.

## Como Executar
```bash
pip install -r requirements.txt
streamlit run app.py
```
