import os
import requests
import subprocess
import winreg
import json

def salvar_json(dados, filename="config.json"):
    """
    Salva um dicionário em formato JSON em um arquivo dentro do diretório 'config'.

    Parâmetros:
    dados (dict): Dados a serem salvos no arquivo JSON.
    filename (str): Nome do arquivo JSON. Padrão é 'config.json'.

    O arquivo será salvo em um diretório 'config' localizado no nível acima do diretório do script atual.
    """
    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    save_dir = os.path.join(os.path.dirname(script_dir), "config")

    # Garante que a pasta "config" existe
    os.makedirs(save_dir, exist_ok=True)

    # Caminho completo do arquivo JSON
    file_path = os.path.join(save_dir, filename)

    # Salva o JSON
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)
    
    print(f"JSON salvo em: {file_path}")


def update_json(chave, valor, filename="config.json"):
    """
    Atualiza ou adiciona uma chave e seu valor correspondente em um arquivo JSON existente.

    Parâmetros:
    chave (str): Chave a ser atualizada ou adicionada no JSON.
    valor (any): Valor associado à chave.
    filename (str): Nome do arquivo JSON. Padrão é 'config.json'.

    O arquivo é localizado no diretório 'config' no nível acima do diretório do script atual.
    """
    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    save_dir = os.path.join(os.path.dirname(script_dir), "config")

    # Caminho completo do arquivo JSON
    file_path = os.path.join(save_dir, filename)

    # Lê o JSON existente
    with open(file_path, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    dados[chave] = valor    

    # Salva o JSON
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)
    
    print(f"JSON salvo em: {file_path}")



def add_trailing_slash(path):
    """
    Adiciona uma barra invertida ('\\') ao final de um caminho, se não houver uma.

    Parâmetros:
    path (str): Caminho de diretório ou arquivo.

    Retorna:
    str: Caminho com uma barra invertida no final.
    """
    return path if path.endswith('\\') else path + '\\'   
            
def config():
    """
    Solicita ao usuário os caminhos para salvar narrações, referências de vozes, histórias e modelos.

    Os caminhos são armazenados em um arquivo JSON de configuração utilizando a função 'salvar_json'.
    """

    path_video = input("Digite o caminho completo do output do comfyUI: ")  
    path_audio = input("Digite o caminho completo para salvar as narrações: ")  
    path_FX    = input("Digite o caminho completo dos soms de fundo do video : ")  

     

    # Exemplo de uso
    config_data = { "path_video" : add_trailing_slash(path_video),
                    "path_audio" : add_trailing_slash(path_audio),
                    "path_FX"    : add_trailing_slash(path_FX)}
    salvar_json(config_data)

