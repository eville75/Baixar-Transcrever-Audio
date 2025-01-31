import yt_dlp as ytdl
from pydub import AudioSegment
import os
import whisper

audio_segment_converter = "C:\\Users\\evill\\OneDrive\\Documentos\\FFmpeg\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"
AudioSegment.converter = audio_segment_converter
AudioSegment.ffmpeg = audio_segment_converter
AudioSegment.ffprobe = "C:\\Users\\evill\\OneDrive\\Documentos\\FFmpeg\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffprobe.exe"

def download_audio(video_url):
    """Baixa o áudio do vídeo do YouTube."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_url, download=True)
    return 'audio.webm'

def convert_audio(input_path):
    """Converte o áudio para WAV com PCM 16-bit."""
    try:
        sound = AudioSegment.from_file(input_path)
        output_path = "audio_convertido.wav"
        sound.export(output_path, format="wav", parameters=["-ac", "1", "-ar", "16000"])
        return output_path
    except Exception as e:
        print(f"Erro ao converter áudio: {e}")
        return None

def transcribe_audio(audio_path):
    """Transcreve o áudio usando Whisper AI."""
    try:
        model = whisper.load_model("base")  # Modelo menor para rapidez
        result = model.transcribe(audio_path, language="pt")
        return result["text"]
    except Exception as e:
        print(f"Erro na transcrição: {e}")
        return ""

def save_transcription(text, filename="transcricao.txt"):
    """Salva a transcrição em um arquivo de texto."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Transcrição salva em {filename}")

def main():
    video_url = input("Insira a URL do vídeo do YouTube: ")
    print("Baixando o áudio...")
    audio_path = download_audio(video_url)
    print("Convertendo o áudio para WAV...")
    converted_audio_path = convert_audio(audio_path)

    if converted_audio_path:
        print("Transcrevendo o áudio...")
        transcription = transcribe_audio(converted_audio_path)
        print("Transcrição completa:")
        print(transcription)
        save_transcription(transcription)

        # Removendo arquivos temporários
        os.remove(audio_path)
        os.remove(converted_audio_path)
        print("Arquivos temporários removidos.")

if __name__ == "__main__":
    main()

