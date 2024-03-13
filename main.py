# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.enums import ParseMode
# from aiogram import types
# import sys
# import logging
# from aiogram.filters import CommandStart
# #from __future__ import unicode_literal
# import yt_dlp
# import os
# import time
# import asyncio

# logging.basicConfig(level=logging.INFO)

# dp = Dispatcher()




# class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
# 	def __init__(self):
# 		super(FilenameCollectorPP, self).__init__(None)
# 		self.filenames = []

# 	def run(self, information):
# 		self.filenames.append(information["filepath"])
# 		return [], information

# @dp.message(CommandStart())
# async def send_welcome(message: types.Message):
# 	await message.answer("Hello, world!")

# @dp.message()
# async def search(message: types.Message):
# 	arg = message.text
# 	await message.reply('Ожидайте...')
# 	YDL_OPTIONS = {'format': 'bestaudio/best',
# 		'noplaylist':'True',
# 		'postprocessors': [{
# 			'key': 'FFmpegExtractAudio',
# 			'preferredcodec': 'mp3',
# 			'preferredquality': '192'
# 		}],
# 	}
# 	with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
# 		try:
# 			video = ydl.extract_info(arg, download=True) 
# 		except:
# 			filename_collector = FilenameCollectorPP()
# 			ydl.add_post_processor(filename_collector)
# 			video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
# 			await message.reply_audio(open(filename_collector.filenames[0], 'rb'))
# 			await message.reply(f'Файл был отправлен!\nСпасибо за использование бота\n\n__{arg}__')
# 			time.sleep(5)
# 			os.remove(filename_collector.filenames[0])

# 		else:
# 			video = ydl.extract_info(arg, download=True)

# 		return filename_collector.filenames[0]

# @dp.message()
# async def youtube(message: types.Message):
# 	arguments = message.get_args()
# 	await message.reply("Ожидайте...")
# 	ydl_opts = {
# 		'format': 'bestaudio/best',
# 		'postprocessors': [{
# 			'key': 'FFmpegExtractAudio',
# 			'preferredcodec': 'mp3',
# 			'preferredquality': '192',
# 		}],
# 	}
# 	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# 		filename_collector = FilenameCollectorPP()
# 		ydl.add_post_processor(filename_collector)
# 		video = ydl.extract_info(arguments,download=True)


# 		await message.reply_document(open(filename_collector.filenames[0], 'rb'))
# 		await message.reply(f'Файл был отправлен!\nСпасибо за использование бота\n\n__{arguments}__')
# 		time.sleep(5)
# 		os.remove(filename_collector.filenames[0])
# 		return filename_collector.filenames[0]

# async def main() -> None:
#     # Initialize Bot instance with a default parse mode which will be passed to all API calls
#     bot = Bot("6885805301:AAGcnYkpGfciC65TDPodn6k2nyRLS3NQKlY", parse_mode=ParseMode.HTML)
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, CallbackQuery
from aiogram.enums import ParseMode
from io import BytesIO
import logging
import sys
import asyncio
from pytube import YouTube
from youtubesearchpython import VideosSearch

dp = Dispatcher()

markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Download", callback_data="Download")
        ]])

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет, я умею скачивать видео с YouTube! Скинь ссылку.")

@dp.message()
async def handle_youtube_link(message: types.Message):
	searchList = VideosSearch(message.text, limit = 5).result()
	searchList[0]['link']
	keyboard = []
	for element in searchList:
		print('do work')
	choose_markup =  InlineKeyboardMarkup(inline_keyboard=keyboard)
	await message.answer(message.text, reply_markup=choose_markup)

@dp.callback_query()
async def callback_handler(query: CallbackQuery):
    if query.data == "Download":
        await download_youtube_audio(query.message, query.message.text)
        return
    await query.message.answer(query.inline_message_id, reply_markup=markup)

async def download_youtube_audio(message: Message, url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        file = BufferedInputFile(buffer.getvalue(), filename=f"{yt.title}.mp3")
        await message.answer_audio(file)
    except Exception as e:
        await message.answer(f"Ошибка при скачивании или отправке видео: {str(e)}")

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token="6885805301:AAGcnYkpGfciC65TDPodn6k2nyRLS3NQKlY", parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())