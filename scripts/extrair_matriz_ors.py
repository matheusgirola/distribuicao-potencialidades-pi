# -*- coding: utf-8 -*-
"""
extrair_matriz_ors.py 
-----------------------------------------------------
Extrai a matriz 224x224 de TEMPOS DE VIAGEM (s) e DISTANCIAS RODOVIARIAS (m)
entre as SEDES dos municipios do Piaui via Matrix API do OpenRouteService.

COMO USAR
  1) Chave gratuita em https://openrouteservice.org  ->  ORS_API_KEY
  2) pip install geopandas requests
  3) Ajuste SEDES_PATH (e SHP_PATH) abaixo e rode: python extrair_matriz_ors.py;
  se não tiver o arquivos de sede, o script dá um fallback e usa centroides
"""
import os, sys, time
import numpy as np
import requests
import geopandas as gpd
import comum as C

# ----------------------------- CONFIG ---------------------------------------
API_KEY   = os.environ.get("ORS_API_KEY")   # defina a variavel de ambiente; nunca grave a chave no codigo
SHP_PATH  = str(C.SHP)   # malha municipal IBGE (sempre necessaria:
                                       # define a ORDEM dos 224 municipios)

# >>> AQUI: arquivo de sedes baixado do IBGE <<<
# Aceita .shp, .gpkg (camada de pontos) ou .csv com colunas de coordenadas.
# Exemplos: "PI_Localidades_2025.shp" | "sedes_municipais.gpkg" | "sedes.csv"
SEDES_PATH = str(C.SEDES)
# Se for CSV, informe os nomes das colunas de longitude/latitude (graus, SIRGAS2000):
CSV_LON, CSV_LAT = "longitude", "latitude"

PROFILE   = "driving-car"
URL       = f"https://api.openrouteservice.org/v2/matrix/{PROFILE}"
MAX_ROUTES   = 3500          # rotas (origens x destinos) por requisicao no plano free
RATE_SLEEP   = 2.0
MAX_RETRIES  = 6
CHECKPOINT   = str(C.DADOS / "ors_progresso.npz")
OUT_DUR      = str(C.CSV_ORS_DURACAO)
OUT_DIST     = str(C.CSV_ORS_DISTANCIA)
# -----------------------------------------------------------------------------

import unicodedata, re
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z0-9]+", " ", s).strip()

def achar_coluna(df, candidatos):
    """Retorna a primeira coluna existente dentre as candidatas (case-insensitive)."""
    low = {c.lower(): c for c in df.columns}
    for c in candidatos:
        if c.lower() in low: return low[c.lower()]
    return None

def carregar_malha(shp_path):
    gdf = gpd.read_file(shp_path)
    if "NM_MUN" not in gdf.columns:
        sys.exit("Malha sem coluna NM_MUN — confira o shapefile do IBGE.")
    gdf["mun_norm"] = gdf["NM_MUN"].map(norm)
    gdf = gdf.sort_values("mun_norm").reset_index(drop=True)  # ordem canonica do projeto
    return gdf

def carregar_sedes(gdf_malha):
    """Devolve coords [lon,lat] na ordem canonica, a partir do arquivo de sedes."""
    ext = os.path.splitext(SEDES_PATH)[1].lower()
    cod_col_malha = achar_coluna(gdf_malha, ["CD_MUN", "CD_GEOCMU", "CD_GEOCODMU"])

    if ext == ".csv":
        import pandas as pd
        try:
            sed = pd.read_csv(SEDES_PATH, sep=None, engine="python", decimal=",")
        except Exception:
            sed = pd.read_csv(SEDES_PATH)
        # Não sabe a estrutura da malha, tentou várias opções
        lon_c = achar_coluna(sed, [CSV_LON, "lon", "long", "longitude", "x"])
        lat_c = achar_coluna(sed, [CSV_LAT, "lat", "latitude", "y"])
        if not lon_c or not lat_c:
            sys.exit(f"CSV sem colunas de coordenadas reconheciveis ({list(sed.columns)}).")
        sed["_lon"] = pd.to_numeric(sed[lon_c].astype(str).str.replace(",", "."), errors="coerce")
        sed["_lat"] = pd.to_numeric(sed[lat_c].astype(str).str.replace(",", "."), errors="coerce")
    else:
        sed = gpd.read_file(SEDES_PATH)
        if sed.crs is None:
            print("AVISO: sedes sem CRS declarado; assumindo EPSG:4674 (SIRGAS 2000).")
            sed = sed.set_crs(4674)
        sed = sed.to_crs(4326)
        # se vier poligono (area urbanizada), usa ponto representativo
        # ponto representativo é garantido em cair dentro da shape, diferente de um centroide
        if not sed.geom_type.str.contains("Point").all():
            sed["geometry"] = sed.representative_point()
        sed["_lon"] = sed.geometry.x
        sed["_lat"] = sed.geometry.y

    # arquivos de LOCALIDADES trazem cidades, vilas e povoados: filtra a SEDE (cidade)
    cat = achar_coluna(sed, ["NM_CATEGOR", "TIPO", "CATEGORIA", "NM_CATEG"])
    if cat is not None:
        vals = sed[cat].astype(str).str.upper()
        if vals.str.contains("CIDADE").any():
            antes = len(sed); sed = sed[vals.str.contains("CIDADE")]
            print(f"Filtro de categoria '{cat}'==CIDADE: {antes} -> {len(sed)} registros.")

    # 1) tenta casar por codigo IBGE de 7 digitos
    cod_col = achar_coluna(sed, ["CD_MUN", "CD_GEOCMU", "CD_GEOCODMU", "GEOCODIGO", "COD_MUN"])
    coords = None
    if cod_col and cod_col_malha:
        sed["_cd"] = sed[cod_col].astype(str).str.extract(r"(\d{7})")[0]
        m = dict(zip(sed["_cd"], zip(sed["_lon"], sed["_lat"])))
        cds = gdf_malha[cod_col_malha].astype(str).str.extract(r"(\d{7})")[0]
        if cds.map(m).notna().all():
            coords = [list(m[c]) for c in cds]
            print(f"Sedes casadas por codigo IBGE ({cod_col}).")
    # 2) fallback: casa por nome normalizado
    if coords is None:
        nome_col = achar_coluna(sed, ["NM_MUN", "NM_MUNICIP", "NOME", "NM_LOCALID", "MUNICIPIO"])
        if not nome_col:
            sys.exit(f"Nao encontrei coluna de codigo nem de nome nas sedes ({list(sed.columns)}).")
        sed["_nm"] = sed[nome_col].map(norm)
        sed = sed.drop_duplicates("_nm")
        m = dict(zip(sed["_nm"], zip(sed["_lon"], sed["_lat"])))
        faltam = [x for x in gdf_malha["mun_norm"] if x not in m]
        if faltam:
            sys.exit(f"{len(faltam)} municipios sem sede no arquivo (ex.: {faltam[:5]}). "
                     "Verifique se o arquivo cobre o PI inteiro e a categoria CIDADE.")
        coords = [list(m[x]) for x in gdf_malha["mun_norm"]]
        print(f"Sedes casadas por nome ({nome_col}).")

    # sanidade: sede deve cair dentro (ou muito perto) do proprio municipio
    from shapely.geometry import Point
    dentro = sum(gdf_malha.geometry.iloc[i].buffer(0.05).contains(Point(*coords[i]))
                 for i in range(len(coords)))
    print(f"Sanidade: {dentro}/{len(coords)} sedes dentro do proprio municipio (tolerancia ~5 km).")
    if dentro < len(coords) - 5:
        print("AVISO: muitas sedes fora do municipio esperado — confira lon/lat "
              "(ordem das colunas?) antes de gastar quota da API.")
    return coords

def carregar_centroides(gdf_malha):
    # Eu acho que ele fez isso pois não tem certeza da projeção da malha que vai receber
    # sabe somente que é do Brasil
    cent = gdf_malha.to_crs(5880).geometry.centroid.to_crs(4326)
    return [[float(p.x), float(p.y)] for p in cent]

def chamada_ors(sess, coords, fontes_idx):
    body = {"locations": coords, "sources": fontes_idx,
            "destinations": list(range(len(coords))),
            "metrics": ["duration", "distance"], "units": "m"}
    for tent in range(MAX_RETRIES):
        r = sess.post(URL, json=body, timeout=120)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            espera = float(r.headers.get("Retry-After") or min(2 ** tent * 5, 120))
            print(f"  HTTP {r.status_code} — aguardando {espera:.0f}s "
                  f"(tentativa {tent+1}/{MAX_RETRIES})")
            time.sleep(espera); continue
        sys.exit(f"Erro HTTP {r.status_code}: {r.text[:400]}\n"
                 "Se for limite diario, rode novamente amanha — o progresso fica salvo.")
    sys.exit("Falhas repetidas na API; tente mais tarde (progresso salvo).")

def main():
    if API_KEY == "COLE_SUA_CHAVE_AQUI":
        sys.exit("Defina ORS_API_KEY ou edite API_KEY no script.")
    malha = carregar_malha(SHP_PATH)
    nomes = malha["NM_MUN"].tolist()
    if SEDES_PATH:
        print(f"Usando SEDES de: {SEDES_PATH}")
        coords = carregar_sedes(malha)
    else:
        print("SEDES_PATH vazio — usando centroides dos poligonos.")
        coords = carregar_centroides(malha)
    n = len(coords)
    print(f"{n} municipios prontos.")

    bloco = max(1, MAX_ROUTES // n)
    blocos = [list(range(i, min(i + bloco, n))) for i in range(0, n, bloco)]
    print(f"{len(blocos)} chamadas de ate {bloco} origens x {n} destinos.")

    if os.path.exists(CHECKPOINT):
        ck = np.load(CHECKPOINT)
        dur, dist, feito = ck["dur"], ck["dist"], ck["feito"]
        print(f"Checkpoint: {int(feito.sum())}/{len(blocos)} blocos ja concluidos.")
    else:
        dur  = np.full((n, n), np.nan); dist = np.full((n, n), np.nan)
        feito = np.zeros(len(blocos), dtype=bool)

    sess = requests.Session()
    sess.headers.update({"Authorization": API_KEY,
                         "Content-Type": "application/json; charset=utf-8"})
    for k, fontes in enumerate(blocos):
        if feito[k]: continue
        print(f"Bloco {k+1}/{len(blocos)} (origens {fontes[0]}–{fontes[-1]})…")
        js = chamada_ors(sess, coords, fontes)
        dur[fontes, :]  = np.array(js["durations"], dtype=float)
        dist[fontes, :] = np.array(js["distances"], dtype=float)
        feito[k] = True
        np.savez_compressed(CHECKPOINT, dur=dur, dist=dist, feito=feito)
        time.sleep(RATE_SLEEP)

    off = ~np.eye(n, dtype=bool)
    n_nan = int(np.isnan(dur[off]).sum())
    print(f"\nConcluido. Pares sem rota: {n_nan} de {off.sum()}")
    if not np.isnan(dur[off]).all():
        print(f"Tempo mediano entre sedes: {np.nanmedian(dur[off])/60:.0f} min | "
              f"maximo: {np.nanmax(dur[off])/3600:.1f} h | "
              f"distancia mediana: {np.nanmedian(dist[off])/1000:.0f} km")

    import csv
    def exportar(mat, caminho):
        with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["NM_MUN"] + nomes)
            for i, nome in enumerate(nomes):
                w.writerow([nome] + [("" if np.isnan(x) else f"{x:.1f}".replace(".", ","))
                                     for x in mat[i]])
    exportar(dur, OUT_DUR); exportar(dist, OUT_DIST)
    print(f"Gravados: {OUT_DUR} e {OUT_DIST}.")

if __name__ == "__main__":
    main()