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
	searchList = VideosSearch(message.text, limit = 5).result()['result']
	keyboard = []
	for element in searchList:
		keyboard.append([InlineKeyboardButton(text=element['title'], callback_data=element['link'])])
	choose_markup =  InlineKeyboardMarkup(inline_keyboard=keyboard)
	await message.answer(message.text, reply_markup=choose_markup)

@dp.callback_query()
async def callback_handler(query: CallbackQuery):
	if query.data == "Download":
		await download_youtube_audio(query.message, query.message.text)
		return
	await query.message.answer(query.data, reply_markup=markup)

async def download_youtube_audio(message: Message, url):
	try:
		yt = YouTube(url)
		stream = yt.streams.filter(only_audio=True).first()
		buffer = BytesIO()
		stream.stream_to_buffer(buffer)
		file = BufferedInputFile(buffer.getvalue(), filename=f"{yt.title}.mp3")
		await message.answer_audio(file)
		buffer.flush()
	except Exception as e:
		await message.answer(f"Ошибка при скачивании или отправке видео: {str(e)}")

async def main() -> None:
	bot = Bot(token="", parse_mode=ParseMode.HTML)
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())