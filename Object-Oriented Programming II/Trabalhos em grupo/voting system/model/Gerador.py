import os
import json
import random

class GeradorModel:
    def __init__(self, pasta, num_regioes, num_candidatos):
        self.criador_arquivos(pasta, int(num_regioes), int(num_candidatos))

    def criador_arquivos(self, pasta, num_regioes, num_candidatos):
        files = [file for file in os.listdir(pasta) if file.endswith(".json")]
        for file in files:
            os.remove(os.path.join(pasta, file))

        for i in range(num_regioes):
            filename = f"{i+1:0{len(str(num_regioes))}d}.json"
            filepath = os.path.join(pasta, filename)

            candidates = {}
            for j in range(num_candidatos):
                candidate_name = f"Candidato {j+1}"
                vote_count = random.randint(0, 1000)
                candidates[candidate_name] = vote_count

            with open(filepath, "w") as f:
                json.dump(candidates, f)
