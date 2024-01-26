import os
import moviepy.editor as mp
import numpy as np
import sys
import shutil
sys.path.append(os.getcwd())

class TikTok_generator:
    def __init__(self,url="https://www.youtube.com/watch?v=Qi4vd3UtBio",filename="Tiktok") -> None:
        self.url = url
        self.filename = filename
        self.prompt = input("What is the subject of your Tiktok?")

    def download_video(self) -> None:
        from pytube import YouTube
        yt = YouTube(self.url)

        # Filter streams by file extension and resolution (720p)
        video_streams = yt.streams.filter(file_extension='mp4', resolution='720p')

        if video_streams:
            # If there is a 720p stream, select the first one
            stream = video_streams[0]

            # Download the video
            stream.download(output_path=os.getcwd(), filename=f"{self.filename}.mp4")
            print(f"Video downloaded successfully in 720p: {self.filename}.mp4")
        else:
            print("No 720p version available for this video.")


    def crop_video(self) -> None:
         # Load video clip
        video_clip = mp.VideoFileClip(f"{os.getcwd()}/{self.filename}.mp4")
        # Calculate the TikTok aspect ratio (9:16)
        tiktok_aspect_ratio = 9 / 16
            
        og_width = video_clip.size[1]
        
        # Calculate the new height based on the TikTok aspect ratio
        new_width = int(og_width * tiktok_aspect_ratio)

        # Crop the video to the TikTok aspect ratio
        cropped_clip = video_clip.crop(x_center=(video_clip.size[0] - new_width) / 2,
                                       width=new_width)

        # Write the cropped video to a file
        cropped_clip.write_videofile(f"output.mp4", codec="libx264", audio_codec="aac")

    def __split_into_chunks(self, text, chunk_size):
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def __concatenate_audio_moviepy(self,audio_clip_paths, output_path):
        """Concatenates several audio files into one audio file using MoviePy
        and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
        clips = [mp.AudioFileClip(c) for c in audio_clip_paths]
        final_clip = mp.concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)

    def __transcribe_audio(self, audio_path):
        import whisper_timestamped as whisper
        import json

        audio = whisper.load_audio(audio_path)

        model = whisper.load_model("tiny", device="cpu")

        transcript = whisper.transcribe(model, audio)

        with open(f"{os.getcwd()}/Transcript.json", 'w') as output_file:
            json.dump(transcript, output_file, indent=4)

    def generate_audio(self)-> None:
        from Lib.TTS import Text2Speech
        from langchain.callbacks.manager import CallbackManager
        from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
        from langchain.llms import Ollama
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        
        llm = Ollama(
            model="llama2-uncensored",
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="Can you tell a short story about {topic} in the format.",
        )
        chain = LLMChain(llm=llm,
                        prompt=prompt,
                        verbose=False)
        text = chain.run(self.prompt)

        chunks = self.__split_into_chunks(text,200)
        
        
        #chunks = self.__split_into_chunks(text,chunak_size)
        os.mkdir(f"{os.getcwd()}/sounds")
        filelocs = []
        for i, text in enumerate(chunks):
            Text2Speech.TiktokTTS('en_us_stitch',text,f"sounds/Sound{i}.mp3")
            filelocs.append(f"{os.getcwd()}/sounds/Sound{i}.mp3")
        self.__concatenate_audio_moviepy(filelocs,"Sound.mp3")
        self.__transcribe_audio(f"{os.getcwd()}/Sound.mp3")
        shutil.rmtree(f"{os.getcwd()}/sounds")

    

    def align_video_and_audio(self):
        import random
        print(f"{os.getcwd()}/Sound.mp3")
        video_clip = mp.VideoFileClip(f"{os.getcwd()}/output.mp4")
        audio_clip = mp.AudioFileClip(f"{os.getcwd()}/Sound.mp3")
        video_duration = video_clip.duration
        audio_duration = audio_clip.duration
        if video_duration-audio_duration > 10:
            randy = random.randint(10,int(abs(video_duration-audio_duration)))
        else:
            randy=10
        
        final_clip = video_clip.subclip(randy,int((randy+audio_duration)))

        final_clip = final_clip.set_audio(audio_clip)
        os.remove(f"{os.getcwd()}/{self.filename}.mp4")
        
        final_clip.write_videofile(f"{self.filename}.mp4")
        
        os.remove(f"{os.getcwd()}/Sound.mp3")
        os.remove(f"{os.getcwd()}/output.mp4")


    def process_subtitleData(self):
        import json
        # Opening JSON file
        f = open(f'{os.getcwd()}/Transcript.json')
        
        # returns JSON object as 
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        data = data['segments']
        new_data = []
        tmp = []
        for words in data:
            new_data.append(words['words'])
        for i in range(len(new_data)):
            for j in range(len(new_data[i])):
                tmp.append([(new_data[i][j]['start'],new_data[i][j]['end']),new_data[i][j]['text']])
        return tmp

    # Function to generate TextClip for subtitles
    def _text_clip_maker(self, subtitle, fontsize=50, color='white'):
        start_time, end_time = subtitle[0]
        text = subtitle[1]
        
        return mp.TextClip(text,font="Nimbus-Sans-L-Bold-Condensed-Italic",fontsize=fontsize, color=color,stroke_color="black",stroke_width=1.1).set_pos(('center', 'center')).set_duration(end_time - start_time).set_start(start_time)
    # Function to add subtitles to video
    def add_subtitles(self):
        video_clip = mp.VideoFileClip(f"{os.getcwd()}/{self.filename}.mp4")

        # Generate TextClips for each subtitle
        subtitles = self.process_subtitleData()
        text_clips = [self._text_clip_maker(subtitle) for subtitle in subtitles]

        # Composite video with subtitles
        video_with_subtitles = mp.CompositeVideoClip([video_clip] + text_clips)
        os.remove(f"{os.getcwd()}/{self.filename}.mp4")

        # Write the final video with subtitles
        video_with_subtitles.write_videofile(f"{os.getcwd()}/{self.filename}.mp4")

    def main(self):
        self.download_video()
        self.crop_video()
        self.generate_audio()
        self.align_video_and_audio()
