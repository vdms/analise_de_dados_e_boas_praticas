"""
fingerprint.py
--------------
Extrai todos os outputs de texto/tabela do notebook e gera um JSON com:
  - hash SHA-256 de cada célula com output
  - texto bruto dos outputs (stdout, text/plain, text/html resumido)

Uso:
  python scripts/fingerprint.py                     # gera fingerprint atual
  python scripts/fingerprint.py --compare base.json # compara com baseline

Arquivos gerados em scripts/fingerprints/
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

NOTEBOOK = Path(__file__).parent.parent / "data_analysis_and_good_practices.ipynb"
OUTPUT_DIR = Path(__file__).parent / "fingerprints"


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_text_from_output(output: dict) -> str:
    """Retorna o conteúdo textual de um output de célula."""
    out_type = output.get("output_type", "")

    if out_type in ("stream",):
        return "".join(output.get("text", []))

    if out_type in ("execute_result", "display_data"):
        data = output.get("data", {})
        # Preferência: text/plain (números puros), depois text/html (tabelas)
        if "text/plain" in data:
            return "".join(data["text/plain"])
        if "text/html" in data:
            # Remove tags HTML para comparação limpa de valores
            raw = "".join(data["text/html"])
            return re.sub(r"<[^>]+>", " ", raw)

    if out_type == "error":
        return f"ERROR: {output.get('ename','')}: {output.get('evalue','')}"

    return ""


def cell_fingerprint(cell_index: int, cell: dict) -> dict | None:
    """Gera fingerprint de uma célula com outputs não-vazios."""
    outputs = cell.get("outputs", [])
    if not outputs:
        return None

    texts = [extract_text_from_output(o) for o in outputs]
    combined = "\n---\n".join(t for t in texts if t.strip())

    if not combined.strip():
        return None

    sha = hashlib.sha256(combined.encode()).hexdigest()[:16]

    # Extrai números do texto para diff rápido
    numbers = re.findall(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", combined)

    return {
        "cell_index": cell_index,
        "cell_type": cell.get("cell_type", ""),
        "source_preview": "".join(cell.get("source", []))[:120].replace("\n", " "),
        "output_sha": sha,
        "numeric_values": numbers[:50],  # cap para legibilidade
        "output_text_preview": combined[:300],
    }


def build_fingerprint(notebook_path: Path) -> dict:
    """Lê o notebook e constrói o fingerprint completo."""
    with open(notebook_path, encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    entries = []

    for i, cell in enumerate(cells):
        fp = cell_fingerprint(i, cell)
        if fp:
            entries.append(fp)

    global_text = json.dumps([e["output_sha"] for e in entries], sort_keys=True)
    global_sha = hashlib.sha256(global_text.encode()).hexdigest()[:16]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "notebook": str(notebook_path.name),
        "total_cells_with_output": len(entries),
        "global_sha": global_sha,
        "cells": entries,
    }


# ── Comparação ────────────────────────────────────────────────────────────────

def compare(baseline: dict, current: dict) -> bool:
    """
    Compara dois fingerprints. Imprime diferenças e retorna True se idênticos.
    """
    ok = True

    # Global hash rápido
    if baseline["global_sha"] == current["global_sha"]:
        print(f"✅  Global SHA match: {current['global_sha']} — outputs idênticos.")
        return True

    print(f"⚠️  Global SHA diferente. Baseline: {baseline['global_sha']}  "
          f"Current: {current['global_sha']}\n")

    base_map = {e["cell_index"]: e for e in baseline["cells"]}
    curr_map = {e["cell_index"]: e for e in current["cells"]}

    all_indices = sorted(set(base_map) | set(curr_map))

    for idx in all_indices:
        b = base_map.get(idx)
        c = curr_map.get(idx)

        if b is None:
            print(f"  ➕ Célula {idx:3d} NOVA output: {c['source_preview'][:80]}")
            continue

        if c is None:
            print(f"  ➖ Célula {idx:3d} REMOVIDA: {b['source_preview'][:80]}")
            ok = False
            continue

        if b["output_sha"] != c["output_sha"]:
            print(f"  ❌ Célula {idx:3d} SHA mudou: {b['output_sha']} → {c['output_sha']}")
            print(f"       Código: {b['source_preview'][:80]}")

            # Diff numérico rápido
            b_nums = set(b["numeric_values"])
            c_nums = set(c["numeric_values"])
            lost = b_nums - c_nums
            gained = c_nums - b_nums
            if lost:
                print(f"       Valores removidos: {sorted(lost)[:10]}")
            if gained:
                print(f"       Valores adicionados: {sorted(gained)[:10]}")
            ok = False

    return ok


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fingerprint de outputs do notebook")
    parser.add_argument(
        "--compare", metavar="BASELINE_JSON",
        help="Compara com um fingerprint anterior (caminho relativo a scripts/fingerprints/)"
    )
    parser.add_argument(
        "--output", metavar="FILENAME",
        help="Nome do arquivo de saída (padrão: fingerprint_<timestamp>.json)"
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Lendo: {NOTEBOOK}")
    current = build_fingerprint(NOTEBOOK)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = args.output or f"fingerprint_{timestamp}.json"
    out_path = OUTPUT_DIR / out_name

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)

    print(f"Cells com output: {current['total_cells_with_output']}")
    print(f"Global SHA:       {current['global_sha']}")
    print(f"Salvo em:         {out_path}\n")

    if args.compare:
        baseline_path = OUTPUT_DIR / args.compare
        if not baseline_path.exists():
            print(f"Erro: baseline não encontrado em {baseline_path}", file=sys.stderr)
            sys.exit(1)
        with open(baseline_path, encoding="utf-8") as f:
            baseline = json.load(f)
        ok = compare(baseline, current)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
