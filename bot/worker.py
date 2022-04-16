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
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from .FastTelethon import download_file, upload_file
from .funcn import *
from .util import get_readable_file_size
from .worker import *

## SOME VARIABLES ##
LOZ = -1001728993522
h = 1280
w = 1720
## DURATION ##


## LOGS ##

async def getlogs(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return
    await event.client.send_file(event.chat_id, file=LOG_FILE_NAME, force_document=True)


async def clean(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return
    await event.reply("Cleared Queued, Working Files and Cached Downloads !")
    WORKING.clear()
    QUEUE.clear()
    os.system("rm -rf downloads/*")
    os.system("rm -rf encode/*")
    for proc in psutil.process_iter():
        processName = proc.name()
        processID = proc.pid
        print(processName, " - ", processID)
        if processName == "ffmpeg":
            os.kill(processID, signal.SIGKILL)
    return


async def restart(event):
    if str(event.sender_id) not in OWNER:
        await asyncio.sleep(5)
    try:
        await event.reply("Restarting Please Wait…")
        os.system("kill -9 -1")
    except Exception as err:
        await event.reply("Error Occurred")
        LOGS.info(str(err))


async def getthumb(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return
    await event.client.send_file(
        event.chat_id,
        file="/bot/thumb.jpg",
        force_document=False,
        caption="Your Current Thumbnail. 🎥",
    )


async def clearqueue(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return
    await event.reply("Cleared Queued Files ! 👳‍♂️")
    QUEUE.clear()
    return


async def thumb(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.reply_text("Well That Ain't Right!")
    if not event.photo:
        return
    os.system("rm thumb.jpg")
    await event.client.download_media(event.media, file="/bot/thumb.jpg")
    await event.reply("Thumbnail Saved Successfully 🎥")


async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, id = wh.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(Path(dl).stat().st_size))
        ed = dt.now()
        name = dl.split("/")[1]
        input = (name[:45] + "…") if len(name) > 45 else name
        currentTime = ts(int((ed - uptime).seconds) * 1000)
        total, used, free = shutil.disk_usage(".")
        total = get_readable_file_size(total)
        used = get_readable_file_size(used)
        free = get_readable_file_size(free)
        get_readable_file_size(psutil.net_io_counters().bytes_sent)
        get_readable_file_size(psutil.net_io_counters().bytes_recv)
        cpuUsage = psutil.cpu_percent(interval=0.5)
        psutil.virtual_memory().percent
        psutil.disk_usage("/").percent
        ans = f"CPU: {cpuUsage}%\n\nTotal Disk Space:\n{total}\n\nDownloaded:\n{ov}\n\nFileName:\n{input}\n\nCompressing:\n{ot}\n\nBot Uptime:\n{currentTime}\n\nUsed: {used}  Free: {free}"
        await e.answer(ans, cache_time=0, alert=True)
    except Exception as er:
        LOGS.info(er)
        ed = dt.now()
        currentTime = ts(int((ed - uptime).seconds) * 1000)
        total, used, free = shutil.disk_usage(".")
        total = get_readable_file_size(total)
        info = f"Error 404: File | Info not Found 🤔\nMaybe Bot was restarted\nKindly Resend Media\n\nOther Info\n═══════════\nBot Uptime: {currentTime}\n\nTotal Disk Space: {total}"
        await e.answer(
            info,
            cache_time=0,
            alert=True,
        )


async def dl_link(event):
    if not event.is_private:
        return
    if str(event.sender_id) not in OWNER:
        return
    link, name = "", ""
    try:
        link = event.text.split()[1]
        name = event.text.split()[2]
    except BaseException:
        pass
    if not link:
        return
    if WORKING or QUEUE:
        QUEUE.update({link: name})
        return await event.reply(
            f"Added {link} in QUEUE !! Compressing Will Start Soon 🗜️"
        )
    WORKING.append(1)
    s = dt.now()
    xxx = await event.reply(
        "Downloding Queue Files 📁 !! Please Wait ⌛ \n Join @FIERCENETWORK`"
    )
    try:
        dl = await fast_download(xxx, link, name)
    except Exception as er:
        WORKING.clear()
        LOGS.info(er)
        return
    es = dt.now()
    kk = dl.split("/")[-1]
    aa = kk.split(".")[-1]
    rr = "encode"
    bb = kk.replace(f".{aa}", " [FIERCENETWORK].mkv")
    out = f"{rr}/{bb}"
    thum = "thumb.jpg"
    dtime = ts(int((es - s).seconds) * 1000)
    hehe = f"{out};{dl};0"
    wah = code(hehe)
    nn = await xxx.edit(
        "Encoding In Progress 🗜️",
        buttons=[
            [Button.inline("PERCENTAGE 🔣", data=f"stats{wah}")],
            [Button.inline("SKIP ⏭️", data=f"skip{wah}")],
        ],
    )
    cmd = FFMPEG.format(dl, out)
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await xxx.edit(str(er) + "\n\n**ERROR** Contact @Nirusaki")
            WORKING.clear()
            os.remove(dl)
            return os.remove(out)
    except BaseException:
        pass
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await xxx.client.send_message(xxx.chat_id, "▲ Uploading Started ▲")
    with open(out, "rb") as f:
        ok = await upload_file(
            client=xxx.client,
            file=f,
            name=out,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "🔺 Uploading The File 📁 🔺")
            ),
        )
    out.split("/")[1]
    ds = await xxx.client.send_file(
        xxx.chat_id,
        file=ok,
        supports_streaming=True,
        thumb=thum,
        caption=bb,
        height=h,
        width=w,
    )
    await nnn.delete()
    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    a1 = await info(dl, xxx)
    a2 = await info(out, xxx)
    dk = await ds.reply(
        f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nMediainfo: [Before]({a1})//[After]({a2})\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}",
        link_preview=False,
    )
    await ds.forward_to(LOZ)
    await dk.forward_to(LOZ)
    os.remove(dl)
    os.remove(out)
    WORKING.clear()


async def encod(event):
    try:
        if not event.is_private:
            return
        if str(event.sender_id) not in OWNER:
            return
        if not event.media:
            return
        if hasattr(event.media, "document"):
            if not event.media.document.mime_type.startswith(
                ("video", "application/octet-stream")
            ):
                return
        else:
            return
        try:
            oc = event.fwd_from.from_id.user_id
            occ = (await event.client.get_me()).id
            if oc == occ:
                return await event.reply("I Know What You Are Trying To Do Kid 😑😑.")
        except BaseException:
            pass
        if WORKING or QUEUE:
            xxx = await event.reply("Added To Queue !! Please Be Patient ⏰")
            # id = pack_bot_file_id(event.media)
            doc = event.media.document
            if doc.id in list(QUEUE.keys()):
                return await xxx.edit("Duplicate File Detected \n Dont Waste My Time ⏰")
            name = event.file.name
            if not name:
                name = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
            QUEUE.update({doc.id: [name, doc]})
            return await xxx.edit(
                "Added To Queue ⏰, \nPlease Wait ,Encoding Will Start Soon ⏰"
            )
        WORKING.append(1)
        xxx = await event.reply("Download Pending… \n**(Waiting For Connection)**")
        s = dt.now()
        ttt = time.time()
        dir = f"downloads/"
        try:
            if hasattr(event.media, "document"):
                file = event.media.document
                filename = event.file.name
                if not filename:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
                dl = dir + filename
                with open(dl, "wb") as f:
                    ok = await download_file(
                        client=event.client,
                        location=file,
                        out=f,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                xxx,
                                ttt,
                                "Downloading Started ⬇️",
                            )
                        ),
                    )
            else:
                dl = await event.client.download_media(
                    event.media,
                    dir,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, xxx, ttt, "Downloading Started ⬇️")
                    ),
                )
        except Exception as er:
            WORKING.clear()
            LOGS.info(er)
            return os.remove(dl)
        es = dt.now()
        kk = dl.split("/")[-1]
        aa = kk.split(".")[-1]
        rr = f"encode"
        bb = kk.replace(f".{aa}", " [FIERCENETWORK].mkv")
        out = f"{rr}/{bb}"
        thum = "thumb.jpg"
        dtime = ts(int((es - s).seconds) * 1000)
        e = xxx
        hehe = f"{out};{dl};0"
        wah = code(hehe)
        nn = await e.edit(
            "**Encoding Files… \n ⏳ This Might Take A While ⏳**",
            buttons=[
                [Button.inline("PERCENTAGE 🔣", data=f"stats{wah}")],
                [Button.inline("SKIP ⏭️", data=f"skip{wah}")],
            ],
        )
        cmd = FFMPEG.format(dl, out)
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        er = stderr.decode()
        try:
            if er:
                await e.edit(str(er) + "\n\n**ERROR** Contact @Nirusaki")
                WORKING.clear()
                os.remove(dl)
                return os.remove(out)
        except BaseException:
            pass
        ees = dt.now()
        ttt = time.time()
        await nn.delete()
        nnn = await e.client.send_message(e.chat_id, "**▲ Uploading ▲**")
        with open(out, "rb") as f:
            ok = await upload_file(
                client=e.client,
                file=f,
                name=out,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, nnn, ttt, "**🔺 Uploading 🔺**")
                ),
            )
        out.split("/")[1]
        ds = await e.client.send_file(
            e.chat_id,
            file=ok,
            supports_streaming=True,
            thumb=thum,
            caption=bb,
            height=h,
            width=w,
        )
        await nnn.delete()
        org = int(Path(dl).stat().st_size)
        com = int(Path(out).stat().st_size)
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}") + "%"
        eees = dt.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        a1 = await info(dl, e)
        a2 = await info(out, e)
        dk = await ds.reply(
            f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nMediainfo: [Before]({a1})//[After]({a2})\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}",
            link_preview=False,
        )
        await ds.forward_to(LOZ)
        await dk.forward_to(LOZ)
        os.remove(dl)
        os.remove(out)
        WORKING.clear()
    except BaseException as er:
        LOGS.info(er)
        WORKING.clear()
