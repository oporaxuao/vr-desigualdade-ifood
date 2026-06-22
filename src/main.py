"""
processar_coleta.py
Processa os JSONs capturados manualmente do iFood e gera o CSV final.

Como usar:
1. Salve os JSONs do DevTools em data/raw/ (um por bairro)
2. Cole o cookie capturado do DevTools na variável COOKIE abaixo
3. Rode: python processar_coleta.py
"""

import json
import time
import requests
import pandas as pd
import os
os.chdir(r"C:\Users\xuao\PycharmProjects\IfoodProject")
import glob
from datetime import datetime




# ============================================================
# COLE SEU COOKIE AQUI (copiar do DevTools > Headers > cookie)
# ============================================================
COOKIE = "COLE_SEU_COOKIE_AQUI"

# ============================================================
# Mapeamento de bairros — complementa os dados dos JSONs
# Chave: trecho do nome do arquivo (lowercase)
# ============================================================
# ============================================================
# BAIRROS_INFO — 40 distritos do Mapa da Desigualdade 2024
# Quartil baseado na posicao do ranking consolidado Trabalho e Renda
# perfil: Q1=alto, Q2=medio_alto, Q3=medio, Q4=popular
# ============================================================
BAIRROS_INFO = {
    # ---------- Q1 ALTO ----------
    "butanta": {"zona": "Oeste", "perfil": "alto", "lat": -23.571, "lon": -46.708},
    "itaim_bibi": {"zona": "Oeste", "perfil": "alto", "lat": -23.585, "lon": -46.675},
    "jd_paulista": {"zona": "Oeste", "perfil": "alto", "lat": -23.5716, "lon": -46.6671},
    "pinheiros": {"zona": "Oeste", "perfil": "alto", "lat": -23.5629, "lon": -46.6908},
    "bela_vista": {"zona": "Centro", "perfil": "alto", "lat": -23.558, "lon": -46.648},
    "moema": {"zona": "Sul", "perfil": "alto", "lat": -23.6014, "lon": -46.665},
    "jabaquara": {"zona": "Sul", "perfil": "alto", "lat": -23.647, "lon": -46.641},
    "vila_mariana": {"zona": "Sul", "perfil": "alto", "lat": -23.5878, "lon": -46.6358},
    "alto_de_pinheiros": {"zona": "Oeste", "perfil": "alto", "lat": -23.5391, "lon": -46.7142},
    "campo_belo": {"zona": "Sul", "perfil": "alto", "lat": -23.62, "lon": -46.668},
    # ---------- Q2 MEDIO-ALTO ----------
    "perdizes": {"zona": "Oeste", "perfil": "medio_alto", "lat": -23.535, "lon": -46.67},
    "agua_rasa": {"zona": "Leste", "perfil": "medio_alto", "lat": -23.57, "lon": -46.56},
    "lapa": {"zona": "Oeste", "perfil": "medio_alto", "lat": -23.5259, "lon": -46.7008},
    "ipiranga": {"zona": "Sul", "perfil": "medio_alto", "lat": -23.59, "lon": -46.605},
    "mooca": {"zona": "Leste", "perfil": "medio_alto", "lat": -23.556, "lon": -46.597},
    "sapopemba": {"zona": "Leste", "perfil": "medio_alto", "lat": -23.602, "lon": -46.51},
    "sacoma": {"zona": "Sul", "perfil": "medio_alto", "lat": -23.605, "lon": -46.59},
    "vila_prudente": {"zona": "Leste", "perfil": "medio_alto", "lat": -23.585, "lon": -46.58},
    "cursino": {"zona": "Sul", "perfil": "medio_alto", "lat": -23.615, "lon": -46.628},
    "vila_sonia": {"zona": "Oeste", "perfil": "medio_alto", "lat": -23.5987, "lon": -46.7393},
    # ---------- Q3 MEDIO ----------
    "anhanguera": {"zona": "Norte", "perfil": "medio", "lat": -23.435, "lon": -46.79},
    "cidade_dutra": {"zona": "Sul", "perfil": "medio", "lat": -23.714, "lon": -46.6991},
    "tatuape": {"zona": "Leste", "perfil": "medio", "lat": -23.54, "lon": -46.576},
    "itaquera": {"zona": "Leste", "perfil": "medio", "lat": -23.535, "lon": -46.4459},
    "raposo_tavares": {"zona": "Oeste", "perfil": "medio", "lat": -23.585, "lon": -46.765},
    "jacana": {"zona": "Norte", "perfil": "medio", "lat": -23.463, "lon": -46.5824},
    "jardim_angela": {"zona": "Sul", "perfil": "medio", "lat": -23.69, "lon": -46.77},
    "penha": {"zona": "Leste", "perfil": "medio", "lat": -23.527, "lon": -46.542},
    "vila_andrade": {"zona": "Sul", "perfil": "medio", "lat": -23.6257, "lon": -46.727},
    "freguesia_do_o": {"zona": "Norte", "perfil": "medio", "lat": -23.4875, "lon": -46.6951},
    # ---------- Q4 POPULAR ----------
    "cidade_tiradentes": {"zona": "Leste", "perfil": "popular", "lat": -23.59, "lon": -46.399},
    "perus": {"zona": "Norte", "perfil": "popular", "lat": -23.405, "lon": -46.753},
    "capao_redondo": {"zona": "Sul", "perfil": "popular", "lat": -23.668, "lon": -46.78},
    "sao_mateus": {"zona": "Leste", "perfil": "popular", "lat": -23.608, "lon": -46.475},
    "pirituba": {"zona": "Norte", "perfil": "popular", "lat": -23.483, "lon": -46.725},
    "sao_miguel_paulista": {"zona": "Leste", "perfil": "popular", "lat": -23.498, "lon": -46.444},
    "campo_limpo": {"zona": "Sul", "perfil": "popular", "lat": -23.648, "lon": -46.758},
    "cangaiba": {"zona": "Leste", "perfil": "popular", "lat": -23.505, "lon": -46.53},
    "lajeado": {"zona": "Leste", "perfil": "popular", "lat": -23.556, "lon": -46.4},
    "grajau": {"zona": "Sul", "perfil": "popular", "lat": -23.76, "lon": -46.685},
}


PM_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.ifood.com.br",
    "referer": "https://www.ifood.com.br/restaurantes",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "cookie": COOKIE,
}


# ============================================================
# FUNÇÕES
# ============================================================

def identificar_bairro(nome_arquivo: str) -> tuple[str, dict]:
    """Tenta identificar o bairro pelo nome do arquivo."""
    base = os.path.basename(nome_arquivo).lower().replace(".json", "")
    # remove acentos simples
    base = (base.replace("ã", "a").replace("â", "a").replace("á", "a")
                .replace("é", "e").replace("ê", "e")
                .replace("ó", "o").replace("ô", "o")
                .replace("ú", "u").replace("ç", "c"))
    base = "".join(c if c.isalnum() else "_" for c in base).strip("_")

    # match exato primeiro
    if base in BAIRROS_INFO:
        return base.replace("_", " ").title(), BAIRROS_INFO[base]
    # depois match parcial, priorizando chaves mais longas
    for chave in sorted(BAIRROS_INFO, key=len, reverse=True):
        if chave in base or base in chave:
            return chave.replace("_", " ").title(), BAIRROS_INFO[chave]
    # fallback: usa o nome do arquivo como bairro
    return base.replace("_", " ").title(), {
        "zona": "Desconhecida", "perfil": "desconhecido",
        "lat": 0.0, "lon": 0.0
    }


def extrair_merchants_do_json(data: dict) -> list[dict]:
    """Extrai lista de restaurantes do JSON do home."""
    merchants = []
    ids_vistos = set()

    for section in data.get("sections", []):
        for card in section.get("cards", []):
            if card.get("cardType") in ("MERCHANT_LIST_V2", "MERCHANT_LIST"):
                for item in card.get("data", {}).get("contents", []):
                    mid = item.get("id")
                    if mid and mid not in ids_vistos:
                        ids_vistos.add(mid)
                        merchants.append(item)

    return merchants


def get_payment_methods(merchant_id: str) -> list[dict]:
    """Busca métodos de pagamento via API (já validado)."""
    try:
        r = requests.get(
            f"https://marketplace.ifood.com.br/v1/merchants/{merchant_id}/payment-methods",
            headers=PM_HEADERS,
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()
        if r.status_code == 401:
            print("\n⚠ Cookie expirado! Atualize o COOKIE no script e rode novamente.")
    except Exception as e:
        print(f"  Erro ao buscar {merchant_id}: {e}")
    return []


def classificar_vr(payments: list[dict]) -> dict:
    """Identifica bandeiras de VR aceitas."""
    bandeiras = list(set([
        pm.get("brand", {}).get("name", "")
        for pm in payments
        if pm.get("method", {}).get("name") == "MEAL_VOUCHER"
    ]))
    return {
        "aceita_alelo":            "ALELO" in bandeiras,
        "aceita_sodexo":           "SODEXO" in bandeiras,
        "aceita_vr":               "VR" in bandeiras,
        "aceita_ticket":           any("TICKET" in b for b in bandeiras),
        "aceita_caju":             "CAJU" in bandeiras,
        "aceita_ifood_beneficios": "IFOOD_MEAL_VOUCHER" in bandeiras,
        "aceita_ben":              "BEN_MEAL_VOUCHER" in bandeiras,
        "aceita_qualquer_vr":      len(bandeiras) > 0,
        "bandeiras_vr_raw":        json.dumps(sorted(bandeiras)),
        "qtd_bandeiras_vr":        len(bandeiras),
    }


# ============================================================
# PROCESSAMENTO PRINCIPAL
# ============================================================

def processar_todos():
    os.makedirs("data/processed", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # Encontra todos os JSONs em data/raw/
    arquivos = glob.glob("data/raw/*.json")
    if not arquivos:
        print("Nenhum arquivo JSON encontrado em data/raw/")
        print("Salve os JSONs do DevTools lá e rode novamente.")
        return

    print(f"Arquivos encontrados: {len(arquivos)}")
    for a in arquivos:
        print(f"  {a}")
    print()

    todos_registros = []


    for arquivo in sorted(arquivos):
        nome_bairro, info_bairro = identificar_bairro(arquivo)
        print(f"\n{'='*50}")
        print(f"Processando: {nome_bairro} ({arquivo})")

        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        merchants = extrair_merchants_do_json(data)
        print(f"  Restaurantes no JSON: {len(merchants)}")

        registros_bairro = []
        ids_distrito = set()
        for i, m in enumerate(merchants):
            mid = m.get("id")
            if not mid or mid in ids_distrito:
                continue
            ids_distrito.add(mid)

            time.sleep(0.35)
            payments = get_payment_methods(mid)
            vr = classificar_vr(payments)
            delivery = m.get("deliveryInfo", {})

            registros_bairro.append({
                "id":                   mid,
                "nome":                 m.get("name"),
                "categoria":            m.get("mainCategory"),
                "nota":                 m.get("userRating"),
                "distancia_km":         m.get("distance"),
                "taxa_entrega_reais":   (delivery.get("fee") or 0) / 100,
                "tempo_min":            delivery.get("timeMinMinutes"),
                "tempo_max":            delivery.get("timeMaxMinutes"),
                "is_super_restaurante": m.get("isSuperRestaurant", False),
                "bairro_busca":         nome_bairro,
                "zona":                 info_bairro["zona"],
                "perfil":               info_bairro["perfil"],
                "lat_busca":            info_bairro["lat"],
                "lon_busca":            info_bairro["lon"],
                "data_coleta":          datetime.now().strftime("%Y-%m-%d %H:%M"),
                **vr,
            })

            if (i + 1) % 5 == 0:
                print(f"    {i+1}/{len(merchants)} processados...")

        aceita_vr = sum(r["aceita_qualquer_vr"] for r in registros_bairro)
        print(f"  Registros gerados: {len(registros_bairro)}")
        print(f"  Aceita algum VR:   {aceita_vr}/{len(registros_bairro)} ({aceita_vr/max(len(registros_bairro),1)*100:.0f}%)")

        todos_registros.extend(registros_bairro)

    # Gera CSV final
    df = pd.DataFrame(todos_registros)
    csv_path = f"data/processed/restaurantes_{timestamp}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"\n{'='*50}")
    print(f"COLETA CONCLUÍDA")
    print(f"Total de restaurantes: {len(df)}")
    print(f"Aceita algum VR:       {df['aceita_qualquer_vr'].mean()*100:.1f}%")
    print(f"Aceita Alelo:          {df['aceita_alelo'].mean()*100:.1f}%")
    print(f"Aceita Sodexo:         {df['aceita_sodexo'].mean()*100:.1f}%")
    print(f"Aceita VR:             {df['aceita_vr'].mean()*100:.1f}%")
    print(f"CSV salvo em:          {csv_path}")

    return df

if __name__ == "__main__":
    processar_todos()