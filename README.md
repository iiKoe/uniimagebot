# uniimagebot
A [Telegram](https://telegram.org/) bot that converts text with Unicode 9 characters to an image.

The bot is implemented using python 2.7 in combination with [telepot](https://github.com/nickoala/telepot)

The bot can be added to telegram by going to: www.telegram.me/uniimagebot.

To run the bot yourself<sup>*</sup> you need python 2.7, the telepot python library and [imagemagic](http://www.imagemagick.org) (called through bash). You need to request a bot token from the telegram BotFather. The command you need to run to start the bot is:
```bash
$ python2 uniimage.py TOKEN
```

<sup>*</sup>The uniimagebot analyzes all messages that are send to it. So if you plan on running it within a group chat with admin right so it can see the messages, I suggest you clone the repo, get your own token and host it yourself for privacy reasons (The bot does not save anny messages, but why trust me).
