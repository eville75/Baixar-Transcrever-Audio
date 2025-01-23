import yt_dlp as ytdl
from pydub import AudioSegment
import os
import speech_recognition as sr
import re

def download_audio(video_url, output_format="mp3"):
    """
    Baixa o áudio do vídeo do YouTube usando yt-dlp.
    """
    ydl_opts = {
        'format': 'bestaudio/best',  # Seleciona o melhor áudio disponível
        'outtmpl': 'audio.%(ext)s',  # Define o nome do arquivo de saída
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        audio_url = info_dict.get("url")
        print(f"Áudio baixado com sucesso: {audio_url}")
        return 'audio.webm'  # Renomeando para webm, que é o formato esperado para o áudio

def convert_audio(input_path, output_format="mp3"):
    """
    Converte o áudio baixado para o formato desejado (default: mp3).
    """
    try:
        sound = AudioSegment.from_file(input_path)
        output_path = "audio_convertido." + output_format
        sound.export(output_path, format=output_format)
        print(f"Áudio convertido para {output_format}: {output_path}")
        return output_path
    except Exception as e:
        print(f"Erro ao converter o áudio: {e}")
        return None

def transcribe_audio(audio_path):
    """
    Transcreve o áudio para texto utilizando o reconhecedor do SpeechRecognition.
    """
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        
        # Usando o reconhecedor Sphinx (offline)
        text = recognizer.recognize_sphinx(audio)
        print("Transcrição realizada com sucesso!")
        return text
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
        return ""
    except sr.RequestError:
        print("Erro ao se conectar ao serviço de transcrição.")
        return ""
    except Exception as e:
        print(f"Erro na transcrição: {e}")
        return ""

def summarize_text(text):
    """
    Faz um resumo básico do texto transcrito.
    """
    words = text.split()
    summary = " ".join(words[:100]) + "..." if len(words) > 100 else text
    return summary

def main():
    # URL do vídeo do YouTube
    video_url = input("Insira a URL do vídeo do YouTube: ")
    
    # Baixando o áudio
    print("Baixando o áudio do vídeo...")
    audio_path = download_audio(video_url, output_format="mp3")
    
    # Convertendo o áudio para o formato desejado (opcional)
    converted_audio_path = convert_audio(audio_path, output_format="mp3")
    
    # Verificando se a conversão foi bem-sucedida antes de transcrever
    if converted_audio_path:
        # Transcrevendo o áudio para texto
        print("Transcrevendo o áudio para texto...")
        transcribed_text = transcribe_audio(converted_audio_path)
        
        if transcribed_text:
            # Gerando o resumo do texto transcrito
            summary = summarize_text(transcribed_text)
            print("\nResumo do áudio transcrito:")
            print(summary)
    
        # Remover arquivos temporários se necessário
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Arquivo {audio_path} removido.")
        if os.path.exists(converted_audio_path):
            os.remove(converted_audio_path)
            print(f"Arquivo {converted_audio_path} removido.")

if __name__ == "__main__":
    main()
