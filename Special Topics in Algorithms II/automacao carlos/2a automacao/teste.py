import re
import json
import argparse
from PyPDF2 import PdfReader

def extrair_texto_pdf(caminho_pdf):
    """Extrai e concatena o texto de todas as páginas do PDF."""
    texto_completo = ""
    with open(caminho_pdf, "rb") as f:
        leitor = PdfReader(f)
        for pagina in leitor.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

def extrair_metadados(texto):
    """Extrai dados do cabeçalho do currículo."""
    metadados = {}
    # Exemplo: "CURRÍCULO DO CURSO\n501 - AGRONOMIA\n20251"
    cabecalho = re.search(r"CURRÍCULO DO CURSO\s+(\d+)\s*-\s*([A-ZÇÁÉÍÓÚ\s]+)\s+(\d+)", texto)
    if cabecalho:
        metadados["codigo_curso"] = cabecalho.group(1).strip()
        metadados["nome_curso"] = cabecalho.group(2).strip()
        metadados["curriculo"] = cabecalho.group(3).strip()

    # Exemplo: extração do campo "Habilitação"
    habilitacao = re.search(r"Habilitação:\s+([\w\sÀ-ÿ]+)", texto)
    if habilitacao:
        metadados["habilitacao"] = habilitacao.group(1).strip()
    
    # Você pode incluir mais expressões para outros campos necessários (documentação, objetivo, carga horária, etc.)
    return metadados

def extrair_disciplinas(texto):
    """
    Tenta separar as disciplinas por fase.
    Cada fase pode ser identificada por um cabeçalho como "1ª Fase-sugestão", "2ª Fase-sugestão", etc.
    Em seguida, busca blocos com dados das disciplinas.
    OBS.: As expressões regulares abaixo são um exemplo e podem precisar de ajustes conforme a formatação.
    """
    disciplinas_por_fase = []
    # Divide o texto pelas fases (exemplo: "1ª Fase-sugestão")
    fases = re.split(r"(\d+ª Fase-sugestão)", texto)
    # Se a divisão resultar em uma lista com cabeçalho e conteúdo intercalados, percorre os pares:
    if len(fases) > 1:
        for i in range(1, len(fases), 2):
            fase_nome = fases[i].strip()
            conteudo_fase = fases[i+1] if i+1 < len(fases) else ""
            disciplinas = []
            # Exemplo de extração: procura padrões como "ObXXXXXX 3Nome da Disciplina ... CH"
            # Essa regex busca um código que comece com "Ob", seguido de letras/números, depois um número (quantidade de aulas) e outro número (CH)
            padrao_disciplina = re.finditer(r"(Ob[A-Z0-9]+)\s+(.+?)\s+(\d+)\s+(\d+)", conteudo_fase)
            for match in padrao_disciplina:
                disciplina = {
                    "codigo": match.group(1).strip(),
                    "nome": match.group(2).strip(),
                    "aulas": match.group(3).strip(),
                    "carga_horaria": match.group(4).strip()
                }
                disciplinas.append(disciplina)
            disciplinas_por_fase.append({
                "fase": fase_nome,
                "disciplinas": disciplinas
            })
    return disciplinas_por_fase

def gerar_json(dados, caminho_saida):
    """Salva os dados extraídos em um arquivo JSON."""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Arquivo JSON criado: {caminho_saida}")

def main(caminho_pdf, caminho_saida):
    texto = extrair_texto_pdf(caminho_pdf)
    dados = {
        "curso": extrair_metadados(texto),
        "disciplinas": extrair_disciplinas(texto)
    }
    gerar_json(dados, caminho_saida)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrai dados de um PDF de currículo e gera um JSON com as informações.")
    parser.add_argument("--input", type=str, required=True, help="Caminho do arquivo PDF de entrada")
    parser.add_argument("--output", type=str, default="curriculo.json", help="Caminho do arquivo JSON de saída")
    args = parser.parse_args()
    main(args.input, args.output)