
# Checklist do Projeto — Índice Hash

## EPIC 1 — Carga e organização dos dados

### HU01 — Carregar arquivo de dados
- [x] Permitir selecionar um arquivo `.txt`
- [x] Ler o conteúdo do arquivo
- [x] Considerar **1 palavra por linha**
- [x] Validar arquivo vazio
- [x] Validar palavras duplicadas
- [x] Armazenar palavras em memória

### HU02 — Paginar registros
- [x] Definir tamanho da página
- [x] Dividir registros em páginas
- [x] Mostrar número total de páginas
- [x] Mostrar número total de palavras

### HU03 — Visualizar páginas
- [x] Mostrar prévia da primeira página
- [x] Mostrar prévia da última página
- [x] Permitir inspeção dos registros

---

## EPIC 2 — Construção do Índice Hash Estático

### HU04 — Criar buckets
- [x] Definir **FR (capacidade do bucket)**
- [x] Calcular **NB (número de buckets)**
- [x] Garantir regra:

```
NB > NR / FR
```

- [x] Criar estrutura de buckets
- [x] Validar valores inválidos

### HU05 — Implementar função hash
- [x] Definir função hash da equipe
- [x] Mapear chave → bucket
- [x] Garantir intervalo `[0..NB-1]`
- [x] Usar hash determinística

### HU06 — Construir índice
- [x] Percorrer páginas de dados
- [x] Aplicar função hash em cada chave
- [x] Inserir entrada `(chave → página)`
- [x] Medir tempo de construção do índice

---

## EPIC 3 — Tratamento de Colisões e Overflow

### HU07 — Resolver colisões
- [x] Detectar bucket cheio (FR)
- [x] Contabilizar colisões
- [x] Permitir múltiplas chaves no mesmo bucket
- [x] Implementar estratégia de resolução

### HU08 — Resolver overflow
- [x] Criar páginas de overflow
- [x] Encadear páginas adicionais
- [x] Contabilizar buckets em overflow
- [x] Armazenar entradas adicionais

---

## EPIC 4 — Busca usando índice

### HU09 — Buscar usando índice
- [x] Permitir digitar chave de busca
- [x] Aplicar função hash
- [x] Localizar bucket
- [x] Buscar na página principal
- [x] Buscar nas páginas de overflow
- [x] Recuperar página de dados
- [x] Carregar página e verificar registro
- [x] Mostrar página encontrada
- [x] Mostrar custo em páginas lidas

---

## EPIC 5 — Table Scan

### HU10 — Implementar Table Scan
- [x] Percorrer páginas de dados sequencialmente
- [x] Buscar chave página por página
- [x] Parar quando encontrar
- [x] Mostrar página encontrada
- [x] Mostrar páginas percorridas
- [x] Mostrar custo do scan (páginas lidas)

### HU11 — Comparar desempenho
- [x] Medir tempo da busca por índice
- [x] Medir tempo do table scan
- [x] Comparar custo em páginas
- [x] Mostrar diferença percentual

---

## EPIC 6 — Estatísticas do índice

### HU12 — Taxa de colisões
- [x] Contar número de colisões
- [x] Calcular taxa de colisão (%)
- [x] Mostrar taxa na interface

### HU13 — Taxa de overflow
- [x] Contar buckets em overflow
- [x] Calcular taxa de overflow (%)
- [x] Mostrar taxa na interface

---

## EPIC 7 — Interface e visualização

### HU14 — Visualização do índice
- [x] Exibir buckets
- [x] Exibir conteúdo do bucket
- [x] Mostrar páginas de overflow
- [x] Destacar bucket acessado durante busca
- [x] Destacar página acessada

---

## Status atual do projeto

```
EPIC 1  ✅ Concluído
EPIC 2  ✅ Concluído
EPIC 3  ✅ Concluído
EPIC 4  ✅ Concluído
EPIC 5  ✅ Concluído
EPIC 6  ✅ Concluído
EPIC 7  ✅ Concluído
```
