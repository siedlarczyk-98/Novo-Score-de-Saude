import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from scripts.config import CARDS_CONFIG
from scripts.extractor import fetch_metabase_card
from scripts.processor import processar_dados_consolidados
from scripts.loader import exportar_para_sheets, escrever_log_dashboard

load_dotenv()

def main():
    # Já declaro o fuso horário aqui em cima pra usar no código todo
    fuso_sp = timezone(timedelta(hours=-3))
    start_time = datetime.now(fuso_sp)
    
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

    # ==========================================
    # 🚨 DEBUG ETAPA 1: O QUE CHEGOU DO METABASE?
    # ==========================================
    print(f"\n📦 DEBUG: Total de DataFrames extraídos: {len(dfs_extraidos)}")
    for i, df in enumerate(dfs_extraidos):
        print(f"   -> DF {i} | Colunas ({len(df.columns)}): {list(df.columns)}")
    print("\n")

    # --- ETAPA 2: TRANSFORMAÇÃO ---
    print("⚙️  Processando e unificando dados...")
    df_final = processar_dados_consolidados(dfs_extraidos)

    # Ordenação das colunas
    cols = ['IES'] + sorted([c for c in df_final.columns if c != 'IES'])
    df_final = df_final[cols]

    # ==========================================
    # 🚨 DEBUG ETAPA 2: O QUE O PROCESSADOR CUSPIU?
    # ==========================================
    print(f"\n📊 DEBUG FINAL: Total de Colunas prontas para o Sheets ({len(df_final.columns)}): {list(df_final.columns)}\n")

    # --- ETAPA 3: CARGA LOCAL (Backup) ---
    df_final.to_excel("relatorio_final_bi.xlsx", index=False)
    print("💾 Backup local 'relatorio_final_bi.xlsx' gerado.")

    # --- ETAPA 4: CARGA NUVEM E LOG ---
    if SPREADSHEET_ID and os.path.exists(JSON_CREDS):
        # 1. Envia os dados para a aba de input
        exportar_para_sheets(df_final, SPREADSHEET_ID, JSON_CREDS)
        
        agora = datetime.now(fuso_sp).strftime('%d/%m/%Y %H:%M:%S')
        mensagem_log = f"Última atualização: {agora}"
        
        escrever_log_dashboard(
            spreadsheet_id=SPREADSHEET_ID,
            json_path=JSON_CREDS,
            aba_nome="Métricas Novas",  
            celula="Q20",
            texto=mensagem_log
        )
    else:
        print("⚠️  PULO: GOOGLE_SHEETS_ID não configurado ou credenciais.json ausente.")

    end_time = datetime.now(fuso_sp)
    print(f"🏁 [FINISH] Tempo total: {end_time - start_time}")

if __name__ == "__main__":
    main()