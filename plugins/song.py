import os
import time
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("I'm helping download your lovely songs on Telegram🎸🎸🎸.[🎶](https://telegra.ph/file/507fa8e980c6274aa1a59.jpg)Do you want to know more about me hit the @SlTeleBots.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝓤𝓹𝓭𝓪𝓽𝓮 𝓒𝓱𝓪𝓷𝓷𝓮𝓵🔔', url='https://t.me/SLTeleBots'),
                    InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['help']))
async def help(client, message):
       await message.reply("<b>Hit help button  to find more about how to use me... 𝒮𝑒𝓃𝒹 - /𝒽𝑒𝓁𝓅 </i>\n\n<b>Eg</b> `/song Faded`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Developer', url='https://t.me/ViharaSenindu')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply("➪<b>Name</b> : ✫<i>Music Downloader</i>\n➪<b>Developer</b> : ✫[Vihara Senindu](https://t.me/ViharaSenindu)\n➪<b>Language</b> : ✫<i>Python3</i>\n➪<b>Server</b> : ✫[𝘏𝘦𝘳𝘰𝘬𝘶](https://heroku.com/)\n➪<b>Source Code</b> : ✫[𝘊𝘭𝘪𝘤𝘬 𝘏𝘦𝘳𝘦](https://github.com/viharasenindu)",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply('🔎 Searching Your Song...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"MusicDownloadv2bot" 
            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('𝓢𝓸𝓻𝓻𝔂 𝓝𝓸𝓽 𝓕𝓸𝓾𝓷𝓭 𝓨𝓸𝓾𝓻 𝓢𝓸𝓷𝓰')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐹𝑜𝑢𝑛𝑑 𝑁𝑜𝑡ℎ𝑖𝑛𝑔.\n\nEg.`Faded`"
        )
        print(str(e))
        return
    m.edit("`𝓤𝓹𝓵𝓸𝓪𝓭𝓲𝓷𝓰 𝓨𝓸𝓾𝓻 𝓢𝓸𝓷𝓰,𝓟𝓵𝓮𝓪𝓼𝓮 𝓦𝓪𝓲𝓽...`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'🎧 𝓣𝓲𝓽𝓵𝓮 : [{title[:35]}]({link})\n⏳ 𝓓𝓾𝓻𝓪𝓽𝓲𝓸𝓷 : `{duration}`\n👀 𝓥𝓲𝓮𝔀𝓼 : `{views}`\n\n📮 𝗕𝘆: {message.from_user.mention()}\n📤 𝗕𝘆 : @RolexXTm2'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('𝓕𝓪𝓲𝓵𝓮𝓭\n\n`𝓟𝓵𝓮𝓼𝓪𝓼𝓮 𝓣𝓻𝔂 𝓐𝓰𝓪𝓲𝓷 𝓛𝓪𝓽𝓮𝓻`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
