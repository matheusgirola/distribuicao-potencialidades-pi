"""Redirecionamento: a versão canônica do mapeamento subclasse -> seção CNAE
fica em scripts/cnae_map.py (usada também pelo pipeline principal)."""
import importlib.util
from pathlib import Path

_arq = Path(__file__).resolve().parents[1] / 'scripts' / 'cnae_map.py'
_spec = importlib.util.spec_from_file_location('_cnae_map_canonico', _arq)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

SECOES, RULES, OVERRIDES = _mod.SECOES, _mod.RULES, _mod.OVERRIDES
norm, classify, secao = _mod.norm, _mod.classify, _mod.secao
