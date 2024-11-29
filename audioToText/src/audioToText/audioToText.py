import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from dotenv import load_dotenv

load_dotenv()

# #single audio file folder path
# audio_folder_path = os.getenv("AUDIO_FOLDER_PATH")
# #audio chunks folder path
# audio_chunks_path = os.getenv("AUDIO_CHUNKS_PATH")
# #single text file folder path
# text_folder_path = os.getenv("TEXT_FOLDER_PATH")

# #folderpath + filename
# audio_file_path = audio_folder_path + "\plsample.wav"

# #folderpath + filename
# text_file_path = text_folder_path + "\plsample.txt"

# filename = os.path.splitext(os.path.basename(audio_file_path))[0]
r = sr.Recognizer()
def transcribe_audio(path):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)

        #language setting
        text = r.recognize_google(audio_listened, language="pl")

    return text
def get_large_audio_transcription_on_silence(path):
    sound = AudioSegment.from_file(path)
    #split when silence > 3000ms, 
    chunks = split_on_silence(sound, 
                              min_silence_len = 3000, silence_thresh=sound.dBFS-14, keep_silence=3000)
    folder_name = audio_chunks_path

    whole_text=""

    for i, audio_chunk in enumerate(chunks, start=1):
        #create chunk in chunk folder
        chunk_filename = os.path.join(folder_name, f"{filename}_chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += "\n"+text
    return whole_text

def audio_to_text(audio_file_path, text_file_path):
    transcription =  get_large_audio_transcription_on_silence(audio_file_path)
    with open(text_file_path, "w", encoding="utf=8") as f:
        f.write(transcription)

audio_to_text(audio_file_path, text_file_path)


