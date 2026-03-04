from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from time import perf_counter
from typing import Iterable


# -----------------------------
# EPIC 1 (já existia): carga e paginação
# -----------------------------
def extrair_palavras(linhas: Iterable[str]) -> list[str]:
    palavras: list[str] = []
    vistas: set[str] = set()
    duplicadas = 0

    for linha in linhas:
        palavra = linha.strip()
        if not palavra:
            continue
        if palavra in vistas:
            duplicadas += 1
            continue
        vistas.add(palavra)
        palavras.append(palavra)

    if not palavras:
        raise ValueError("Arquivo vazio ou sem palavras validas.")
    if duplicadas > 0:
        raise ValueError(f"Foram encontradas {duplicadas} palavras duplicadas no arquivo.")
    return palavras


def paginar(registros: list[str], tamanho_pagina: int) -> list[list[str]]:
    if tamanho_pagina <= 0:
        raise ValueError("Tamanho da pagina deve ser maior que zero.")
    return [
        registros[indice : indice + tamanho_pagina]
        for indice in range(0, len(registros), tamanho_pagina)
    ]


# Compatibilidade com nomes anteriores.
parse_words = extrair_palavras
paginate = paginar


# -----------------------------
# EPIC 2 (novo): índice hash estático
# -----------------------------
@dataclass(frozen=True)
class IndexEntry:
    chave: str
    pagina_id: int


@dataclass
class Bucket:
    fr: int
    primary: list[IndexEntry]
    overflow_pages: list[list[IndexEntry]]

    def __init__(self, fr: int) -> None:
        self.fr = fr
        self.primary = []
        self.overflow_pages = []

    def inserir(self, entry: IndexEntry) -> tuple[bool, bool]:
        """
        Retorna:
        - collision_occurred
        - overflow_bucket_occurred
        """

        # Cabe no bucket principal
        if len(self.primary) < self.fr:
            self.primary.append(entry)
            return (False, False)

        # ---------------------------
        # COLISÃO (HU07)
        # ---------------------------
        collision = True

        # ---------------------------
        # OVERFLOW (HU08)
        # ---------------------------
        overflow_bucket_occurred = False

        # Se ainda não existe overflow, cria
        if not self.overflow_pages:
            self.overflow_pages.append([])
            overflow_bucket_occurred = True

        # Tenta inserir na última página
        last_page = self.overflow_pages[-1]

        if len(last_page) < self.fr:
            last_page.append(entry)
        else:
            # Última página cheia → cria nova
            self.overflow_pages.append([entry])

        return (collision, overflow_bucket_occurred)


@dataclass
class IndexStats:
    nr: int
    fr: int
    nb: int
    build_time_sec: float
    collisions: int
    overflow_buckets: int
    overflow_pages_created: int
    overflow_entries: int

    @property
    def collision_rate_percent(self) -> float:
        return (self.collisions / self.nr * 100.0) if self.nr else 0.0

    @property
    def overflow_bucket_rate_percent(self) -> float:
        # Percentual de buckets que entraram em overflow (alinha com "quantos buckets entraram em overflow")
        return (self.overflow_buckets / self.nb * 100.0) if self.nb else 0.0


class StaticHashIndex:
    def __init__(self, fr: int, nb: int) -> None:
        if fr <= 0:
            raise ValueError("FR deve ser maior que zero.")
        if nb <= 0:
            raise ValueError("NB deve ser maior que zero.")
        self.fr = fr
        self.nb = nb
        self.buckets: list[Bucket] = [Bucket(fr) for _ in range(nb)]

    @staticmethod
    def calcular_nb(nr: int, fr: int) -> int:
        """
        Regra do PDF: NB > NR / FR.
        Escolha simples e segura: NB = floor(NR/FR) + 1
        """
        if fr <= 0:
            raise ValueError("FR deve ser maior que zero.")
        if nr < 0:
            raise ValueError("NR invalido.")
        return (nr // fr) + 1

    def hash_bucket(self, chave: str) -> int:
        """
        Função hash determinística (não usa hash() do Python).
        Retorna sempre no intervalo [0..NB-1].
        """
        digest = sha256(chave.encode("utf-8")).hexdigest()
        valor = int(digest, 16)
        return valor % self.nb

    def construir(self, paginas: list[list[str]]) -> IndexStats:
        """
        Percorre pagina por pagina e registro por registro,
        inserindo (chave -> pagina_id) no índice hash.
        """

        nr = sum(len(p) for p in paginas)

        start = perf_counter()

        collisions = 0
        overflow_buckets = 0
        overflow_entries = 0

        for pagina_id, pagina in enumerate(paginas, start=1):
            for chave in pagina:
                bucket_id = self.hash_bucket(chave)
                bucket = self.buckets[bucket_id]

                entry = IndexEntry(chave=chave, pagina_id=pagina_id)

                collision, overflow_bucket_occurred = bucket.inserir(entry)

                # -------------------------
                # HU07 - Colisão
                # -------------------------
                if collision:
                    collisions += 1
                    overflow_entries += 1  # toda inserção após FR vai para overflow

                # -------------------------
                # HU08 - Overflow
                # -------------------------
                if overflow_bucket_occurred:
                    overflow_buckets += 1

        end = perf_counter()

        return IndexStats(
            nr=nr,
            fr=self.fr,
            nb=self.nb,
            build_time_sec=end - start,
            collisions=collisions,
            overflow_buckets=overflow_buckets,
            overflow_pages_created=0,  # não usamos mais essa métrica
            overflow_entries=overflow_entries,
        )