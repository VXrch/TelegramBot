import telebot
from telebot import types
import Downloader.downloaderFromYT

bot = telebot.TeleBot('')
file_names_to_delete = []


@bot.message_handler(commands=['start'])
def start(message):

    kb = types.InlineKeyboardMarkup(row_width=1)

    only_video_btn = types.InlineKeyboardButton(
        text=' Only video (🔇)', callback_data='o_v_btn')
    only_audio_btn = types.InlineKeyboardButton(
        text='Only audio 🎵', callback_data='o_a_btn')
    audio_video_btn = types.InlineKeyboardButton(
        text='audio 🎼 + video 🎥', callback_data='a_v_btn')
    only_video_playlist_btn = types.InlineKeyboardButton(
        text='Only video playlist (🔇)', callback_data='o_v_pl_btn')
    only_audio_playlist_btn = types.InlineKeyboardButton(
        text='Only audio playlist 🎶', callback_data='o_a_pl_btn')
    audio_vidoe_playlist_btn = types.InlineKeyboardButton(
        text='audio 🔊 + video playlist 📽', callback_data='a_v_pl_btn')

    kb.add(only_video_btn, only_audio_btn, audio_video_btn,
           only_video_playlist_btn, only_audio_playlist_btn, audio_vidoe_playlist_btn)

    bot.send_message(
        message.chat.id, 'Hello! What do you want to download?', reply_markup=kb)


def continue_downloading(message):

    kb = types.InlineKeyboardMarkup(row_width=1)

    only_video_btn = types.InlineKeyboardButton(
        text=' Only video (🔇)', callback_data='o_v_btn')
    only_audio_btn = types.InlineKeyboardButton(
        text='Only audio 🎵', callback_data='o_a_btn')
    audio_video_btn = types.InlineKeyboardButton(
        text='audio 🎼 + video 🎥', callback_data='a_v_btn')
    only_video_playlist_btn = types.InlineKeyboardButton(
        text='Only video playlist (🔇)', callback_data='o_v_pl_btn')
    only_audio_playlist_btn = types.InlineKeyboardButton(
        text='Only audio playlist 🎶', callback_data='o_a_pl_btn')
    audio_vidoe_playlist_btn = types.InlineKeyboardButton(
        text='audio 🔊 + video playlist 📽', callback_data='a_v_pl_btn')

    kb.add(only_video_btn, only_audio_btn, audio_video_btn,
           only_video_playlist_btn, only_audio_playlist_btn, audio_vidoe_playlist_btn)

    bot.send_message(
        message.chat.id, 'What do you want to download?', reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    global what_to_do
    if callback.data == 'o_v_btn' or callback.data == 'o_a_btn' or callback.data == 'a_v_btn' or callback.data == 'o_v_pl_btn' or callback.data == 'o_a_pl_btn' or callback.data == 'a_v_pl_btn':
        what_to_do = callback.data
        bot.send_message(callback.message.chat.id, 'Enter video url: ')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global file_names_to_delete
    file_names_to_delete.clear()
    try:
        bot.send_message(message.chat.id, 'It may take a few minutes...')
        url = message.text
        if Downloader.downloaderFromYT.is_video_url(url):  # IF USER SEND A URL

            temp_names = Downloader.downloaderFromYT.Download_video(
                what_to_do, url)
            if temp_names != False:
                if what_to_do == 'o_v_pl_btn' or what_to_do == 'o_a_pl_btn' or what_to_do == 'a_v_pl_btn':
                    for name in temp_names:
                        file_names_to_delete.append(name)
                else:
                    file_names_to_delete.append(str(temp_names))
                    file_with_path = 'Downloader/downloads/' + temp_names

                # If only one video (--no-playlist)
                if what_to_do == 'o_a_btn' or what_to_do == 'o_v_btn' or what_to_do == 'a_v_btn':
                    if what_to_do == 'o_a_btn':  # Only audio without video
                        try:
                            with open(file_with_path, 'rb') as audio_file:
                                bot.send_audio(message.chat.id, audio_file)
                        except Exception as err:
                            print(
                                f"An error occurred while sending a message: {err}")
                            bot.send_message(
                                message.chat.id, 'An error occurred while sending a message')
                    else:  # "Audio + video" or "video"
                        try:
                            with open(file_with_path, 'rb') as video_file:
                                bot.send_video(message.chat.id, video_file)
                        except Exception as err:
                            print(
                                f"An error occurred while sending a message: {err}")
                            bot.send_message(
                                message.chat.id, 'An error occurred while sending a message')

                else:  # If downloading playlist (--yes-playlist)
                    if what_to_do == 'o_v_pl_btn' or what_to_do == 'a_v_pl_btn':  # Send video playlist
                        try:
                            for file in temp_names:
                                video_path = 'Downloader/downloads/' + file
                                with open(video_path, 'rb') as video_file:
                                    bot.send_video(message.chat.id, video_file)
                        except Exception as err:
                            print(f"An error occurred while sending a message: {err}")
                            bot.send_message(
                                message.chat.id, 'An error occurred while sending a message')
                    else:  # Send audio playlist
                        try:
                            for file in temp_names:
                                audio_path = 'Downloader/downloads/' + file
                                with open(audio_path, 'rb') as audio_file:
                                    bot.send_audio(message.chat.id, audio_file)
                        except Exception as err:
                            print(f"An error occurred while sending a message: {err}")
                            bot.send_message(
                                message.chat.id, 'An error occurred while sending a message')
            else:
                print(
                    f"An error occurred while downloading the file! File returned \"FALSE\"")
                bot.send_message(
                    message.chat.id, 'An error occurred while downloading the file!')
        else:
            bot.send_message(
                message.chat.id, 'You have entered an incorrect url adress!')

        if len(file_names_to_delete) != 0:
            Downloader.downloaderFromYT.delete_videos(file_names_to_delete)

    except Exception as err:
        print("Unexpected error! >>> ", err)
        bot.send_message(
            message.chat.id, f'There is an unexpected error! >>> {err}')

    continue_downloading(message)


bot.polling()
