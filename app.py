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

        except Exception as exc:
            st.error(f"Erro ao construir indice: {exc}")

    stats = st.session_state.get("stats")
    indice = st.session_state.get("indice")

    if stats and indice:
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

else:
    st.info("Carregue um arquivo e pagine (EPIC 1) para liberar a construcao do indice (EPIC 2).")