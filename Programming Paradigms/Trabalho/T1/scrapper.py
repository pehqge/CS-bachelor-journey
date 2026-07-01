import requests
from bs4 import BeautifulSoup

def scrape_kojun_problems(base_url, start, end):
    problems = []
    failed_urls = []

    for i in range(start, end + 1):
        url = f"{base_url}/{str(i).zfill(3)}.a.htm"
        print(f"Scraping: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                failed_urls.append(url)
                continue
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            script_tag = soup.find("script", text=lambda x: x and "size" in x)
            if script_tag:
                problem_data = script_tag.text
                
                problem_data = problem_data[problem_data.index("size"):]
                
                problem_data = problem_data[:problem_data.index("[moves]")]
                
                problems.append({"url": url, "data": problem_data})
                print(f"Problema encontrado: {url}")
            else:
                print(f"Dados do problema não encontrados em {url}")
                failed_urls.append(url)

        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
            failed_urls.append(url)
    
    print(f"\nTotal de problemas coletados: {len(problems)}")
    print(f"Páginas com erro ou sem dados: {len(failed_urls)}")
    return problems


base_url = "https://www.janko.at/Raetsel/Kojun"
start = 1  
end = 110

problems = scrape_kojun_problems(base_url, start, end)

with open("kojun_problems.json", "w", encoding="utf-8") as f:
    import json
    json.dump(problems, f, ensure_ascii=False, indent=4)

print("Scraping concluído.")