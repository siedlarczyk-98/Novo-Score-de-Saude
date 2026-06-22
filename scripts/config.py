import os
from dotenv import load_dotenv

load_dotenv()

# Autenticação
BASE_URL = os.getenv("METABASE_URL")
API_KEY = os.getenv("METABASE_API_KEY")

CARDS_CONFIG = {
    1580: "Acessos Plataforma",
    1586: "Acessos Plataforma 30d",
    1578: "Ativos e Inativos",
    1587: "Ativos e Inativos 30d",
    1579: "Casos e Repeticao",
    1585: "Casos e Repeticao 30d",
    1581: "Retencao",               # Com Perfil
    1588: "Retencao Geral",         
    1584: "Retencao 30d",           # Com Perfil
    1589: "Retencao Geral 30d",     
    1582: "Satisfacao",             # Com Perfil
    1590: "Satisfacao Geral",       
    1583: "Satisfacao 30d",         # Com Perfil
    1591: "Satisfacao Geral 30d",
    1614: "Licenças Professores Contratadas",
    1615: "Licenças Alunos Contratadas",
    1673: "Acesso aos cursos 30d",
    1674: "Acesso aos cursos Geral"
}

AGG_RULES = {
    "Acessos Plataforma": "sum",
    "Acessos Plataforma 30d": "sum",
    "Ativos e Inativos": "sum",
    "Ativos e Inativos 30d": "sum",
    "Casos e Repeticao": "sum",
    "Casos e Repeticao 30d": "sum",
    "Retencao": "mean",
    "Retencao Geral": "mean",
    "Retencao 30d": "mean",
    "Retencao Geral 30d": "mean",
    "Satisfacao": "mean",
    "Satisfacao Geral": "mean",
    "Satisfacao 30d": "mean",
    "Satisfacao Geral 30d": "mean",
    "Licenças Professores Contratadas": "sum",
    "Licenças Alunos Contratadas": "sum",
    "Acesso aos cursos 30d": "sum",
    "Acesso aos cursos Geral": "sum"
}

IES_CLEAN_MAP = {
    "IDOMED": "IDOMED",
    "UNINOVE": "UNINOVE",
}

FINAL_COLUMNS = [
    "IES", 
    "Acessos Plataforma", "Acessos Plataforma 30d",
    "Ativos e Inativos", "Ativos e Inativos 30d",
    "Casos e Repeticao", "Casos e Repeticao 30d",
    "Retencao Geral", "Retencao 30d",
    "Satisfacao Geral", "Satisfacao 30d",
    "Licenças Professores Contratadas", "Licenças Alunos Contratadas",
    "Acesso aos cursos Geral", "Acesso aos cursos 30d"
]