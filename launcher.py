import discord
import const
import os
import config
import time

CATEGORY_SORTED_TXT = const.CATEGORY_SORTED_TXT
BASE_CATEGORY_ID = const.BASE_CATEGORY_ID
ACCESS_TOKEN = const.ACCESS_TOKEN
GUILD_ID = const.GUILD_ID
CHECK_CHANNEL = const.CHECK_CHANNEL

intents = discord.Intents.default()
client = discord.Client(intents=intents)


# 起動時に動作する処理
@client.event
async def on_ready():
    print('ログインしました。')
    channel = client.get_channel(CHECK_CHANNEL)
    await channel.send("on ready")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    # # 「@Botちゃん /join <channel.id>」でBotがvcチャンネルに参加
    # if message.content.split()[1] == '/join':
    #     vc_channel = client.get_channel(int(message.content.split()[2]))
    #     await vc_channel.connect()

    # # 「@Botちゃん /join <channel.id>」でBotがvcチャンネルから離脱
    # if message.content.split()[1] == '/leave':
    #     await message.guild.voice_client.disconnect()


@client.event
# vcチャンネルに変更があった際に動作する処理
async def on_voice_state_update(member,before,after):
    # 同じチャンネル内での変化（マイクミュートなど）の場合、無視
    if before.channel == after.channel:
        pass
    # それ以外の場合
    else:
        # ソート済みのカテゴリーリストを取得
        category_sorted = []
        with open(CATEGORY_SORTED_TXT, "r") as f:
            for line in f:
                category_sorted.append(int(line.strip()))
        category_sort_dict = dict()
        # カテゴリの順番を扱いやすいよう辞書に登録
        for category_position, category_id in enumerate(category_sorted):
            category_sort_dict[category_id] = category_position
        
        categories = client.get_guild(GUILD_ID).categories
        category_list = []
        for category in categories:
            category_members = sum([len(channel.members) for channel in category.voice_channels])
            # [カテゴリの人数, カテゴリの元の位置, カテゴリのid]
            category_list.append([category_members, -category_sort_dict[category.id], category.id])
        
        category_list.sort(reverse=True)
        for position, [category_members, category_origin_position, category_id] in enumerate(category_list):
            category = client.get_channel(category_id)
            category_now_position = category.position
            if category_now_position != position:
                await category.edit(position=position)

# Botの起動とDiscordサーバーへの接続
client.run(ACCESS_TOKEN)