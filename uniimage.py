"""
$ python2.7 uniimage.py <token>

Author: Vito Kortbeek
UniImageBot: An unicode 9 emoji to image converter - You send a message containg
an unicode 9 emoji, an image of the message including the emoji is generated as 
send as a photo. This is for users of systems which don't have unicode 9 emoji's.

Caution: Python's treatment of unicode characters longer than 2 bytes (which
most emojis are) varies across versions and platforms.

- Uses ImageMagick to create and convert the images
- Emoji png images are extracted from the Google Noto Font
"""

import sys
import time
import telepot
import telepot.namedtuple
import subprocess
import os
import codecs

EmojiList = []
def load_options():
    f = codecs.open('unicode9.txt', encoding='utf-8')
    for line in f:
        code = line.replace("\n", "")
        EmojiList.append(code)
        #print repr(code)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    if content_type == 'text':
        img_list = []
        text_list = []
        text_str = ""
        img_str = ""
        text_img_str = ""
        text_count = 0
        is_unicode = False

        for uni_char in msg['text'][:128]:
            uni = uni_char.encode('unicode-escape').decode('ascii')

            # Get image from folder
            uni_img_name = "emoji_" + uni.replace("\\", "").replace("U000", "u") + ".png"
            uni_img_path = "font-images/" + uni_img_name
            if os.path.isfile(uni_img_path):
                if uni_char in EmojiList:
                    is_unicode = True
                if text_str.isspace():
                    text_str = "" #TODO spaces between emoji will now be removed
                text_list.append((text_str, uni_img_path))
                text_str = ""
            else:
                text_str += uni.encode("utf8")
        
        if text_str.isspace():
            text_str = "_"
        text_list.append((text_str, ""))
        
        if is_unicode == True:
            if chat_id < 0:
                # group message
                print 'Received a %s from %s, by %s' % (content_type, m.chat, m.from_)
            else:
                # private message
                print 'Received a %s from %s' % (content_type, m.chat)  # m.chat == m.from_

            for text, image in text_list:
                if text:
                    # Create text image
                    process = subprocess.Popen(["convert", "-pointsize", "100", "-font", 
                        "/usr/share/fonts/TTF/DejaVuSans.ttf", "label:" + text,
                        str(text_count) + ".png"], stdout=subprocess.PIPE)
                    output, error = process.communicate()
                    text_img_str += str(text_count) + ".png "
                    img_str += str(text_count) + ".png "
                    text_count+=1

                if image:
                    img_str += image + " "
                    
            # concatonate the images
            bash_command = "convert " + img_str + " +append uniimg.png"
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            # Resize if needed
            bash_command = "identify -format %w uniimg.png"
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print "Image size: " + output
            try:
                if int(output) > 1920:
                    print "Too large, resizing"
                    bash_command = "convert uniimg.png -resize 1920 -extent 1920x100 uniimg.png"
                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
            except TypeError:
                print "Type error"

            # Send the final image
            img = open('uniimg.png', 'rb')
            try:
                bot.sendPhoto(chat_id, ('uniimg.png', img), disable_notification=True)

                print "Unicode image message is send"
            except:
                bot.sendMessage(chat_id, "Yea, thats a bit too extreme for telegram I'm afraid")
                print "An error occured during sending"

        # Remove temp text images
        if is_unicode:
            for x in range(0, text_count):
                os.remove(str(x) + ".png")
            os.remove("uniimg.png")

TOKEN = sys.argv[1]  # get token from command-line

load_options()

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)
