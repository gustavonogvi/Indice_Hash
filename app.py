from __future__ import annotations

from typing import Any

import streamlit as st

from indice_hash import StaticHashIndex, extrair_palavras, paginar


st.set_page_config(page_title="Indice Hash - Projeto", layout="wide")
st.title("Indice Hash - Projeto")
st.caption("EPIC 1 (carga/paginacao) + EPIC 2 (buckets/hash/construcao do indice).")


def ler_arquivo_enviado(arquivo_enviado: Any) -> list[str]:
    conteudo_bruto = arquivo_enviado.getvalue()
    try:
        texto = conteudo_bruto.decode("utf-8")
    except UnicodeDecodeError:
        texto = conteudo_bruto.decode("latin-1")
    return extrair_palavras(texto.splitlines())


def renderizar_previa_pagina(id_pagina: int, pagina: list[str]) -> None:
    st.markdown(f"**Pagina {id_pagina}**")
    previa = pagina[:5]
    st.code("\n".join(previa) if previa else "(vazia)", language="text")


def renderizar_bucket(bucket_id: int, bucket: Any) -> None:
    st.markdown(f"### Bucket {bucket_id}")

    st.markdown("**Primary**")
    if bucket.primary:
        st.code(
            "\n".join([f"{e.chave} -> pagina {e.pagina_id}" for e in bucket.primary]),
            language="text",
        )
    else:
        st.code("(vazio)", language="text")

    st.markdown("**Overflow pages**")
    if bucket.overflow_pages:
        for i, page in enumerate(bucket.overflow_pages, start=1):
            st.markdown(f"- Overflow Page {i}")
            st.code(
                "\n".join([f"{e.chave} -> pagina {e.pagina_id}" for e in page]) if page else "(vazia)",
                language="text",
            )
    else:
        st.code("(sem overflow)", language="text")


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Configuracao (EPIC 1)")
    tamanho_pagina = st.number_input(
        "Tamanho da pagina (registros)", min_value=1, value=200, step=1
    )
    arquivo_enviado = st.file_uploader("Arquivo .txt (1 palavra por linha)", type=["txt"])

    st.divider()
    st.header("Configuracao (EPIC 2)")
    fr = st.number_input("FR (capacidade do bucket)", min_value=1, value=4, step=1)

# ---------------- EPIC 1: carregar e paginar ----------------
col_btn1, col_btn2 = st.columns([1, 2])

with col_btn1:
    if st.button("Carregar e paginar (EPIC 1)", type="primary"):
        if arquivo_enviado is None:
            st.error("Selecione um arquivo .txt.")
        else:
            try:
                registros = ler_arquivo_enviado(arquivo_enviado)
                paginas = paginar(registros, int(tamanho_pagina))

                st.session_state["registros"] = registros
                st.session_state["paginas"] = paginas
                st.session_state["tamanho_pagina"] = int(tamanho_pagina)

                # Limpa índice antigo se recarregar
                st.session_state.pop("indice", None)
                st.session_state.pop("stats", None)

            except Exception as exc:
                st.error(f"Erro ao carregar arquivo: {exc}")

with col_btn2:

    registros = st.session_state.get("registros")
paginas = st.session_state.get("paginas")
tamanho_pagina_carregado = st.session_state.get("tamanho_pagina")

if paginas:
    st.subheader("EPIC 1 — Resultado")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de palavras", len(registros))
    c2.metric("Total de paginas", len(paginas))
    c3.metric("Tamanho da pagina", tamanho_pagina_carregado)

    col_esq, col_dir = st.columns(2)
    with col_esq:
        renderizar_previa_pagina(1, paginas[0])
    with col_dir:
        renderizar_previa_pagina(len(paginas), paginas[-1])

    st.divider()

    # ---------------- EPIC 2: construir índice ----------------
    st.subheader("EPIC 2 — Construção do Índice Hash Estático")

    nr = len(registros)
    nb_calculado = StaticHashIndex.calcular_nb(nr=nr, fr=int(fr))

    c4, c5, c6 = st.columns(3)
    c4.metric("NR (registros)", nr)
    c5.metric("FR (capacidade)", int(fr))
    c6.metric("NB (buckets)", nb_calculado)

    if st.button("Construir indice hash (EPIC 2)", type="primary"):
        try:
            indice = StaticHashIndex(fr=int(fr), nb=nb_calculado)
            stats = indice.construir(paginas)

            st.session_state["indice"] = indice
            st.session_state["stats"] = stats
            st.session_state.pop("resultado_indice", None)
            st.session_state.pop("resultado_scan", None)

        except Exception as exc:
            st.error(f"Erro ao construir indice: {exc}")

    stats = st.session_state.get("stats")
    indice = st.session_state.get("indice")

    if stats is not None and indice is not None:
        st.success("Indice construido com sucesso!")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tempo de construcao (s)", f"{stats.build_time_sec:.4f}")
        m2.metric("Colisoes (count)", stats.collisions)
        m3.metric("Taxa de colisoes (%)", f"{stats.collision_rate_percent:.4f}")
        m4.metric("Buckets em overflow", stats.overflow_buckets)

        m5, m6, m7 = st.columns(3)
        m5.metric("Taxa overflow (buckets %)", f"{stats.overflow_bucket_rate_percent:.4f}")
        m6.metric("Overflow pages criadas", stats.overflow_pages_created)
        m7.metric("Entradas em overflow", stats.overflow_entries)

        st.divider()
        st.subheader("Visualizacao (HU14 - parcial): Buckets e conteudo")

        # Para não travar exibindo tudo, deixamos escolher um bucket.
        bucket_id = st.number_input(
            "Escolha um bucket para inspecionar",
            min_value=0,
            max_value=indice.nb - 1,
            value=0,
            step=1,
        )

        renderizar_bucket(int(bucket_id), indice.buckets[int(bucket_id)])

        # ---------------- EPIC 3: busca e comparativo ----------------
        st.divider()
        st.subheader("EPIC 3 — Busca e Comparativo")

        chave_busca = st.text_input("Chave de busca (palavra)")

        col_b1, col_b2 = st.columns(2)

        if col_b1.button("Buscar por indice (EPIC 3)", type="primary", disabled=not chave_busca):
            st.session_state["resultado_indice"] = indice.buscar(chave_busca)

        if col_b2.button("Table scan (EPIC 3)", disabled=not chave_busca):
            st.session_state["resultado_scan"] = StaticHashIndex.table_scan(chave_busca, paginas)

        resultado_indice = st.session_state.get("resultado_indice")
        resultado_scan = st.session_state.get("resultado_scan")

        if resultado_indice is not None:
            st.markdown("#### Resultado — Busca por Indice")
            if resultado_indice.encontrada:
                st.success(f"Chave **'{resultado_indice.chave}'** encontrada na pagina {resultado_indice.pagina_id}.")
            else:
                st.error(f"Chave **'{resultado_indice.chave}'** nao encontrada.")
            r1, r2, r3 = st.columns(3)
            r1.metric("Bucket acessado", resultado_indice.bucket_id)
            r2.metric("Custo (leituras)", resultado_indice.custo_leituras)
            r3.metric("Tempo (s)", f"{resultado_indice.tempo_sec:.6f}")

            st.markdown("**Conteudo do bucket acessado:**")
            renderizar_bucket(resultado_indice.bucket_id, indice.buckets[resultado_indice.bucket_id])

            if resultado_indice.encontrada and resultado_indice.pagina_id is not None:
                st.markdown(f"**Pagina de dados acessada (Pagina {resultado_indice.pagina_id}):**")
                pagina_dados = paginas[resultado_indice.pagina_id - 1]
                linhas_destacadas = [
                    f">>> {r}  ← encontrada aqui" if r == resultado_indice.chave else f"    {r}"
                    for r in pagina_dados
                ]
                st.code("\n".join(linhas_destacadas), language="text")

        if resultado_scan is not None:
            st.markdown("#### Resultado — Table Scan")
            if resultado_scan.encontrada:
                st.success(f"Chave **'{resultado_scan.chave}'** encontrada na pagina {resultado_scan.pagina_id}.")
            else:
                st.error(f"Chave **'{resultado_scan.chave}'** nao encontrada.")
            s1, s2 = st.columns(2)
            s1.metric("Custo (paginas lidas)", resultado_scan.paginas_lidas)
            s2.metric("Tempo (s)", f"{resultado_scan.tempo_sec:.6f}")

            with st.expander(f"Paginas lidas durante o scan ({len(resultado_scan.paginas_visitadas)})"):
                for pid in resultado_scan.paginas_visitadas:
                    pagina_conteudo = paginas[pid - 1]
                    previa = pagina_conteudo[:5]
                    encontrada_aqui = resultado_scan.encontrada and pid == resultado_scan.pagina_id
                    label = f"**Pagina {pid}** ✓ (encontrada aqui)" if encontrada_aqui else f"Pagina {pid}"
                    st.markdown(label)
                    st.code("\n".join(previa), language="text")

        # Comparativo (exibe somente quando ambos foram executados para a mesma chave)
        if (
            resultado_indice is not None
            and resultado_scan is not None
            and resultado_indice.chave == resultado_scan.chave
        ):
            st.markdown("#### Comparativo Indice x Table Scan")
            t_indice = resultado_indice.tempo_sec
            t_scan = resultado_scan.tempo_sec
            diff_pct = ((t_scan - t_indice) / t_scan * 100.0) if t_scan else 0.0

            cp1, cp2, cp3 = st.columns(3)
            cp1.metric("Tempo indice (s)", f"{t_indice:.6f}")
            cp2.metric("Tempo scan (s)", f"{t_scan:.6f}")
            cp3.metric("Indice mais rapido (%)", f"{diff_pct:.2f}")

            cc1, cc2 = st.columns(2)
            cc1.metric("Custo indice (leituras)", resultado_indice.custo_leituras)
            cc2.metric("Custo scan (paginas lidas)", resultado_scan.paginas_lidas)

else:
    st.info("Carregue um arquivo e pagine (EPIC 1) para liberar a construcao do indice (EPIC 2).")