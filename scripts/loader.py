import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def exportar_para_sheets(df, spreadsheet_id, json_path):
    print(f"☁️ Conectando ao Google Sheets...")
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        try:
            sheet = spreadsheet.worksheet("metabase_input")
        except gspread.exceptions.WorksheetNotFound:
            print("⚠️ Aba 'metabase_input' não encontrada. Criando...")
            sheet = spreadsheet.add_worksheet(title="metabase_input", rows="100", cols="50")

        print("🧹 Limpando dados antigos...")
        sheet.clear()

        df_clean = df.fillna("")
        dados_para_colar = [df_clean.columns.values.tolist()] + df_clean.values.tolist()

        print(f"📤 Enviando {len(df_clean)} linhas...")
        sheet.update('A1', dados_para_colar)
        print("✅ Sucesso! Dados atualizados.")

    except Exception as e:
        print(f"❌ Erro no Exportar: {e}")

def escrever_log_dashboard(spreadsheet_id, json_path, aba_nome, celula, texto):
    """
    Aqui você NÃO MUDA nada. O Python vai receber o nome da aba e a célula 
    que você enviar lá no main.py.
    """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(spreadsheet_id).worksheet(aba_nome)
        
        # O gspread espera uma lista de listas para o update
        sheet.update(celula, [[texto]])
        print(f"📍 Log registrado em {aba_nome}!{celula}")

    except Exception as e:
        print(f"❌ Falha ao registrar log: {e}")