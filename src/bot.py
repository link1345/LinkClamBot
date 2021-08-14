
import config.BaseSetting # token 設定場所

from base.base import LinkClanBot

if __name__ == '__main__':

    base = LinkClanBot()

#    intents = discord.Intents.default()
#	intents.members = True
#	intents.guilds = True

#	base = LinkClanBot.BotBase()
#	base.client = discord.Client(intents=intents)


    base.run()