# ===================== config_loader.py =====================
# le o config.txt no formato KEY=VALOR e devolve dict[str,str]
# ============================================================

import os
import sys


def load_config(path: str = None) -> dict:
    # se não fornecido path via argumento, assume ../config.txt em relação a este arquivo
    if path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "..", "config.txt")
    path = os.path.abspath(path)

    cfg: dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):   # ignora comentarios e linhas em branco
                continue
            if "=" not in line:                    # linha sem '=' tambem nao serve
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg


# ------------------------------------------------------------
# getters tipados — se o valor for inválido, avisa no stderr
# e usa um fallback do default em vez de quebrar
# ------------------------------------------------------------

def get_int(cfg: dict, key: str, default: int) -> int:
    try:
        return int(cfg.get(key, default))
    except ValueError:
        sys.stderr.write(f"[config] {key} invalido, usando default={default}\n")
        return default


def get_float(cfg: dict, key: str, default: float) -> float:
    try:
        return float(cfg.get(key, default))
    except ValueError:
        sys.stderr.write(f"[config] {key} invalido, usando default={default}\n")
        return default


def get_str(cfg: dict, key: str, default: str) -> str:
    return cfg.get(key, default)
