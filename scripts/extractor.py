import requests
import pandas as pd
from scripts.config import BASE_URL, API_KEY

def fetch_metabase_card(card_id, metric_name):
    if not BASE_URL or not API_KEY: return None
    url = f"{BASE_URL}/api/card/{card_id}/query/json"
    headers = {"Content-Type": "application/json", "X-API-Key": API_KEY}

    try:
        response = requests.post(url, headers=headers, timeout=60)
        data = response.json()
        if not data: return None
        df = pd.DataFrame(data)

        # 1. MAPEAMENTO DINÂMICO
        col_ies = next((c for c in df.columns if "Empresa" in c), None)
        col_perfil = next((c for c in df.columns if "Perfil" in c), None)
        col_status = next((c for c in df.columns if "Status" in c), None)
        
        # A coluna de valor é a que sobrar
        col_val = next((c for c in df.columns if c not in [col_ies, col_perfil, col_status]), None)

        # 2. LIMPEZA MATEMÁTICA INTELIGENTE
        def clean_numeric(val):
            if pd.isna(val): return 0
            # Se já for um número nativo do JSON (ex: 5.0 ou 100), devolve intacto
            if isinstance(val, (int, float)): return float(val)
            
            val_str = str(val).strip()
            
            if ',' in val_str:
                val_str = val_str.replace('.', '')   # Remove ponto de milhar
                val_str = val_str.replace(',', '.')  # Transforma vírgula em ponto decimal
            else:
                # Se tiver ponto, descobre se é milhar ("4.145") ou decimal ("5.0")
                if val_str.count('.') == 1:
                    parts = val_str.split('.')
                    if len(parts[1]) == 3: # Exatamente 3 casas após o ponto = Milhar
                        val_str = val_str.replace('.', '')
                elif val_str.count('.') > 1: # Vários pontos = Milhar
                    val_str = val_str.replace('.', '')
            
            try:
                return float(val_str)
            except:
                return 0

        df[col_val] = df[col_val].apply(clean_numeric)

        # 3. MONTAGEM DA TABELA
        new_df = pd.DataFrame()
        new_df['IES'] = df[col_ies].astype(str).str.strip()
        
        # TRATAMENTO PARA "ATIVOS E INATIVOS"
        if col_perfil and col_status:
            # Transforma true/false em Ativos/Inativos e junta ao Perfil
            status_map = {'true': 'Ativos', 'false': 'Inativos'}
            status_series = df[col_status].astype(str).str.lower().map(status_map).fillna('Outros')
            new_df['Perfil'] = status_series + " (" + df[col_perfil].astype(str).str.strip() + ")"
        elif col_perfil:
            new_df['Perfil'] = df[col_perfil].astype(str).str.strip()
            
        new_df[metric_name] = df[col_val]

        return new_df

    except Exception as e:
        print(f"❌ Erro no Card {card_id}: {e}")
        return None