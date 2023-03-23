from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:

    
    
    import discord, json, sys, time

client = discord.Client()

token = '토큰'

@client.event
async def on_connect():
    with open('./setting.json', 'r') as boo:
        data = json.load(boo)
    setting = data['percent']

    if not setting.isdecimal() or int(setting) > 100:
        print(f'수수료 퍼센트({setting})가 잘못되었습니다\nsetting.json을 수정해주세요')
        time.sleep(3)
        await client.logout()
        sys.exit()
    print(f"수수료봇 온라인\n설정된 수수료: {setting}%")


@client.event
async def on_message(message):
    if message.content.startswith("!수수료") and not message.content.startswith("!수수료수정"):
        with open('./setting.json', 'r') as boo:
            data = json.load(boo)
        setting = data['percent']

        try:
            amount = message.content.split(" ")[1]
        except IndexError:
            await message.channel.send(f'{message.author.mention} 값이 설정되지 않았습니다')
            return

        if not amount.isdecimal():
            await message.channel.send(f'{message.author.mention} 값이 숫자가 아닙니다')
            return

        result = int(amount) * (100-int(setting)) / 100
        result = round(result)
        await message.channel.send(f'{message.author.mention},\n**`{amount}`원의 수수료({setting}%)를 제외한 값은 `{result}`원입니다**')

    if message.content.startswith('!수수료수정') or message.content.startswith('!수정'):
        if message.author.guild_permissions.manage_messages:
            try:
                edit_amount = message.content.split(" ")[1]
            except:
                embed = discord.Embed(title='!수수료수정 [숫자]', description='')
                await message.channel.send(embed=embed)
                return

            if not edit_amount.isdecimal() or int(edit_amount) > 100:
                embed = discord.Embed(title='!수수료수정 [숫자]', description='')
                await message.channel.send(embed=embed)
                return

            with open('./setting.json', 'r') as boo:
                data = json.load(boo)
            data['percent'] = edit_amount
            with open('./setting.json', 'w', encoding='utf-8') as making:
                json.dump(data, making, indent="\t")
            s = data['percent']
            await message.channel.send(f'수수료가 `{s}`%로 수정되었습니다')

client.run(token)
