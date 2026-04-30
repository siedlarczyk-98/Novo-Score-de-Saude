import pandas as pd
from scripts.config import AGG_RULES

def limpar_nome_ies(nome_bruto):
    """Mantém o nome original do Metabase para bater perfeitamente com o Google Sheets"""
    if pd.isna(nome_bruto): return ""
    return str(nome_bruto).strip()

def processar_dados_consolidados(df_lista):
    if not df_lista: return pd.DataFrame()

    dfs_consolidados = []
    for df in df_lista:
        temp_df = df.copy()
        temp_df['IES'] = temp_df['IES'].apply(limpar_nome_ies)
        
        # Isola qual é a métrica atual (ex: 'Retencao Geral')
        metric_col = [c for c in temp_df.columns if c not in ['IES', 'Perfil']][0]
        regra = AGG_RULES.get(metric_col, "sum")

        if 'Perfil' in temp_df.columns:
            # Pivot_table agrupa automaticamente IES iguais e espalha os perfis.
            # Se houver linhas duplicadas (ex: Status True/False), ele já aplica a regra (Soma) aqui.
            temp_df = temp_df.pivot_table(
                index='IES', 
                columns='Perfil', 
                values=metric_col, 
                aggfunc=regra
            ).reset_index()
            
            # Renomeia colunas: de 'Usuário/Aluno' para 'Nome da Metrica (Usuário/Aluno)'
            temp_df.columns = ['IES'] + [f"{metric_col} ({c})" for c in temp_df.columns[1:]]
        else:
            temp_df = temp_df.groupby("IES", as_index=False).agg({metric_col: regra})

        dfs_consolidados.append(temp_df)

    # Une todas as tabelas perfeitamente pela IES
    master_df = dfs_consolidados[0]
    for df in dfs_consolidados[1:]:
        master_df = master_df.merge(df, on="IES", how="outer")

    return master_df.fillna(0)