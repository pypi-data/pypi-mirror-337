# Nome do Projeto

**Descrição breve:** Projeto que baseado em um json cria narrações frase a frase em uma lista de frases, com flexibilidade de parametros do modelo XTTS2.

## Índice

- [Introdução](#introdução)
- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Configurando Variáveis de Ambiente](#configurando-variáveis-de-ambiente)
  - [Instalando Dependências](#instalando-dependências)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Introdução

[Em construlçai]

## Instalação

Uma das dependencias (DeepSpeed) necessita de pré instalação de recursos CUDA para pleno funcionamento.

### Método Direto - Manual

#### CUDA Nvidia 
Baixe e instale Nvidia Cuda Toolkit 12.1 [Link](https://www.exemplo.com)



##### Configurando Variáveis de Ambiente CUDA 12.1


```powershell
[Environment]::SetEnvironmentVariable("CUDA_HOME", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1", "Machine")

[Environment]::SetEnvironmentVariable("CUDA_PATH", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1", "Machine")

```
##### Instale Pytorch = CUDA 12.1


```shell
pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121

```

##### Instale Narration-Xtts2


```shell
pip install narration-xtts2

```

Na primeira execução execute a função **narration_config()** para configurar os diretórios de trabalho

```python
narration_xtts2.utils.install_dependents_win11.narration_config()

```


### Método Direto - Manual

#### CUDA Nvidia 
Baixe e instale Nvidia Cuda Toolkit 12.1 [Link](https://www.exemplo.com)



##### Configurando Variáveis de Ambiente CUDA 12.1


```powershell
[Environment]::SetEnvironmentVariable("CUDA_HOME", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1", "Machine")

[Environment]::SetEnvironmentVariable("CUDA_PATH", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1", "Machine")

```
##### Instale Pytorch = CUDA 12.1


```shell
pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121

```

##### Instale Narration-Xtts2


```shell
pip install narration-xtts2

```

Na primeira execução execute a função **narration_config()** para configurar os diretórios de trabalho

```python
narration_xtts2.utils.install_dependents_win11.narration_config()

```


### Método Direto - SemiAutomatico

##### Instale Narration-Xtts2


```shell
pip install narration-xtts2

```

Na primeira execução execute a função **init()** para configurar os diretórios de trabalho, baixar e executar CUDA 12.1 e configurar as variaveis de ambiente

```python
narration_xtts2.utils.install_dependents_win11.init()

```

##### Re-instale Narration-Xtts2


```shell
pip uninstall narration-xtts2

```

```shell
pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121

```

```shell
pip install narration-xtts2

```
### Pré-requisitos

Especificamente para o pacote deepspeed==0.15
- SO = Windows 11 (testado)
- Python = ">=3.11,<3.12"
- GPU NVIDEA, com suporte a CUDA 12
- CUDA 12.1

