"""
apply_refinements_v2.py
-----------------------
Applies second round of refinements:
  1. Executive summary cell at the top (after the Colab badge)
  2. Markdown before cell 29 (numeric consistency check)
  3. Markdown before cell 75 (seaborn heatmap)
  4. Markdown bridge between total_por_sexo and proporcao_sexo (cell 101)
  5. Markdown bridge between estrutura_etaria and proporcao_etaria (cell 108)
"""

import json
from pathlib import Path

NB_PATH = Path("data_analysis_and_good_practices.ipynb")

with open(NB_PATH, encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]


def src(c):
    s = c.get("source", [])
    return "".join(s) if isinstance(s, list) else s


def set_src(c, text):
    c["source"] = text


def find_idx(pattern):
    for i, c in enumerate(cells):
        if pattern in src(c):
            return i
    raise ValueError(f"Cell not found: {pattern!r}")


def mk_md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def insert_before(pattern, new_cell):
    idx = find_idx(pattern)
    cells.insert(idx, new_cell)
    print(f"  ✓ inserted markdown before idx {idx} ({pattern[:50]!r})")


def insert_after(pattern, new_cells_list):
    idx = find_idx(pattern)
    for offset, nc in enumerate(new_cells_list):
        cells.insert(idx + 1 + offset, nc)
    print(f"  ✓ inserted {len(new_cells_list)} cell(s) after idx {idx}")


# ── 1. EXECUTIVE SUMMARY ──────────────────────────────────────────────────────
print("\n── 1. Sumário executivo ───────────────────────────────────────────────")

exec_summary = """\
## Sumário executivo

Este notebook analisa como a população alfabetizada se distribui entre os bairros \
do Rio de Janeiro em três cortes censitários — 2000, 2010 e 2022 — a partir de \
dados públicos do Data.Rio.

O trabalho cobre as etapas de definição do problema, análise exploratória e \
pré-processamento de dados. A análise parte de quatro hipóteses exploratórias \
e responde a cada uma delas ao final com base em evidências descritivas. \
O foco recai sobre volumes absolutos de população alfabetizada: \
os resultados não permitem inferir desigualdade *relativa* de alfabetização, \
pois não dispomos do denominador populacional por bairro.

**Principais achados:** a distribuição é heterogênea e essa heterogeneidade \
permanece ao longo do período; os maiores bairros ampliam marginalmente sua \
participação; a composição por sexo é estável entre bairros; \
há evidência consistente de envelhecimento da população alfabetizada."""

# Insert after the Colab badge cell (first markdown cell, index 0)
cells.insert(1, mk_md(exec_summary))
print(f"  ✓ inserted executive summary at index 1")


# ── 2. ORPHAN: checagem de consistência numérica (was cell 29, now shifted) ──
print("\n── 2. Orphan: consistência numérica ──────────────────────────────────")

consistency_md = """\
Verificadas as estruturas básicas dos três arquivos, realiza-se a checagem de \
consistência numérica nas variáveis substantivas — excluindo identificadores \
territoriais cujos valores inteiros são esperados. \
O objetivo é detectar eventuais colunas lidas como texto que deveriam ser \
numéricas, o que comprometeria cálculos posteriores."""

insert_before("Checagem de consistência numérica apenas nas variáveis substantivas", mk_md(consistency_md))


# ── 3. ORPHAN: seaborn heatmap ────────────────────────────────────────────────
print("\n── 3. Orphan: heatmap seaborn ────────────────────────────────────────")

heatmap_md = """\
Com a matriz de correlação calculada, visualiza-se o padrão de associação entre \
as variáveis analíticas principais — totais por sexo, proporções e faixas etárias \
agregadas — para o ano de referência 2022."""

insert_before("import seaborn as sns\n\nfig, ax = plt.subplots(figsize=FIG_SIZE_HEATMAP)", mk_md(heatmap_md))


# ── 4. ORPHAN: proporcao_sexo bridge ─────────────────────────────────────────
print("\n── 4. Orphan: proporcao_sexo ─────────────────────────────────────────")

prop_sexo_md = """\
A partir dos totais absolutos por sexo, calculam-se as proporções \
`prop_f` e `prop_m` — que permitem verificar se a composição de sexo \
varia entre bairros o suficiente para explicar diferenças nos totais observados."""

insert_before("def proporcao_sexo(df):\n    df[\"prop_f\"]", mk_md(prop_sexo_md))


# ── 5. ORPHAN: proporcao_etaria bridge ───────────────────────────────────────
print("\n── 5. Orphan: proporcao_etaria ───────────────────────────────────────")

prop_etaria_md = """\
De forma análoga, calculam-se as proporções etárias `prop_jovens` e `prop_idosos`, \
que permitem comparar o perfil de envelhecimento entre bairros e ao longo do tempo."""

insert_before("def proporcao_etaria(df):\n    df[\"prop_jovens\"]", mk_md(prop_etaria_md))


# ── SAVE ──────────────────────────────────────────────────────────────────────
print("\n── Saving ────────────────────────────────────────────────────────────")
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"✅  Done. Total cells: {len(cells)}")
