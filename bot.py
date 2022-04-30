"""
MIT License
Copyright (C) 2021-2022 MetaVoid (MoeZilla) 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging

from telegram import Update,ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient
import os


BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")
Chat_Group = [-1001773806532]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger("tlb")




levellink =["https://telegra.ph/file/6620fe683ff3989268c7f.mp4", "https://telegra.ph/file/c6bbce91cb75d4ab318ae.mp4", "https://telegra.ph/file/c2ac7b63d248f49da952c.mp4", "https://telegra.ph/file/b100466a5f0c42fa7255f.mp4", "https://telegra.ph/file/67c9dc7b59f78aa7aaf4c.mp4", "https://telegra.ph/file/06e2d74343e89c9d3cd12.mp4", "https://telegra.ph/file/88458a18eea8e86292b14.mp4", "https://telegra.ph/file/e3786d4f321ff4335a70f.mp4"]
levelname = ["Team Rocket", "Stray God", "Vector", "Hero Association", "Z Warrior", "Black Knight", "Ghoul", "Overlord"]
levelnum = [2,5,15,25,35,50,70,100]



def level(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = message.chat.id
    user_id = message.from_user.id    
    user = update.effective_user
    leveldb = MongoClient(MONGO_URL)
    
    level = leveldb["LevelDb"]["Level"] 
 
    if message.chat.id in Chat_Group:
        xpnum = level.find_one({"level": user_id})

        if not message.from_user.is_bot:
            if xpnum is None:
                newxp = {message = update.effective_message"level": user_id, "xp": 10}
                level.insert_one(newxp)   
                    
            else:
                xp = xpnum["xp"] + 10
                level.update_one({"level": user_id}, {
                    "$set": {"xp": xp}})
                l = 0
                while True:
                    if xp < ((50*(l**2))+(50*(l))):
                         break
                    l += 1
                xp -= ((50*((l-1)**2))+(50*(l-1)))
                if xp == 0:
                    message.reply_text(f"🌟 {user.mention_html()}, You have reached level {l}**, Nothing can stop you on your way!",parse_mode=ParseMode.HTML)
    
                    for lv in range(len(levelname)) and range(len(levellink)):
                            if l == levelnum[lv]:            
                                Link = f"{levellink[lv]}"
                                message.reply_video(video=Link, caption=f"{user.mention_html()}, You have reached Rank Name **{levelname[lv]}**",parse_mode=ParseMode.HTML)
                  

                               

def rank(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = message.chat.id
    user_id = message.from_user.id    
    user = update.effective_user
    leveldb = MongoClient(MONGO_URL)
    
    level = leveldb["LevelDb"]["Level"] 
    
    if message.chat.id in Chat_Group:
        xpnum = level.find_one({"level": user_id})
        xp = xpnum["xp"]
        l = 0
        r = 0
        while True:
            if xp < ((50*(l**2))+(50*(l))):
                break
            l += 1

        xp -= ((50*((l-1)**2))+(50*(l-1)))
        rank = level.find().sort("xp", -1)
        for k in rank:
            r += 1
            if xpnum["level"] == k["level"]:
                break                     
        message.reply_text(f"{user.mention_html()},Level Info:\nLevel: {l}\nProgess: {xp}/{int(200 *((1/2) * l))}\n Ranking: {r}",parse_mode=ParseMode.HTML)






def main():
    updater = Updater("BOT_TOKEN")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("rank", rank))
    dispatcher.add_handler(MessageHandler(Filters.all & Filters.chat_type.groups , level))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
