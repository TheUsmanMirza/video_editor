from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation


class VideoEditor:

    @classmethod
    def trim(cls, filename, target_name, start_time, end_time):
        ffmpeg_extract_subclip(filename=filename, t1=start_time, t2=end_time, targetname=target_name)
        return target_name

    @classmethod
    def add_text(cls, filename, start_time, end_time, text, target_name, h, w):
        video = VideoFileClip(filename)

        # Make the text. Many more options are available.
        txt_clip = (TextClip(text).set_position((w, h))
                    .set_duration(end_time - start_time)
                    .set_start(start_time))
        result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
        result.write_videofile(target_name, fps=25, codec="libx264")
        return target_name

    @classmethod
    def add_text_to_video_object(cls, video_obj, start_time, end_time, text, h, w, font_size, color):
        """
        saprate function to add text in a video object
        """
        # Make the text. Many more options are available.
        txt_clip = (TextClip(text, fontsize=font_size, color=color, font='Courier').set_position((w, h))
                    .set_duration(end_time - start_time)
                    .set_start(start_time))
        result = CompositeVideoClip([video_obj, txt_clip])  # Overlay text on video
        return result


    @classmethod
    def add_audio(cls, video_file, audio_file, target_name, volume, start_time, end_time):
        video = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)

        # Set volume of the audio
        audio_clip = volumex(audio_clip, volume)

        # Set start time and duration of the audio
        video = video.set_audio(CompositeAudioClip([audio_clip.set_start(start_time)]).duration(end_time - start_time))
        video.write_videofile(target_name, fps=25, codec="libx264")
        return target_name

    @classmethod
    def concat_video(cls):
        pass

    @classmethod
    def change_bg(cls, video_filename, target_name, bg_image):

        segmentor = SelfiSegmentation()
        fpsReader = cvzone.FPS()
        imgBG = cv2.imread(bg_image)


        # read video file
        cap = cv2.VideoCapture(video_filename)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        result = cv2.VideoWriter(target_name, cv2.VideoWriter_fourcc(*'FMP4'), fps, size)
        imgBG = cv2.resize(imgBG, size)

        success = True
        while success:
            success, img = cap.read()
            if success:
                img = cv2.resize(img, size)
                # imgOut = segmentor.removeBG(img, (255,0,255), threshold=0.83)
                imgOut = segmentor.removeBG(img, imgBG, threshold=0.83)

                imgStack = cvzone.stackImages([img, imgOut], 2, 1)
                _, imgStack = fpsReader.update(imgStack)
                result.write(imgStack)

            # cv2.imshow("image", imgStack)
            # key = cv2.waitKey(1)

        result.release()
        return target_name

    @classmethod
    def black_n_white(cls, filename, target_name):
        video = VideoFileClip(filename)
        video = video.fx(blackwhite)
        # result = CompositeVideoClip([video])
        video.write_videofile(target_name, fps=25, codec="libx264")
        return target_name


    @classmethod
    def crop(cls, video_file, target_name, x, y, h, w):

        # read video file
        cap = cv2.VideoCapture(video_file)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Output file
        result = cv2.VideoWriter(target_name, cv2.VideoWriter_fourcc(*'FMP4'), fps, size)

        success = True
        while success:
            success, frame = cap.read()
            if success:
                frame = frame[y:y+h, x:x+w]
                result.write(frame)
        result.release()
        return target_name

    @classmethod
    def save_video(cls, video, target_name):
        video.write_videofile(target_name, fps=25, codec="libx264")
        return target_name

    @classmethod
    def get_video_object_from_url(cls, filename):
        video = VideoFileClip(filename)
        return video



