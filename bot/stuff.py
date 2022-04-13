#    This file is part of the CompressorQueue distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/1Danish-00/CompressorQueue/blob/main/License> .

import shutil

import psutil

from .util import get_readable_file_size
from .worker import *


async def detail(event):
    await event.reply(
        f"""
**Available Commands 🤖**
/start - __Check Bot is Working Or Not__
/help - __Get Detailed Help__
/logs - __Get Bot Logs__
/ping - __Check Ping__
/status - __Get System Info__
/link - __Download From Link__
/cancelall - __Clear Cached Downloads and Queued files__
/clear - __Clear Queued Files__
/showthumb - __Show Current Thumbnail__
/eval - __Execute An Argument__
/bash - __Run Bash Commands__
/cmds - __Show This List Again__
"""
    )


async def up(event):
    if not event.is_private:
        return
    stt = dt.now()
    ed = dt.now()
    v = ts(int((ed - uptime).seconds) * 1000)
    ms = (ed - stt).microseconds / 1000
    p = f"🌋Pɪɴɢ = {ms}ms"
    await event.reply(v + "\n" + p)


async def status(event):
    if not event.is_private:
        return
    ed = dt.now()
    currentTime = ts(int((ed - uptime).seconds) * 1000)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    await event.reply(
        f"**Bot Uptime:** `{currentTime}`\n"
        f"**Total Disk Space:** `{total}`\n"
        f"**Used:** `{used}` "
        f"**Free:** `{free}`\n\n"
        f"**Upload:** `{sent}`\n"
        f"**Download:** `{recv}`\n\n"
        f"**CPU:** `{cpuUsage}%` "
        f"**RAM:** `{memory}%` "
        f"**DISK:** `{disk}%`"
    )


async def start(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`\n This Is A Video Compressor Bot Created By Danish Edited By Nirusaki\n It Can Compress Videos Much Effiecently Than Any Bot Because \n Of The Queue System Built Into It",
        buttons=[
            [Button.inline("HELP", data="ihelp")],
            [
                Button.url("SOURCE (Original)", url="github.com/1Danish-00/"),
                Button.url("DEVELOPER", url="t.me/danish_00"),
            ],
            [Button.url("Maintainer ✌️", url="t.me/nirusaki")],
        ],
    )


async def help(event):
    await event.reply(
        "This Is A Video Compressor Bot Created By Danish Edited By Nirusaki\n It Can Compress Videos Much Effiecently Than Any Bot Because \n Of The Queue System Built Into It"
    )


async def ihelp(event):
    await event.edit(
        "This Is A Video Compressor Bot Created By Danish Edited By Nirusaki\n It Can Compress Videos Much Effiecently Than Any Bot Because \n Of The Queue System Built Into It",
        buttons=[Button.inline("BACK", data="beck")],
    )


async def beck(event):
    await event.edit(
        f"Hi `{event.sender.first_name}`\n  This Is A Video Compressor Bot Created By Danish Edited By Nirusaki\n It Can Compress Videos Much Effiecently Than Any Bot Because \n Of The Queue System Built Into It",
        buttons=[
            [Button.inline("HELP", data="ihelp")],
            [
                Button.url("SOURCE (Original)", url="github.com/1Danish-00/"),
                Button.url("DEVELOPER", url="t.me/danish_00"),
            ],
            [Button.url("Maintainer ✌️", url="t.me/nirusaki")],
        ],
    )
