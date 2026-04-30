import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def exportar_para_sheets(df, spreadsheet_id, json_path):
    """
    df: O DataFrame final com os dados consolidados
    spreadsheet_id: O ID longo que está no seu .env
    json_path: O caminho para o seu arquivo credenciais.json
    """
    print(f"☁️ Conectando ao Google Sheets...")
    
    # Configuração de escopo para acessar Planilhas e Drive
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        # Autenticação
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        
        # Abre a planilha pelo ID
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        # Tenta acessar a aba 'metabase_input'
        try:
            sheet = spreadsheet.worksheet("metabase_input")
        except gspread.exceptions.WorksheetNotFound:
            print("⚠️ Aba 'metabase_input' não encontrada. Criando uma nova...")
            sheet = spreadsheet.add_worksheet(title="metabase_input", rows="100", cols="50")

        # --- FAXINA E PREPARAÇÃO ---
        print("🧹 Limpando dados antigos...")
        sheet.clear()

        # Tratamento de dados: Converte NaN para vazio e garante que tudo seja string/número simples
        df_clean = df.fillna("")
        
        # O gspread precisa de uma lista de listas (Cabeçalho + Dados)
        dados_para_colar = [df_clean.columns.values.tolist()] + df_clean.values.tolist()

        # --- UPLOAD ---
        print(f"📤 Enviando {len(df_clean)} linhas para a nuvem...")
        sheet.update('A1', dados_para_colar)
        
        print("✅ Sucesso! Dados atualizados no Google Sheets.")

    except Exception as e:
        print(f"❌ Erro crítico no Loader: {e}")