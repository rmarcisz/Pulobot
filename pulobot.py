import discord
import random
import os
import qrcode
import json
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client(intents=discord.Intents.default())

all_gg = {'gg4': {'strategies': ['Cloak and Dagger', 'Stuff the Ballots', 'Raid the Vaults', 'Plant Explosives'], 'schemes': ['Let Them Bleed', 'Death Beds', 'Power Ritual', 'In Your Face', 'Deliver a Message', 'Outflank', 'Hold Up Their Forces', 'Espionage', 'Sweating Bullets', 'Information Overload', 'Take Prisoner', 'Protected Territory', 'Ensnare'], 'deployments': ['Standard', 'Wedge', 'Flank', 'Corner']}, 'gg3': {'strategies': ['Carve a Path', 'Guard the Stash', 'Covert Operation', 'Cursed Objects'], 'schemes': ['Breakthrough', 'Vendetta', 'Assassinate', 'Leave Your Mark', 'Sabotage', 'Hidden Martyrs', 'Catch and Release', 'Spread Them Out', '''Load 'Em Up''', 'Public Demonstration', 'Set the Trap', 'In Your Face', 'Secret Meetup'], 'deployments': ['Standard', 'Wedge', 'Flank', 'Corner']}, 'gg2': {'strategies': ['Corrupted Ley Lines', 'Symbols of Authority', 'Break the Line', 'Turf War'], 'schemes': ['Breakthrough', 'Detonate Charges', 'Vendetta', 'Assassinate', 'Claim Jump', 'Hidden Martyrs', 'Death Beds', 'Catch and Release', 'Let Them Bleed', 'Outflank', 'Research Mission', 'Spread Them Out', 'Bait and Switch'], 'deployments': ['Standard', 'Wedge', 'Flank', 'Corner']}, 'gg1': {'strategies': ['Corrupted Ley Lines', 'Symbols of Authority', 'Recover Evidence', 'Public Enemies'], 'schemes': ['Breakthrough', 'Take Prisoner', 'Vendetta', 'Assassinate', 'Claim Jump', 'Hidden Martyrs', 'Sabotage', 'Catch and Release', 'Let Them Bleed', 'Leave Your Mark', 'Research Mission', 'Spread Them Out', 'Runic Biding'], 'deployments': ['Standard', 'Wedge', 'Flank', 'Corner']}, 'gg0': {'strategies':['Turf War', 'Plant Explosives', 'Corrupted Idols', 'Reckoning'], 'schemes':['Detonate Charges', 'Breakthrough', 'Harness the Ley Line', 'Search the Ruins', 'Dig Their Graves', 'Hold Up Their Forces', 'Take Prisoner', 'Power Ritual' , 'Outflank', 'Assassinate', 'Deliver a Message', 'Claim Jump', 'Vendetta'], 'deployments': ['Standard', 'Wedge', 'Flank', 'Corner']}, 'ggall': {'strategies': ['Cloak and Dagger', 'Stuff the Ballots', 'Raid the Vaults', 'Plant Explosives', 'Carve a Path', 'Guard the Stash', 'Covert Operation', 'Cursed Objects', 'Corrupted Ley Lines', 'Symbols of Authority', 'Break the Line', 'Turf War', 'Recover Evidence', 'Public Enemies', 'Corrupted Idols', 'Reckoning'], 'schemes': ['''Lugharcan's Clover''', '''Lover's Dilemma''', 'Breakthrough', 'Detonate Charges', 'Vendetta', 'Assassinate', 'Claim Jump', 'Hidden Martyrs', 'Catch and Release', 'Research Mission', 'Spread Them Out', 'Bait and Switch', 'Sabotage', 'Leave Your Mark', 'Runic Biding', 'Harness the Ley Line', 'Search the Ruins', 'Dig Their Graves', "Load 'Em Up", 'Public Demonstration', 'Set the Trap', 'Secret Meetup', 'Let Them Bleed', 'Death Beds', 'Power Ritual', 'In Your Face', 'Deliver a Message', 'Outflank', 'Hold Up Their Forces', 'Espionage', 'Sweating Bullets', 'Information Overload', 'Take Prisoner', 'Protected Territory', 'Ensnare'], 'deployments': ['Standard', 'Wedge', 'Flank', 'Corner']}}
gaining_grounds = []
for gg in all_gg:
    gaining_grounds.append(gg)
    
def message_read(message):
    request_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    arguments = message.split(',')
    try:
        rounds_number = min(int(arguments[0].strip()), 10)
    except:
        rounds_number = 'Invalid message. Message should be formatted as [number of rounds, gg to be used, event name, parameters] to work. Please refer to user manual at wincyjneverbornów.blogspot'
    try:
        gg_input = arguments[1].strip()
    except:
        gg_input = 'gg4'
    try:
        event_name = arguments[2].strip()[:20]
    except:
        event_name = 'Unnamed event'
    try:
        options = arguments[3].strip()
    except:
        options = ''
    return [rounds_number, gg_input, event_name, options, request_time]

def read_gg(gg_input):
    scenario_gg = {'Primary': [], 'Secondary': []}
    for gg in gaining_grounds:
        if str(gg+'*') in gg_input:
            scenario_gg['Primary'].append(gg)
        if gg in gg_input:
            if gg not in scenario_gg['Primary']:
                scenario_gg['Secondary'].append(gg)
    if scenario_gg['Primary'] == [] and scenario_gg['Secondary'] == []:
        scenario_gg['Primary'].append('gg4')
    return scenario_gg

def refill(gg, target):
    res = []
    for i in gg:
         res.extend(all_gg[i][target])
    return res

def strat_generator(rounds_number, scenario_gg):
    strat_pool = []
    primary_strats = []
    secondary_strats = []
    
    while len(strat_pool) < rounds_number:
        if primary_strats != []:
            strat_pool.append(primary_strats.pop(random.choice(range(len(primary_strats)))))
        elif secondary_strats != []:
            strat_pool.append(secondary_strats.pop(random.choice(range(len(secondary_strats)))))
        else:
            primary_strats = refill(scenario_gg['Primary'], 'strategies')
            secondary_strats = refill(scenario_gg['Secondary'], 'strategies')
    return strat_pool

def scheme_generator(rounds_number, scenario_gg):
    scheme_pool = []
    pool_of_scheme_pools = []
    primary_schemes = []
    secondary_schemes = []
    sanity_passed = False
    while sanity_passed == False:
        while len(scheme_pool) < rounds_number * 5:
            if primary_schemes != []:
                scheme_pool.append(primary_schemes.pop(random.choice(range(len(primary_schemes)))))
            elif secondary_schemes != []:
                scheme_pool.append(secondary_schemes.pop(random.choice(range(len(secondary_schemes)))))
            else:
                primary_schemes = refill(scenario_gg['Primary'], 'schemes')
                secondary_schemes = refill(scenario_gg['Secondary'], 'schemes')
        if scheme_pool.count(max(set(scheme_pool), key=scheme_pool.count)) <= rounds_number:
            sanity_passed = True
        else:
            scheme_pool = []
    for round in range(rounds_number):
        pool_of_scheme_pools.append([])
    while scheme_pool != []:
        scheme = max(set(scheme_pool), key=scheme_pool.count)
        while scheme in scheme_pool:
            updated = random.choice(pool_of_scheme_pools)
            if len(updated) < 5:
                if scheme not in updated:
                    updated.append(scheme)
                    scheme_pool.remove(scheme)
    return pool_of_scheme_pools

def scenario_generator(rounds_number, strat_pool, pool_of_scheme_pools):
    scenarios = []
    deployments_to_use = []
    for round in range(1, rounds_number+1):
        scenarios.append({'Round': round,})
    for scenario in scenarios:
        if deployments_to_use == []:
            deployments_to_use = refill(['gg4'], 'deployments')
        scenario['Deployment'] = deployments_to_use.pop(random.choice(range(len(deployments_to_use))))
        scenario['Strategy'] = strat_pool.pop(random.choice(range(len(strat_pool))))
        scenario['Schemes'] = pool_of_scheme_pools.pop(random.choice(range(len(pool_of_scheme_pools))))
    return scenarios

def qrcode_generator(scenarios, event_name,request_time,message_author):
    images_names = []
    os.mkdir(f'''output/{message_author}_{event_name}_{request_time}''')
    for scenario in scenarios:
        schemes_decoded = []
        for scheme in scenario['Schemes']:
            schemes_decoded.append(all_gg['ggall']['schemes'].index(scheme))
        data_input = {"specialRules":{},"name": event_name + ' Round ' + str(scenario['Round']), "ruleset":"All", "strat": scenario['Strategy'], "deployment": scenario['Deployment'], "maxCrewSize": 50, "createdIn":"1.7.24", "created": "2004-04-02T21:37:00.000", "schemePool": schemes_decoded}
        imago = qrcode.make(json.dumps(data_input))
        imago.save(f'output/{message_author}_{event_name}_{request_time}/qr.png')
        image1 = Image.new("RGB", (1500, 750), color=(47,49,54))
        image2 = Image.open(f'output/{message_author}_{event_name}_{request_time}/qr.png')
        image1.paste(image2, (30, 30))
        image2.close
        os.remove(f'output/{message_author}_{event_name}_{request_time}/qr.png')
        fnt = ImageFont.truetype('comic.ttf', 40)
        draw = ImageDraw.Draw(image1)
        draw.text(xy=(800, 100), text=f'''{event_name}''', font=fnt, fill=(255, 255, 255))
        draw.text(xy=(800, 150), text=f'''by {message_author}''', font=fnt, fill=(255, 255, 255))
        draw.text(xy=(800, 200), text=f'''Round {scenario['Round']}''', font=fnt, fill=(255, 255, 255))
        draw.text(xy=(800, 250), text=f'''Deployment: {scenario['Deployment']}''', font=fnt, fill=(255, 255, 255))
        draw.text(xy=(800, 300), text=f'''Strategy: {scenario['Strategy']}''', font=fnt, fill=(255, 255, 255))
        draw.text(xy=(800, 350), text='Schemes:', font=fnt, fill=(255, 255, 255))
        for num, scheme in enumerate(scenario['Schemes']):
            y = 400 + num*50
            draw.text(xy=(850, y), text=f'''{scheme}''', font=fnt, fill=(255, 255, 255))
        image1.save(f'''output/{message_author}_{event_name}_{request_time}/{scenario['Round']}.png''')
        images_names.append(discord.File(f'''output/{message_author}_{event_name}_{request_time}/{scenario['Round']}.png'''))
    return images_names

@bot.event
async def on_message(message):
    if message.content[:22] == '<@1300737832289173525>':
        message_author = message.author
        user_input = message_read(str(message.content[22:]))
        if type(user_input[0]) == int:
            gg_input = read_gg(user_input[1])
            strat_generated = strat_generator(user_input[0], gg_input)
            schemes_generated = scheme_generator(user_input[0], gg_input)
            scenarios = scenario_generator(user_input[0], strat_generated, schemes_generated)
            qr_codes = qrcode_generator(scenarios, user_input[2],user_input[4],message_author)
            await message.channel.send(files=qr_codes)
        else:
            await message.channel.send(user_input[0])

bot.run(DISCORD_TOKEN)