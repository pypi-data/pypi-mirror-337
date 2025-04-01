import torch
import torch.serialization
import json
import os
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import random

def init():
    print("Carregando configs!")

    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    path_config = os.path.join(script_dir, "config")

    file_path = os.path.join(path_config, "config.json")

    if file_path :
        # Lê o JSON existente
        with open(file_path, 'r', encoding='utf-8') as arquivo:
            config = json.load(arquivo)
    else:
        print("Erro config não existe")


    print("Inicializando TTS")
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    

    config_xtts = XttsConfig()
    config_xtts.max_ref_len = 20
    config_xtts.load_json(config["path_model"]+"config.json")
    model = Xtts.init_from_config(config_xtts)
    model.load_checkpoint(config_xtts, checkpoint_dir=config["path_model"], use_deepspeed=True)
    model.cuda()

    print("TTS inicializado")


    # Versão antiga ##################
    # List available 🐸TTS models
    # print(TTS().list_models())

    # Init TTS
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # tts = TTS(model_path=config["path_model"], config_path=config["path_model"]+"config.json").to(device)
    return model, config

def setTTS(scene, num, id, idioma , tts, config, voice):
    print("Iniciando Narração setTTS .....") 
    print("Computing speaker latents...")
    gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=[config["path_ref"]+voice])
    print("Inference...")
    params = voice.replace(".wav", "").split("_")
    print("Parametros:  ")
    print(params[0])
    print(float(int(params[1])/100))
    print(float(int(params[2])/100))
    print(int(params[3]))
    print(float(int(params[4])/100))
    print(float(int(params[5])))
    print(float(int(params[6])))
    out = tts.inference(
        scene,
        idioma,
        gpt_cond_latent,
        speaker_embedding,

        temperature=float(int(params[1])/100), # Add custom parameters here
        speed=float(int(params[2])/100),
        top_k=int(params[3]),
        top_p=float(int(params[4])/100),
        length_penalty = float(int(params[5])),
        repetition_penalty = float(int(params[6]))


    )
    torchaudio.save(config["path_audio"]+str(id)+"/"+str(id)+"_Scene_"+str(num)+"_"+idioma+"_"+".wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)





    # Versão antiga ##################
    # Text to speech to a file
    # tts.tts_to_file(text=scene,
    #                     speaker_wav=config["file_ref"], 
    #                     language=idioma,
    #                     file_path=config["path_audio"]+str(id)+"_Scene_"+str(num)+"_"+idioma+"_"+".wav"
    #                     )
        

def create_narration(id):

   
    tts, config = init()
    with open(config['path_history']+str(id)+"_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)
    salve_dir = os.path.join(config["path_audio"], str(id))
    if not os.path.exists(salve_dir):
        os.makedirs(salve_dir)
        print(f"Pasta do projeto de voz criada: {salve_dir}")
        voices = [arq for arq in os.listdir(config["path_ref"]) if os.path.isfile(os.path.join(config["path_ref"], arq))]
    
        for lan in history:
            voice = random.choice(voices)
            history[lan]["idvoz"] = voice
            scenes = history[lan]['narration']
            with open(config['path_history']+str(id)+"_history.json", "w", encoding="utf-8") as json_file:
                json.dump(history, json_file, indent=4, ensure_ascii=False)
            
            num = 0
            for i in scenes:
                num = num + 1
                
                setTTS(i, num, id, lan, tts, config, voice)
                
            
    else:
        print(f"A pasta já existe: {salve_dir}")
        print("Abort!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        


    
    
    

if __name__ == "__main__":
    print("Iniciando Narração .....")
    create_narration(10)
