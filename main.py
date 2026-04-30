import os
from datetime import datetime
from dotenv import load_dotenv
from scripts.config import CARDS_CONFIG
from scripts.extractor import fetch_metabase_card
from scripts.processor import processar_dados_consolidados
from scripts.loader import exportar_para_sheets  # <-- Liberado!

load_dotenv()

def main():
    start_time = datetime.now()
    print(f"🚀 [START] Iniciando pipeline: {start_time.strftime('%H:%M:%S')}")

    # Configurações do Google extraídas do .env
    SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID") 
    JSON_CREDS = "credenciais.json" 

    dfs_extraidos = []

    # --- ETAPA 1: EXTRAÇÃO ---
    for card_id, metric_name in CARDS_CONFIG.items():
        print(f"🔎 Extraindo Card {card_id}: {metric_name}...")
        df = fetch_metabase_card(card_id, metric_name)
        if df is not None:
            dfs_extraidos.append(df)

    if not dfs_extraidos:
        print("❌ ERRO: Nenhum dado extraído dos cards.")
        return

    # --- ETAPA 2: TRANSFORMAÇÃO ---
    print("⚙️  Processando e unificando dados...")
    df_final = processar_dados_consolidados(dfs_extraidos)

    # Ordenação: IES primeiro, o resto em ordem alfabética para facilitar o CORRESP do Sheets
    cols = ['IES'] + sorted([c for c in df_final.columns if c != 'IES'])
    df_final = df_final[cols]

    # --- ETAPA 3: CARGA LOCAL (Backup) ---
    df_final.to_excel("relatorio_final_bi.xlsx", index=False)
    print("💾 Backup local 'relatorio_final_bi.xlsx' gerado.")

    # --- ETAPA 4: CARGA NUVEM (Google Sheets) ---
    if SPREADSHEET_ID and os.path.exists(JSON_CREDS):
        exportar_para_sheets(df_final, SPREADSHEET_ID, JSON_CREDS)
    else:
        print("⚠️  PULO: GOOGLE_SHEETS_ID não configurado ou credenciais.json ausente.")

    end_time = datetime.now()
    print(f"🏁 [FINISH] Tempo total: {end_time - start_time}")

if __name__ == "__main__":
    main()

    #teste