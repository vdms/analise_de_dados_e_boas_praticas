"""
apply_refactor_harmonizacao.py
------------------------------
Refactors construir_base_harmonizada(): extracts the two column-mapping
dicts as named constants and reduces the function body to ~20 lines.
Logic is identical — fingerprint validates correctness.
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

# Find the cell with the function
target_idx = None
for i, c in enumerate(cells):
    if "def construir_base_harmonizada(" in src(c):
        target_idx = i
        break

if target_idx is None:
    raise ValueError("construir_base_harmonizada not found")

print(f"Found at cell index {target_idx}")

# ── New cell source ────────────────────────────────────────────────────────────
new_source = """\
# Padronizar nomes analíticos para sexo e faixa etária comparáveis

# Mapeamento: nome analítico padronizado → nome original no CSV 2000/2010
MAPA_HARM_2000_2010 = {
    "alf_m_15_19": "15_a_19_anos_sexo_masculino_alfabetizada",
    "alf_f_15_19": "15_a_19_anos_sexo_feminino_alfabetizada",
    "alf_m_20_24": "20_a_24_anos_sexo_masculino_alfabetizada",
    "alf_f_20_24": "20_a_24_anos_sexo_feminino_alfabetizada",
    "alf_m_25_29": "25_a_29_anos_sexo_masculino_alfabetizada",
    "alf_f_25_29": "25_a_29_anos_sexo_feminino_alfabetizada",
    "alf_m_30_34": "30_a_34_anos_sexo_masculino_alfabetizada",
    "alf_f_30_34": "30_a_34_anos_sexo_feminino_alfabetizada",
    "alf_m_35_39": "35_a_39_anos_sexo_masculino_alfabetizada",
    "alf_f_35_39": "35_a_39_anos_sexo_feminino_alfabetizada",
    "alf_m_40_44": "40_a_44_anos_sexo_masculino_alfabetizada",
    "alf_f_40_44": "40_a_44_anos_sexo_feminino_alfabetizada",
    "alf_m_45_49": "45_a_49_anos_sexo_masculino_alfabetizada",
    "alf_f_45_49": "45_a_49_anos_sexo_feminino_alfabetizada",
    "alf_m_50_54": "50_a_54_anos_sexo_masculino_alfabetizada",
    "alf_f_50_54": "50_a_54_anos_sexo_feminino_alfabetizada",
    "alf_m_55_59": "55_a_59_anos_sexo_masculino_alfabetizada",
    "alf_f_55_59": "55_a_59_anos_sexo_feminino_alfabetizada",
    "alf_m_60_64": "60_a_64_anos_sexo_masculino_alfabetizada",
    "alf_f_60_64": "60_a_64_anos_sexo_feminino_alfabetizada",
    "alf_m_65_69": "65_a_69_anos_sexo_masculino_alfabetizada",
    "alf_f_65_69": "65_a_69_anos_sexo_feminino_alfabetizada",
    "alf_m_80_mais": "80_anos_ou_mais_sexo_masculino_alfabetizada",
    "alf_f_80_mais": "80_anos_ou_mais_sexo_feminino_alfabetizada",
}

# Mapeamento: nome analítico padronizado → nome original no CSV 2022
MAPA_HARM_2022 = {
    "alf_m_15_19": "pessoas_alfabetizadas_sexo_masculino_15_a_19_anos",
    "alf_f_15_19": "pessoas_alfabetizadas_sexo_feminino_15_a_19_anos",
    "alf_m_20_24": "pessoas_alfabetizadas_sexo_masculino_20_a_24_anos",
    "alf_f_20_24": "pessoas_alfabetizadas_sexo_feminino_20_a_24_anos",
    "alf_m_25_29": "pessoas_alfabetizadas_sexo_masculino_25_a_29_anos",
    "alf_f_25_29": "pessoas_alfabetizadas_sexo_feminino_25_a_29_anos",
    "alf_m_30_34": "pessoas_alfabetizadas_sexo_masculino_30_a_34_anos",
    "alf_f_30_34": "pessoas_alfabetizadas_sexo_feminino_30_a_34_anos",
    "alf_m_35_39": "pessoas_alfabetizadas_sexo_masculino_35_a_39_anos",
    "alf_f_35_39": "pessoas_alfabetizadas_sexo_feminino_35_a_39_anos",
    "alf_m_40_44": "pessoas_alfabetizadas_sexo_masculino_40_a_44_anos",
    "alf_f_40_44": "pessoas_alfabetizadas_sexo_feminino_40_a_44_anos",
    "alf_m_45_49": "pessoas_alfabetizadas_sexo_masculino_45_a_49_anos",
    "alf_f_45_49": "pessoas_alfabetizadas_sexo_feminino_45_a_49_anos",
    "alf_m_50_54": "pessoas_alfabetizadas_sexo_masculino_50_a_54_anos",
    "alf_f_50_54": "pessoas_alfabetizadas_sexo_feminino_50_a_54_anos",
    "alf_m_55_59": "pessoas_alfabetizadas_sexo_masculino_55_a_59_anos",
    "alf_f_55_59": "pessoas_alfabetizadas_sexo_feminino_55_a_59_anos",
    "alf_m_60_64": "pessoas_alfabetizadas_sexo_masculino_60_a_64_anos",
    "alf_f_60_64": "pessoas_alfabetizadas_sexo_feminino_60_a_64_anos",
    "alf_m_65_69": "pessoas_alfabetizadas_sexo_masculino_65_a_69_anos",
    "alf_f_65_69": "pessoas_alfabetizadas_sexo_feminino_65_a_69_anos",
    "alf_m_70_79": "pessoas_alfabetizadas_sexo_masculino_70_a_79_anos",
    "alf_f_70_79": "pessoas_alfabetizadas_sexo_feminino_70_a_79_anos",
    "alf_m_80_mais": "pessoas_alfabetizadas_sexo_masculino_80_anos_ou_mais",
    "alf_f_80_mais": "pessoas_alfabetizadas_sexo_feminino_80_anos_ou_mais",
}

# Ordem padronizada das colunas na base harmonizada
ORDEM_FINAL_HARM = [
    "bairro", "codbnum", "ano",
    "alf_m_15_19", "alf_f_15_19",
    "alf_m_20_24", "alf_f_20_24",
    "alf_m_25_29", "alf_f_25_29",
    "alf_m_30_34", "alf_f_30_34",
    "alf_m_35_39", "alf_f_35_39",
    "alf_m_40_44", "alf_f_40_44",
    "alf_m_45_49", "alf_f_45_49",
    "alf_m_50_54", "alf_f_50_54",
    "alf_m_55_59", "alf_f_55_59",
    "alf_m_60_64", "alf_f_60_64",
    "alf_m_65_69", "alf_f_65_69",
    "alf_m_70_79", "alf_f_70_79",
    "alf_m_80_mais", "alf_f_80_mais",
]


def construir_base_harmonizada(df, ano):
    \"\"\"Aplica mapa de harmonização etária e retorna base comparável entre os três anos.\"\"\"
    base = df[["bairro", "codbnum", "ano"]].copy()
    mapa = MAPA_HARM_2000_2010 if ano in [2000, 2010] else MAPA_HARM_2022

    for nova, antiga in mapa.items():
        base[nova] = df[antiga]

    # 2000/2010: faixas 70–74 e 75–79 são colunas separadas — agrega para comparabilidade com 2022
    if ano in [2000, 2010]:
        base["alf_m_70_79"] = (
            df["70_a_74_anos_sexo_masculino_alfabetizada"] +
            df["75_a_79_anos_sexo_masculino_alfabetizada"]
        )
        base["alf_f_70_79"] = (
            df["70_a_74_anos_sexo_feminino_alfabetizada"] +
            df["75_a_79_anos_sexo_feminino_alfabetizada"]
        )

    return base[ORDEM_FINAL_HARM]\
"""

cells[target_idx]["source"] = new_source
print(f"✅ Cell {target_idx} replaced. New length: {len(new_source.splitlines())} lines")

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("✅ Saved.")
