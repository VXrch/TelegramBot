import os
import re
import yt_dlp

filenames = []


def Download_video(what_to_do, url):
    if what_to_do == 'o_v_btn':
        filename = only_video_dwnl(url)
    elif what_to_do == 'o_a_btn':
        filename = only_audio_dwnl(url)
    elif what_to_do == 'a_v_btn':
        filename = audio_video_dwnl(url)
    elif what_to_do == 'o_v_pl_btn':
        filename = only_video_pl_dwnl(url)
    elif what_to_do == 'o_a_pl_btn':
        filename = only_audio_pl_dwnl(url)
    elif what_to_do == 'a_v_pl_btn':
        filename = audio_video_pl_dwnl(url)

    if filename != None:
        return filename
    else:
        return False


def only_video_dwnl(url):
    try:
        options = {
            'format': 'bestvideo[ext=mp4]',
            'noplaylist': True,
            'outtmpl': os.path.join('Downloader', 'downloads', '%(title)s.%(ext)s'),
            'ignoreerrors': True
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = info_dict['title'] + '.' + info_dict['ext']
        return filename
    except Exception as err:
        print(f"An error occurred while downloading the file: {err}")
        return None


def only_audio_dwnl(url):
    try:
        options = {
            'format': 'bestaudio[ext=mp4]',
            'noplaylist': True,
            'outtmpl': os.path.join('Downloader', 'downloads', '%(title)s.%(ext)s'),
            'ignoreerrors': True
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = info_dict['title'] + '.' + info_dict['ext']
        return filename
    except Exception as err:
        print(f"An error occurred while downloading the file: {err}")
        return None


def audio_video_dwnl(url):
    try:
        options = {
            'format': 'best',
            'noplaylist': True,
            'outtmpl': os.path.join('Downloader', 'downloads', '%(title)s.%(ext)s'),
            'ignoreerrors': True
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = info_dict['title'] + '.' + info_dict['ext']
        return filename
    except Exception as err:
        print(f"An error occurred while downloading the file: {err}")
        return None


def only_video_pl_dwnl(url):
    global filenames
    filenames.clear()
    try:
        options = {
            'format': 'bestvideo[ext=mp4]',
            'yes_playlist': True,
            'outtmpl': os.path.join('Downloader', 'downloads', '%(title)s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            entries = info_dict['entries']
            filenames = []
            for entry in entries:
                filename = entry['title'] + '.' + entry['ext']
                filenames.append(filename)
                ydl.download([entry['webpage_url']])
        print("RETURN THIS === ", filenames)
        return filenames
    except Exception as err:
        print(f"An error occurred while downloading the file: {err}")
        return None


def only_audio_pl_dwnl(url):
    global filenames
    filenames.clear()
    try:
        options = {
            'format': 'bestaudio[ext=mp4]',
            'yes_playlist': True,
            'outtmpl': os.path.join('Downloader', 'downloads', '%(title)s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            entries = info_dict['entries']
            filenames = []
            for entry in entries:
                filename = entry['title'] + '.' + entry['ext']
                filenames.append(filename)
                ydl.download([entry['webpage_url']])
        return filenames
    except Exception as err:
        print(f"An error occurred while downloading the file: {err}")
        return None


def audio_video_pl_dwnl(url):
    global filenames
    filenames.clear()
    try:
        options = {
            'format': 'best',
            'yes_playlist': True,
            'outtmpl': os.path.join('Downloader', 'downloads', '%(title)s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            entries = info_dict['entries']
            filenames = []
            for entry in entries:
                filename = entry['title'] + '.' + entry['ext']
                filenames.append(filename)
                ydl.download([entry['webpage_url']])
        return filenames
    except Exception as err:
        print(f"An error occurred while downloading the file: {err}")
        return None


###################################################################################################

def delete_videos(filenames):
    try:
        print("File names = ", filenames)
        for file in filenames:
            file_path = 'Downloader/downloads/' + file
            print("Path to file = ", file_path)
            os.remove(file_path)
            print(f"file {file} successfully deleted!")
    except FileNotFoundError:
        print(f"File {file} is not found!")
    except PermissionError:
        print(f"Permission denied! You can`t delete {file}")
    except Exception as e:
        print(f"Unexpected error! {file}: {str(e)}")


def is_video_url(url):
    try:
        pattern = r'(https?://)?(www\.)?(youtube|youtu|vimeo|dailymotion)\.(com|be)/.*'
        return re.match(pattern, url) is not None
    except Exception as err:
        print(f"There was an error when checking url address: {err}")
        return None
