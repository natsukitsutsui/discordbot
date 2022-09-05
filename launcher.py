import discord
import config


intents = discord.Intents.default()
client = discord.Client(intents=intents)


# 起動時に動作する処理
@client.event
async def on_ready():
    print('ログインしました。')


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
                if after.channel.category.id != config.BASE_CATEGORY_ID:
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
                    if before.channel.category.id != config.BASE_CATEGORY_ID:
                        base_channel = client.get_channel(config.BASE_CATEGORY_ID)
                        base_position = base_channel.position
                        await before.channel.category.edit(position=base_position+1)
        except AttributeError:
            pass

# Botの起動とDiscordサーバーへの接続
client.run(config.ACCESS_TOKEN)