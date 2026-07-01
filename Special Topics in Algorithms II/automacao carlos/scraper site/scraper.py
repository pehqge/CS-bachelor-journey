import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai
import logging
from transf import json_to_excel

# Configura logging para ajudar na depuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GeminiExtractor:
    def __init__(self, api_key, model_name="gemini-pro"):
        """Inicializa o extractor Gemini."""
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    def extract_company_info(self, text, link):
        """Extrai informações detalhadas de empresas a partir do texto."""
        prompt = f"""
        Você receberá um texto de um diário oficial. Sua tarefa é extrair informações detalhadas sobre empresas mencionadas no texto que estejam relacionadas a concreto, pavimentação, asfalto, construtoras, etc.

        Para cada empresa encontrada, você deve fornecer as seguintes informações:

        - **nome**: Nome da empresa.
        - **cnpj**: Número do CNPJ da empresa, se disponível.
        - **endereco_servico**: O nome da cidade onde o serviço está sendo ocorrido. Está sempre presente no link ou no texto. (este NUNCA pode estar vazio, sempre precisa estar preenchido com a cidade que está no link)
        - **telefone**: Número de telefone da empresa, se disponível.
        - **contexto**: Um breve resumo do que a empresa está fazendo no contexto do texto.

        Se alguma informação não estiver disponível no texto, deixe o campo correspondente vazio, mas certifique-se que todos os itens (nome, cnpj, endereco_servico, telefone, contexto) estão presentes.
        
        Formate a saída como uma lista de dicionários JSON, onde cada dicionário representa uma empresa encontrada.

        Se nenhuma empresa relevante for encontrada, retorne uma lista JSON vazia: `[]`

        Texto: {text}
        Link: {link}
        """
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logging.info(f"Resposta do Gemini para extração detalhada: {result}")
            
            # Tenta carregar a resposta como JSON diretamente
            try:
                company_list = json.loads(result)
                return company_list
            except json.JSONDecodeError:
                # Se falhar, verifica se a resposta inclui um bloco de código JSON
                if result.startswith("```json") and result.endswith("```"):
                    try:
                        json_string = result[7:-3].strip()
                        company_list = json.loads(json_string)
                        return company_list
                    except json.JSONDecodeError:
                         logging.error(f"Resposta Gemini com bloco JSON inválido: {result}")
                         return []
                else:
                     logging.error(f"Resposta Gemini não é JSON válido e não contém bloco JSON: {result}")
                     # Se não for um JSON válido, tenta corrigir com o Gemini novamente
                     correction_prompt = f"Por favor, formate a resposta anterior como uma lista de dicionários JSON. A resposta atual é: {result}"
                     corrected_response = self.model.generate_content(correction_prompt)
                     corrected_result = corrected_response.text.strip()
                     try:
                         return json.loads(corrected_result)
                     except json.JSONDecodeError:
                         logging.error(f"Não foi possível corrigir o formato JSON. Resposta Gemini: {corrected_result}")
                         return []

        except Exception as e:
            logging.error(f"Erro ao usar o Gemini: {e}")
            return []



class WebScraper:
    def __init__(self, base_url, progress_file, gemini_extractor):
        """Inicializa o scraper."""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = base_url
        self.progress_file = progress_file
        self.gemini_extractor = gemini_extractor
        self.progress = self._load_progress()

    def _load_progress(self):
        """Carrega o progresso do arquivo JSON."""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, "r") as f:
                return json.load(f)
        return {"pagina": 1, "item": 0, "resultados": {}}

    def _save_progress(self):
        """Salva o progresso em um arquivo JSON."""
        with open(self.progress_file, "w") as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=4)

    def _search_term(self, term, date):
        """Realiza a busca no site."""
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        busca_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-invalid='false']")
        busca_input.send_keys(term)

        date_input = self.driver.find_element(By.CSS_SELECTOR, "input#\\:r1\\:")
        date_input.send_keys(Keys.DOWN)
        date_input.send_keys(date)

        busca_input.send_keys(Keys.ENTER)
        self.driver.find_element(By.CSS_SELECTOR, ".css-1oy4u67").click()
        time.sleep(2)
    
    def _update_progress_and_save(self, key, link, empresas):
      """Atualiza o progresso e salva em tempo real."""
      if "resultados" not in self.progress:
         self.progress["resultados"] = {}
      self.progress["resultados"][key] = {
        "link": link,
        "empresas": empresas
      }
      self._save_progress()

    def scrape(self, term="pavimentação", date="11112024"):
        """Realiza o scraping completo."""
        try:
            # Inicia a busca
            self._search_term(term, date)

            # Navega para a página salva
            for _ in range(1, self.progress["pagina"]):
                self.driver.find_element(By.CSS_SELECTOR, ".css-6rdzsm").click()

            # Processa itens e páginas
            while True:
                items = self.driver.find_elements(By.CSS_SELECTOR, ".css-yzftv1")
                total_items = len(items)

                for i in range(self.progress["item"], total_items):
                    self.progress["item"] = i
                    try:
                        items[i].click()
                        time.sleep(1)

                        # Troca para a aba nova
                        self.driver.switch_to.window(self.driver.window_handles[1])

                        # Pega o link atual
                        link = self.driver.current_url
                        text_content = self.driver.find_element(By.TAG_NAME, "body").text
                        company_info = self.gemini_extractor.extract_company_info(text_content, link)

                        if company_info: # Só adiciona se tiver alguma informação de empresa
                            key = f"pagina_{self.progress['pagina']}_item_{i}"
                            self._update_progress_and_save(key, link, company_info)

                        # Fecha a aba e retorna à principal
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
        
                    except Exception as e:
                        logging.error(f"Erro ao processar item {i}: {e}")
                        if self.driver.window_handles:  # Verifica se ainda há janelas abertas
                             self.driver.switch_to.window(self.driver.window_handles[0])
                        continue

                # Próxima página
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".css-6rdzsm").click()
                    self.progress["pagina"] += 1
                    self.progress["item"] = 0
                    self._save_progress()
                    time.sleep(1)
                except Exception:
                    logging.info("Fim das páginas ou erro ao avançar.")
                    break
        finally:
            self.driver.quit()


if __name__ == "__main__":
    # Configura a chave da API do Gemini pela variável de ambiente
    gemini_api_key = "AIzaSyAJ4-IolrG5TN7oAwmoz8Q1Dun543DdQLA"
    if not gemini_api_key:
        logging.error("A variável de ambiente GOOGLE_API_KEY não está definida.")
    else:
        gemini = GeminiExtractor(api_key=gemini_api_key)
        scraper = WebScraper(
            base_url="https://doe.sp.gov.br/busca-avancada",
            progress_file="resultados.json",
            gemini_extractor=gemini,
        )

        scraper.scrape()