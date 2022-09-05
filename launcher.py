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
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content.split()[1] == '/join':
        vc_channel = client.get_channel(int(message.content.split()[2]))
        print(vc_channel)
        await vc_channel.connect()

    if message.content.split()[1] == '/leave':
        await message.guild.voice_client.disconnect()
        

@client.event
async def on_voice_state_update(member,before,after):
    #したいこと
    #特定のチャンネルに入室した際、入室者が一人目だった場合にテキストチャンネルへの通知を出す

    #テキストチャンネルのidが入った変数(仮)：text_channel_id
    #入室を検知したいボイスチャンネルのidが入った変数(仮)：voice_channel_id
    if before.channel == after.channel:#同じチャンネル内での変化（マイクミュートなど）の場合
        pass#無視
    else:#それ以外の場合
        try:
            if len(after.channel.members) == 1:#入室者が一人目の場合
                send_message_content = "```" + member.display_name + "が「"+ after.channel.name + "」に一人目として接続しました。```"
                print(send_message_content)
                if after.channel.category.id != config.BASE_CATEGORY_ID:
                    await after.channel.category.edit(position=0)
        except AttributeError:
            pass

        try:
            if len(before.channel.members) == 0:
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