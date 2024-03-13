import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram import types
import sys
import logging
from aiogram.filters import CommandStart
#from __future__ import unicode_literal
from config import Token
import yt_dlp
import os
import time
import asyncio

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()




class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
	def __init__(self):
		super(FilenameCollectorPP, self).__init__(None)
		self.filenames = []

	def run(self, information):
		self.filenames.append(information["filepath"])
		return [], information

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
	await message.answer("Hello, world!")

@dp.message()
async def search(message: types.Message):
	arg = message.get_url()
	await message.reply('Ожидайте...')
	YDL_OPTIONS = {'format': 'bestaudio/best',
		'noplaylist':'True',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192'
		}],
	}
	with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
		try:
			video = ydl.extract_info(arg, download=True) 
		except:
			filename_collector = FilenameCollectorPP()
			ydl.add_post_processor(filename_collector)
			video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
			await message.reply_audio(open(filename_collector.filenames[0], 'rb'))
			await message.reply(f'Файл был отправлен!\nСпасибо за использование бота\n\n__{arg}__')
			time.sleep(5)
			os.remove(filename_collector.filenames[0])

		else:
			video = ydl.extract_info(arg, download=True)

		return filename_collector.filenames[0]

@dp.message()
async def youtube(message: types.Message):
	arguments = message.get_args()
	await message.reply("Ожидайте...")
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		filename_collector = FilenameCollectorPP()
		ydl.add_post_processor(filename_collector)
		video = ydl.extract_info(arguments,download=True)


		await message.reply_document(open(filename_collector.filenames[0], 'rb'))
		await message.reply(f'Файл был отправлен!\nСпасибо за использование бота\n\n__{arguments}__')
		time.sleep(5)
		os.remove(filename_collector.filenames[0])
		return filename_collector.filenames[0]

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(Token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())