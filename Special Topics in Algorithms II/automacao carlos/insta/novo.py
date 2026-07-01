import csv
import logging
import unicodedata
import time
import os
from tqdm import tqdm
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from google import genai
from google.genai import types

# Inicializa colorama para funcionar em todos os sistemas
init()

# Configuração básica do logging com um handler personalizado
class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Remover handlers existentes
for handler in logger.handlers[:]:
    logger.removeHandler(handler)
# Adicionar o handler personalizado
logger.addHandler(TqdmLoggingHandler())
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.handlers[0].setFormatter(formatter)

# Classe para exibir estatísticas
class LeadStats:
    def __init__(self):
        self.processed = 0
        self.approved = 0
        self.skipped = 0
        self.rate_limited = 0
        self.pbar = None
        
    def init_progress_bar(self, total):
        self.pbar = tqdm(
            total=total, 
            desc=f"{Fore.BLUE}Processando leads{Style.RESET_ALL}", 
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            colour="blue"
        )
        
    def update_progress(self, increment=1):
        if self.pbar:
            self.pbar.update(increment)
            self.processed += increment
            self.update_stats()
            
    def increment_approved(self):
        self.approved += 1
        self.update_stats()
        
    def increment_skipped(self):
        self.skipped += 1
        self.update_stats()
        
    def increment_rate_limited(self):
        self.rate_limited += 1
        self.update_stats()
        
    def update_stats(self):
        if self.pbar:
            stats = (
                f"{Fore.GREEN}Aprovados: {self.approved}{Style.RESET_ALL}, "
                f"{Fore.YELLOW}Ignorados: {self.skipped}{Style.RESET_ALL}, "
                f"{Fore.RED}Rate limited: {self.rate_limited}{Style.RESET_ALL}"
            )
            self.pbar.set_postfix_str(stats)
            
    def countdown(self, seconds):
        """Exibe um contador regressivo quando atinge o limite de requisições"""
        end_time = datetime.now() + timedelta(seconds=seconds)
        with tqdm(total=seconds, desc=f"{Fore.RED}Aguardando limite de requisições{Style.RESET_ALL}", 
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}s restantes", colour="red") as pbar:
            while datetime.now() < end_time:
                remaining = (end_time - datetime.now()).total_seconds()
                if remaining <= 0:
                    break
                time.sleep(0.1)
                progress = seconds - remaining
                pbar.update(progress - pbar.n)
    
    def close(self):
        if self.pbar:
            self.pbar.close()


def normalize_text(text):
    """
    Remove acentuação e espaços, deixando o texto em caixa baixa para comparação.
    """
    if not text:
        return ""
    # Remove acentos
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('utf-8')
    return text.lower().strip()


def get_company_name(row):
    """
    Retorna o nome da empresa a partir dos dados da linha.
    Se o campo 'Empresa' estiver vazio, usa a concatenação de 'Primeiro Nome' e 'Último Nome'.
    """
    empresa = row.get("Empresa", "").strip()
    if not empresa:
        primeiro = row.get("Primeiro Nome", "").strip()
        ultimo = row.get("Último Nome", "").strip()
        empresa = f"{primeiro} {ultimo}".strip()
    return empresa


class GeminiLeadChecker:
    """
    Classe para usar o Gemini e verificar se um lead é relevante para
    produtos de limpeza de betoneira (ou seja, relacionado a concreto).
    Implementação atualizada para usar a API do Gemini conforme documentação oficial.
    """
    def __init__(self, api_key, model_name="gemini-2.0-flash", stats=None):
        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)
        self.prompt_count = 0
        self.stats = stats

    def check_relevance(self, lead):
        """
        Recebe um dicionário com os dados do lead e retorna True se for
        relevante (ou seja, se a empresa tem perfil para comprar produtos para limpar betoneiras) e False caso contrário.
        """
        # Utiliza a função get_company_name para ter o nome correto da empresa
        empresa = get_company_name(lead)
        cargo = lead.get("Cargo", "").strip()
        tags = lead.get("Tags", "").strip()
        biografia = lead.get("Biografia", "").strip()

        prompt_text = f"""
Você é um especialista em identificar leads para empresas que possam comprar produtos para limpar betoneiras. Lembrando que empresas com MIX no nome geralmente são empresas de construção civil.
Analise as informações a seguir e responda apenas com "sim" ou "não".

Empresa: {empresa}
Cargo: {cargo}
Tags: {tags}
Biografia: {biografia}

Este lead é de uma empresa que tem perfil para comprar produtos de limpeza para betoneiras?
        """

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt_text),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=0.2,  # Valor baixo para respostas mais determinísticas
            top_p=0.95,
            top_k=40,
            max_output_tokens=100,  # Reduzido pois esperamos apenas "sim" ou "não"
            response_mime_type="text/plain",
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=generate_content_config,
            )
            
            result = response.text.strip().lower()
            logging.info(f"Resposta do Gemini para o lead '{empresa}': {result}")

            # Se a resposta contiver "sim" (sem "não" ou "nao"), consideramos relevante
            if "sim" in result and ("não" not in result and "nao" not in result):
                return True
            else:
                return False

        except Exception as e:
            time = 2
            
            if "429" in str(e):
                logging.error(f"Limite de solicitações atingido. Aguardando {time} segundos...")
                if self.stats:
                    self.stats.increment_rate_limited()
                    self.stats.countdown(time)
                else:
                    time.sleep(time)
                return self.check_relevance(lead)  # Tenta novamente após esperar
            
            logging.error(f"Erro ao processar o lead: {str(e)}")
            return False


def read_old_leads(file_path):
    """
    Lê o arquivo CSV de leads antigos e retorna um conjunto com os nomes (normalizados) das empresas.
    """
    old_leads = set()
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                # Remove espaços dos nomes dos campos e dos valores
                # Garante que não há chaves None no dicionário
                row = {(k.strip() if k else ""): (v.strip() if v else "") 
                       for k, v in row.items() if k is not None}
                nome = row.get("Nome", "")
                if nome:
                    old_leads.add(normalize_text(nome))
        logging.info(f"Foram encontrados {len(old_leads)} leads antigos.")
    except FileNotFoundError:
        logging.warning(f"Arquivo '{file_path}' não encontrado. Criando lista vazia de leads antigos.")
    except Exception as e:
        logging.error(f"Erro ao ler arquivo de leads antigos: {str(e)}")
    
    return old_leads


def read_existing_filtered_leads(file_path):
    """
    Lê o arquivo CSV de leads já filtrados (se existir) para identificar onde a execução anterior parou.
    Retorna um conjunto com os nomes de empresas já processados e uma contagem.
    """
    existing_filtered = set()
    count = 0
    
    if not os.path.exists(file_path):
        logging.info(f"Arquivo de filtrados '{file_path}' não existe ainda. Começando do início.")
        return existing_filtered, count
    
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                # Garante que não há chaves None no dicionário
                row = {(k.strip() if k else ""): (v.strip() if v else "") 
                       for k, v in row.items() if k is not None}
                
                empresa = get_company_name(row)
                normalized_empresa = normalize_text(empresa)
                if normalized_empresa:
                    existing_filtered.add(normalized_empresa)
                    count += 1
        
        logging.info(f"Encontrados {count} leads já filtrados no arquivo '{file_path}'. Retomando a partir desse ponto.")
    except Exception as e:
        logging.error(f"Erro ao ler arquivo de leads já filtrados: {str(e)}")
    
    return existing_filtered, count


def filter_new_leads(old_leads, new_leads_file, output_file, gemini_checker):
    """
    Lê o arquivo CSV de novos leads, filtra removendo aqueles que já estão na lista antiga
    ou que não são relevantes (usando o Gemini), e grava os leads aprovados em um novo arquivo CSV.
    Salva em tempo real, evita duplicações e suporta retomar de onde parou.
    """
    # Verifica se já existe um arquivo de filtrados e obtém as empresas já processadas
    current_filtered_companies, filtered_count = read_existing_filtered_leads(output_file)
    
    # Conta quantos leads temos para processar
    total_leads = sum(1 for _ in csv.DictReader(open(new_leads_file, newline='', encoding='utf-8'), delimiter=';'))
    
    # Inicializa as estatísticas e barra de progresso
    stats = LeadStats()
    stats.approved = filtered_count  # Inicializa com os leads já aprovados anteriormente
    stats.init_progress_bar(total_leads)
    
    # Atualiza a referência nas estatísticas do Gemini checker
    gemini_checker.stats = stats
    
    try:
        # Determina se estamos criando um novo arquivo ou adicionando ao existente
        file_mode = 'a' if os.path.exists(output_file) and filtered_count > 0 else 'w'
        
        with open(new_leads_file, newline='', encoding='utf-8') as f_in, \
             open(output_file, file_mode, newline='', encoding='utf-8') as f_out:
            
            reader = csv.DictReader(f_in, delimiter=';')
            fieldnames = [field.strip() if field else "" for field in reader.fieldnames if field is not None]
            
            # Se estamos criando um novo arquivo, escrevemos o cabeçalho
            writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter=';')
            if file_mode == 'w':
                writer.writeheader()
            
            for row in reader:
                # Garante que não há chaves None no dicionário
                row = {(k.strip() if k else ""): (v.strip() if v else "") 
                      for k, v in row.items() if k is not None}

                # Obtém o nome da empresa usando a função criada
                empresa = get_company_name(row)
                normalized_empresa = normalize_text(empresa)
                
                # Verifica se o lead já existe na lista antiga
                if normalized_empresa in old_leads:
                    logging.info(f"Lead '{empresa}' já existe na lista de usados. Ignorando.")
                    stats.increment_skipped()
                    stats.update_progress()
                    continue
                    
                # Verifica se o lead já foi processado na execução atual ou em execuções anteriores
                if normalized_empresa in current_filtered_companies:
                    logging.info(f"Lead '{empresa}' já foi processado anteriormente. Ignorando.")
                    stats.increment_skipped()
                    stats.update_progress()
                    continue

                # Usa o Gemini para avaliar se o lead é relevante para produtos de limpeza de betoneira
                if gemini_checker.check_relevance(row):
                    # Adiciona ao conjunto de empresas já processadas
                    current_filtered_companies.add(normalized_empresa)
                    
                    # Escreve imediatamente no arquivo de saída
                    writer.writerow(row)
                    f_out.flush()  # Garante que os dados sejam escritos no disco
                    
                    stats.increment_approved()
                    logging.info(f"{Fore.GREEN}Lead '{empresa}' aprovado e adicionado ao arquivo (Total: {stats.approved}){Style.RESET_ALL}")
                else:
                    logging.info(f"{Fore.YELLOW}Lead '{empresa}' não é relevante para produtos de limpeza de betoneira.{Style.RESET_ALL}")
                    stats.increment_skipped()
                
                stats.update_progress()
    
    except FileNotFoundError as e:
        logging.error(f"{Fore.RED}Arquivo não encontrado: {str(e)}{Style.RESET_ALL}")
        raise
    except Exception as e:
        logging.error(f"{Fore.RED}Erro ao processar os leads: {str(e)}{Style.RESET_ALL}")
        raise
    finally:
        # Sempre fechar a barra de progresso
        stats.close()

    logging.info(f"{Fore.BLUE}Processo concluído. {Fore.RESET}Processados: {stats.processed}, "
                f"{Fore.GREEN}Aprovados: {stats.approved}{Fore.RESET}, "
                f"{Fore.YELLOW}Ignorados: {stats.skipped}{Style.RESET_ALL}")
    logging.info(f"Leads aprovados foram salvos em '{output_file}'.")


def main():
    # Configura sua chave da API do Gemini 
    # gemini_api_key = "AIzaSyAJ4-IolrG5TN7oAwmoz8Q1Dun543DdQLA"
    gemini_api_key = "AIzaSyA9S_dQ6XGTnxNY9329Usf8sVUWGd5NBOY"
    
    # Opcionalmente, poderia configurar via variável de ambiente
    # os.environ["GEMINI_API_KEY"] = gemini_api_key
    
    # Cria o checker com estatísticas (serão atualizadas no filter_new_leads)
    gemini_checker = GeminiLeadChecker(api_key=gemini_api_key, model_name="gemini-2.0-flash-lite")

    # Caminhos dos arquivos CSV
    old_leads_file = "ja usados.csv"
    new_leads_file = "novos.csv"
    output_file = "novos_filtrados.csv"

    print(f"\n{Fore.CYAN}=== ANÁLISE DE LEADS PARA PRODUTOS DE LIMPEZA DE BETONEIRA ==={Style.RESET_ALL}\n")
    
    # Lê os leads antigos
    old_leads = read_old_leads(old_leads_file)

    # Processa e filtra os novos leads, retomando de onde parou se necessário
    filter_new_leads(old_leads, new_leads_file, output_file, gemini_checker)
    
    print(f"\n{Fore.GREEN}✓ Processamento concluído com sucesso!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()