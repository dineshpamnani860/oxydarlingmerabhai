from os import path

import OxyXmusic.services.converter
from OxyXmusic.config import DURATION_LIMIT
from OxyXmusic.services.downloaders import youtube

from OxyXmusic import Client
from OxyXmusic.callsmusic import callsmusic, queues
from OxyXmusic.helpers.decorators import errors
from OxyXmusic.helpers.errors import DurationLimitError
from OxyXmusic.helpers.filters import command, other_filters
from OxyXmusic.helpers.gets import get_file_name, get_url
from OxyXmusic.pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from OxyXmusic.types import Message


@Client.on_message(command("ply") & other_filters)
@errors
async def play(_, message: Message):

    lel = await message.reply("🔄 **Processing**")
    message.from_user.id
    message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔥𝕐𝖔𝖚𝖗 - 𝕯𝖆𝖉𝖉𝕪🔥", url="https://t.me/FallenAngel_xD"
                )
            ]
        ]
    )

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ {DURATION_LIMIT} minute(s) se bada video..😮 mai nhi play karta ja..🙄"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("❗ Abey play karne kuch de to sahi noob 😂")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await lel.edit(f"#⃣ **Queued** at position {position}!")
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo="https://telegra.ph/file/fa90d4ed2fac4f5300d76.jpg",
            reply_markup=keyboard,
            caption="▶️ **Playing** here the song requested by🔥{}!".format(
                message.from_user.mention()
            ),
        )
        return await lel.delete()
