from pytube import YouTube
import os
import requests


# used to download, delete the video and for getting the properties of it
class YTdownload:
  
    def __init__(self, url: str, user_id):

        self.video = YouTube(url)  # pytube video object
        self.title = self.video.title
        self.user_id = user_id
        self.file_name = str(
            self.user_id
        ) + '.mp3'  # it will be saved with telegram chat ID as its name

    def download(self):

        self.downloaded_video = self.video.streams.filter(
            only_audio=True).first().download()  #downloads the video
        os.rename(self.downloaded_video, self.file_name)

    def save_thumbnail(self):

      self.thumbnail = self.video.thumbnail_url
      response = requests.get(self.thumbnail)
      with open(f"{self.user_id}.jpg", "wb") as f:
        f.write(response.content)
        f.close

      return open(f"{self.user_id}.jpg", "rb")

    def delete(self):

        os.remove(self.file_name)
        os.remove(f"{self.user_id}.jpg")

    def properties(self):

        # getting properties
        self.video_title = self.video.title
        self.video_length = self.video.length
        self.video_date = self.video.publish_date
        self.video_views = self.video.views
        self.video_author = self.video.author

        output = f" Title: {self.video_title}\n Author: {self.video_author} \n Date Published: {self.video_date} \n Number Of Views: {self.video_views} \n Length: {self.video_length}"

        return output
