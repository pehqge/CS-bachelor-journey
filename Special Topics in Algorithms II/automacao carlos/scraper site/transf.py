import json
import pandas as pd


def json_to_excel(json_file="resultados.json", excel_file="resultados.xlsx"):
    """
    Transforma um arquivo JSON em um arquivo Excel com as colunas especificadas.

    Args:
        json_file (str): Caminho para o arquivo JSON de entrada.
        excel_file (str): Caminho para o arquivo Excel de saída.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo JSON '{json_file}' não encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Erro: Arquivo JSON '{json_file}' inválido.")
        return

    all_companies = []
    if "resultados" in data:
        for key, value in data["resultados"].items():
            link = value.get("link", "")
            empresas = value.get("empresas", [])
            for empresa in empresas:
                all_companies.append({
                    "Nome": empresa.get("nome", ""),
                    "CNPJ": empresa.get("cnpj", ""),
                    "Endereco Servico": empresa.get("endereco_servico", ""),
                    "Telefone": empresa.get("telefone", ""),
                    "Contexto": empresa.get("contexto", ""),
                    "Link": link
                })

    df = pd.DataFrame(all_companies)
    try:
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Dados salvos em {excel_file}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {e}")
        
json_to_excel()