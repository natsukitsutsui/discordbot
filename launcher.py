import discord
import const
import os
import config

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
    print(message.content)
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    # # 「@Botちゃん /join <channel.id>」でBotがvcチャンネルに参加
    # if message.content.split()[1] == '/join':
    #     vc_channel = client.get_channel(int(message.content.split()[2]))
    #     print(vc_channel)
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
        try:
            # 入室者が一人目の場合
            if len(after.channel.members) == 1:
                send_message_content = "```" + member.display_name + "が「"+ after.channel.name + "」に一人目として接続しました。```"
                print(send_message_content)
                if after.channel.category.id != BASE_CATEGORY_ID:
                    await after.channel.category.edit(position=0)
        except AttributeError:
            pass

        try:
            #vcチャンネルに誰もいなくなった場合
            if len(before.channel.members) == 0:
                #同じカテゴリの他のvcに人がいる場合、ポジションを変えない
                channel_list = before.channel.category.voice_channels
                position_reset_flag = True
                for channel in channel_list:
                    if len(channel.members) > 0:
                        position_reset_flag = False
                if position_reset_flag:
                    send_message_content = "```" + member.display_name + "が「"+ before.channel.name + "」から切断されました。```"
                    print(send_message_content)
                    if before.channel.category.id != BASE_CATEGORY_ID:
                        category_sorted = []
                        # ソート済みのカテゴリーリストを取得
                        with open(CATEGORY_SORTED_TXT, "r") as f:
                            for line in f:
                                category_sorted.append(int(line.strip()))
                        category_sort_dict = dict()

                        #カテゴリの順番を扱いやすいよう辞書に登録
                        for category_position, category_id in enumerate(category_sorted):
                            category_sort_dict[category_id] = category_position

                        #カテゴリの元のpositionより大きい値のpositionが出現したらそこに挿入
                        guild = client.get_guild(GUILD_ID)
                        category_list = [[category.id, category.position] for category in guild.categories]
                        print(category_list)
                        category_base_flag = False
                        for [category_id, category_position] in category_list:
                            try :
                                if category_base_flag and category_sort_dict[category_id] > category_sort_dict[before.channel.category.id]:
                                    await before.channel.category.edit(position=category_position)
                                    break
                            except KeyError:
                                await before.channel.category.edit(position=len(category_list)-1)
                            if category_id == BASE_CATEGORY_ID:
                                category_base_flag = True

        except AttributeError:
            pass

# Botの起動とDiscordサーバーへの接続
client.run(ACCESS_TOKEN)