import os
import time
import json
import signal

def text_to_kojun(data):
    
    lines = data.strip().split("\n")
    width = 0
    height = 0
    grid = []
    regions = []
    solution = []

    section = None
    for line in lines:
        line = line.strip()
        if line == "[problem]":
            section = "problem"
            continue
        elif line == "[areas]":
            section = "areas"
            continue
        elif line.startswith("depth"):  
            continue
        elif line.startswith("size"):
            _, size = line.split()
            width = int(size)
            height = int(size)
            continue
        elif line == "[solution]":
            section = "solution"
            continue
        elif not line or line.startswith("#"):  
            continue

        if section == "problem":
            grid.extend(
                [0 if x == '-' else int(x) for x in line.split()]
            )
        elif section == "areas":
            regions.extend(
                [int(x) for x in line.split()]
            )
        elif section == "solution":
            solution.extend(
                [int(x) for x in line.split()])

    return grid, regions, width, height, solution


def treat_and_run(data, output_file):

    grid, regions, width, height, solution = text_to_kojun(data)

    grid_text = ", ".join(map(str, grid))
    region_text = ", ".join(map(str, regions))

    with open(output_file, 'r') as f:
        content = f.read()
        
    content = content.splitlines()
        
    for i in range(len(content)):
        if i == 5:  
            content[i] = f"-define(WIDTH, {width})."
            content[i+1] = f"-define(HEIGHT, {height})."
        elif i == 17: 
            content[i] = f"  [{grid_text}]."
        elif i == 28:  
            content[i] = f"  [{region_text}]."
            
    content = "\n".join(content)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    os.system("erlc solver.erl")
    
    start_time = time.time()
    os.system("erl -noshell -s solver main -s init stop > output.txt")
    elapsed_time = time.time() - start_time
    signal.alarm(0)


    solution_output = []
    with open("output.txt", "r") as f:
        for line in f:
            if line.strip(): 
                solution_output.append([int(x) for x in line.split()])


    output = [num for row in solution_output for num in row]
    is_correct = output == solution

    return is_correct, elapsed_time


def solve_all_problems(json_file, output_file):

    with open(json_file, "r", encoding="utf-8") as f:
        problems = json.load(f)
        
    total_time = 0
    
    results = []
    for problem in problems:
        print(f"Resolvendo o problema numero {int(problem['url'][35:38])}")
        is_correct, elapsed_time = treat_and_run(problem['data'], output_file)
        results.append({
            "url": problem['url'],
            "is_correct": is_correct,
            "elapsed_time": elapsed_time
        })
        print(f"Problema {problem['url'][35:38]} {'resolvido corretamente' if is_correct else 'falhou'} em {elapsed_time:.2f} segundos.\n")
        total_time += elapsed_time
        
    os.remove("output.txt")
    os.remove("solver.beam")
    
    return results, total_time


json_file = "kojun_problems.json" 
output_file = "solver.erl"  
results, total_time = solve_all_problems(json_file, output_file)


for result in results:
    print(f"{result['url'][35:38]}: {'Correto' if result['is_correct'] else 'Incorreto'}, Tempo: {result['elapsed_time']:.2f} segundos")
    
print(f"\n\nTotal de problemas resolvidos: {len([x for x in results if x['is_correct']])}/{len(results)} em {total_time:.2f} segundos")