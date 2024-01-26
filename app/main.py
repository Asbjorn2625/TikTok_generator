from Lib.Generator import Tiktok as tt
import sys
import os
sys.path.append(os.getcwd())

vid = tt.TikTok_generator(filename="FamilieFyr",url="https://www.youtube.com/watch?v=zBN729Jwab0")
vid.download_video()
"""
vid.crop_video()
vid.generate_audio()
vid.align_video_and_audio()
vid.add_subtitles()
"""