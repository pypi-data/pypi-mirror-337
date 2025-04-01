
from moviepy import  VideoFileClip, AudioFileClip, concatenate_videoclips, afx, CompositeAudioClip, vfx
import os
import random
import json







def findVideos(id_selec, config):
    lista_videos = {}
    for i in os.listdir(config["path_video"]):
        split = i.split("_")
        id = split[0]
        if str(id_selec) == str(id):
            print(config["path_video"]+i)
            num = split[2]
            lista_videos[str(num)]=VideoFileClip(config["path_video"]+i,  duration=5)
    return lista_videos

            


def findAudios(id_selec, config):
    lista_audio = {}
    for i in os.listdir(config["path_audio"]+"/"+str(id)+"/"):
        split = i.split("_")
        id = split[0]
        if str(id_selec) == str(id):
            print(config["path_audio"]+"/"+str(id)+"/"+i)
            num = split[2].replace(".wav","")
            lista_audio[str(num)]=AudioFileClip(config["path_audio"]+"/"+str(id)+"/"+i)
    return lista_audio
            

def findFX(id, config):
    fx_list = os.listdir(config["path_FX"])
    fx_selec = random.randint(0, len(fx_list)-1)
    return config["path_FX"]+fx_list[fx_selec]


def maker(id):
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
        
    # set_audios = findAudios(id, config)
    # set_videos = findVideos(id, config)
    # set_fx     = findFX(id, config)
    # print(set_audios)
    # print(set_videos)
    # print(set_fx)
    # print("um audio:",set_audios["10"])
    

    # fx = AudioFileClip(set_fx)

    

    # for audio in range(1,len(set_audios)-1):
    #     aux = set_audios[str(audio)]
    #     aux_video = set_videos[str(audio)]
    #     set_audios[str(audio)] = aux.subclipped(0, min(aux.duration, aux_video.duration))

    # for video in range(1,len(set_videos)-1):
    #     aux = set_videos[str(video)]
    #     set_videos[str(video)] = aux.with_audio(set_audios[str(video)])



    # # # Concatenar os vídeos com seus áudios
    # lista_videos_final = []
    # for i in set_videos:
    #     lista_videos_final.append(set_videos[i])
    # final_video = concatenate_videoclips(lista_videos_final)


    
    # fx = fx.with_effects([afx.AudioLoop(duration=final_video.duration)])

    # fx = fx.with_effects([afx.MultiplyVolume(0.2)])

    # narracao = final_video.audio

    

    # audio_final = CompositeAudioClip([narracao, fx])

    

    # final_video = final_video.with_audio(audio_final)

    final_video = VideoFileClip("C:/Users/will_/OneDrive/Documentos/GitHub/Automatic-Youtube-Maker/AutomaticVideo/workflow/edit/video_com_audio_final_normal.mp4")
    
    final_video = final_video.with_effects([vfx.MultiplySpeed(0.95)])


    # Exportar o vídeo final com os áudios correspondentes
    final_video.write_videofile("C:/Users/will_/OneDrive/Documentos/GitHub/Automatic-Youtube-Maker/AutomaticVideo/workflow/edit/video_com_audio_final.mp4")

if __name__ == "__main__":
    maker(2)
