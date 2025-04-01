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



def set_env_variable(name, value):
    """
    Define uma variável de ambiente permanentemente no Windows utilizando o PowerShell como administrador.

    Parâmetros:
    name (str): Nome da variável de ambiente.
    value (str): Valor a ser atribuído à variável de ambiente.

    A função tenta definir a variável tanto no escopo 'Machine' (global).
    """
    for i in ['Machine']:
        command = f"[Environment]::SetEnvironmentVariable('{name}', '{value}', '{i}')"
        powershell_cmd = f'Start-Process powershell -ArgumentList \"{command}\" -Verb RunAs'
        
        print(powershell_cmd)
        try:
            subprocess.run( ["powershell", "-Command", powershell_cmd], shell=True, check=True)
            print(f"✔ Variável de ambiente {name} definida como {value} (Requer reinício para aplicar).")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao definir {name}: {e}")

def cuda_config():
    """
    Configura as variáveis de ambiente necessárias para o CUDA Toolkit versão 12.1 no Windows.

    Define as variáveis 'CUDA_HOME' e 'CUDA_PATH' apontando para os diretórios correspondentes do CUDA Toolkit.
    """
    url = "https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_531.14_windows.exe"  # Substitua pela URL real
    save_folder = "temp"  # Pasta onde o arquivo será salvo
    if os.path.isdir(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1'):
        print(f'O diretório "{r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1'}" existe.')
    else:
        print(f'O diretório "{r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1'}" não existe.')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)  # Cria a pasta se não existir
        
        if filename is None:
            filename = url.split("/")[-1]  # Usa o nome do arquivo da URL se não for fornecido
        
        file_path = os.path.join(save_folder, filename)
        
        response = requests.get(url, stream=True)
        print("Baixando: cuda_12.1.1_531.14_windows.exe! ...")
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Arquivo salvo em: {file_path}")
            if file_path.endswith(".exe"):
                print(f"Executando {file_path}...")
                subprocess.run(file_path, shell=True)

            else:
                print("Erro ao executar arquivo! Não encontrado cuda_12.1.1_531.14_windows.exe")
            # Deletar o arquivo
            try:
                os.remove(file_path)
                print(f"Arquivo {file_path} deletado com sucesso.")
            except FileNotFoundError:
                print(f"O arquivo {file_path} não foi encontrado.")
            except PermissionError:
                print(f"Permissão negada para deletar o arquivo {file_path}.")
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
        else:
            print("Erro ao baixar o arquivo.")
        
    


    set_env_variable("CUDA_HOME", r"C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1")
    set_env_variable("CUDA_PATH", r"C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1")

def add_trailing_slash(path):
    """
    Adiciona uma barra invertida ('\\') ao final de um caminho, se não houver uma.

    Parâmetros:
    path (str): Caminho de diretório ou arquivo.

    Retorna:
    str: Caminho com uma barra invertida no final.
    """
    return path if path.endswith('\\') else path + '\\'   
            
def narration_config():
    """
    Solicita ao usuário os caminhos para salvar narrações, referências de vozes, histórias e modelos.

    Os caminhos são armazenados em um arquivo JSON de configuração utilizando a função 'salvar_json'.
    """
    path_audio = input("Digite o caminho completo para salvar as narrações: ")   
    path_ref = input("Digite o caminho completo das opções de vozes, os arquivos devem ter o padrão <idvoz>_<temperature>_<speed>_<top_k>_<top_p>_<length_penalty>_<repetition_penalty>.wav: ")  
    
    path_history = input("Digite o caminho completo das historias na nomenclatura '<id>_History.: ")  
    path_model = input("Digite o caminho completo da localizacao do modelo: ")  

    # Exemplo de uso
    config_data = {"path_audio": add_trailing_slash(path_audio), "path_history": add_trailing_slash(path_history),"path_model": add_trailing_slash(path_model), "path_ref": add_trailing_slash(path_ref)}
    salvar_json(config_data)




def init():
    """
    Executa o processo de instalação e configuração.

    Inclui a configuração do CUDA Toolkit e a configuração das narrações.
    """
    # Exemplo de uso
    print("Instalação ....")
    print("Configurando CUDA Kit Tool: ....")
    
    cuda_config()
    
    print("Configurando CUDA Kit Tool: Conclido!")
    print("")
    print("Configuração Narration-xtts2: ....")

    narration_config()
    

    


if __name__ == "__main__":
    print("Instalação ....")
    init()