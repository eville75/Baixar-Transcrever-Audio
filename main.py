import yt_dlp as ytdl
from pydub import AudioSegment
import os
import whisper
import language_tool_python

audio_segment_converter = r"C:\EVILLE\PROJETOS\Baixar-Transcrever-Audio\ffmpeg\FFmpeg\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
AudioSegment.converter = audio_segment_converter
AudioSegment.ffmpeg = audio_segment_converter
AudioSegment.ffprobe = r"C:\EVILLE\PROJETOS\Baixar-Transcrever-Audio\ffmpeg\FFmpeg\ffmpeg-master-latest-win64-gpl-shared\bin\ffprobe.exe"


def baixar_audio(url_video):
    opcoes_ydl = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with ytdl.YoutubeDL(opcoes_ydl) as ydl:
        ydl.extract_info(url_video, download=True)
        return "audio.mp3"

def converter_audio(caminho_entrada):
    try:
        som = AudioSegment.from_file(caminho_entrada)
        caminho_saida = "audio_convertido.wav"
        som = som.set_channels(1).set_frame_rate(16000)
        som.export(caminho_saida, format="wav")
        return caminho_saida
    except Exception as e:
        print(f"Erro ao converter áudio: {e}")
        return None

def transcrever_audio(caminho_audio):
    try:
        modelo = whisper.load_model("medium")
        resultado = modelo.transcribe(caminho_audio, language="pt")
        return resultado["text"]
    except Exception as e:
        print(f"Erro na transcrição: {e}")
        return ""

def corrigir_texto(texto):
    try:
        ferramenta = language_tool_python.LanguageTool("pt-BR")
        texto_corrigido = ferramenta.correct(texto)
        return texto_corrigido
    except Exception as e:
        print(f"Erro ao corrigir texto: {e}")
        return texto

def salvar_transcricao(texto, nome_arquivo="transcricao.txt"):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"✅ Transcrição salva em {nome_arquivo}")

def principal():
    url_video = input("🎥 Insira a URL do vídeo do YouTube: ")
    print("⏳ Baixando o áudio...")
    caminho_audio = baixar_audio(url_video)
    
    if not os.path.exists(caminho_audio):
        print("❌ Erro: O áudio não foi baixado corretamente.")
        return
    
    print("🔄 Convertendo o áudio para WAV...")
    caminho_audio_convertido = converter_audio(caminho_audio)
    
    if caminho_audio_convertido:
        print("📝 Transcrevendo o áudio...")
        transcricao = transcrever_audio(caminho_audio_convertido)
        print("\n✅ Transcrição bruta:")
        print(transcricao)
        
        print("\n🔍 Corrigindo a transcrição...")
        transcricao_corrigida = corrigir_texto(transcricao)
        print("\n✅ Transcrição corrigida:")
        print(transcricao_corrigida)
        
        salvar_transcricao(transcricao_corrigida)
        
        for arquivo in [caminho_audio, caminho_audio_convertido]:
            if os.path.exists(arquivo):
                os.remove(arquivo)
        print("🗑️ Arquivos temporários removidos.")

if __name__ == "__main__":
    principal()
