import random
import os
import qrcode
import json
from datetime import datetime
from gg import *

from PIL import Image, ImageDraw, ImageFont

def message_read(message):
    request_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    arguments = message.split(',')
    try:
        rounds_number = min(int(arguments[0].strip()), 10)
    except:
        return 'error'
    try:
        gg_input = arguments[1].strip()
        gg_input = gg_input.lower()
    except:
        gg_input = 'gg4'
    try:
        event_name = arguments[2].strip()[:35]
    except:
        event_name = 'Unnamed event'
    try:
        options = arguments[3].strip()
    except:
        options = ''
    return [rounds_number, gg_input, event_name, options, request_time]

def read_gg(gg_input):
    scenario_gg = {'Primary': [], 'Secondary': []}
    for gg_pool in gaining_grounds:
        if str(gg_pool+'*') in gg_input:
            scenario_gg['Primary'].append(gg_pool)
        if gg_pool in gg_input:
            if gg_pool not in scenario_gg['Primary']:
                scenario_gg['Secondary'].append(gg_pool)
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
    pool_of_scheme_pools = []
    empty_pool = []
    def scheme_pool_randomizer():
        scheme_pool = []
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
        return scheme_pool
    scheme_pool = scheme_pool_randomizer()
    for round in range(rounds_number):
        pool_of_scheme_pools.append([])
    while scheme_pool != []:
        i = 0
        scheme = max(set(scheme_pool), key=scheme_pool.count)
        while scheme in scheme_pool:
            if i > 100:
                pool_of_scheme_pools = []
                for round in range(rounds_number):
                    pool_of_scheme_pools.append([])
                scheme_pool = scheme_pool_randomizer()
                break
            else:
                i += 1
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

def qrcode_generator(scenarios, event_name,options,request_time):
    maps_used = []
    rules = {}
    if 'sin' in options:
        rules['Singles'] = {'name': 'Singles'}
    if '-ban' in options:
        if '-ban3' in options:
            rules['Bans'] = {'name': 'Bans', 'value':3}
        elif '-ban2' in options:
            rules['Bans'] = {'name': 'Bans', 'value':2}
        else:
            rules['Bans'] = {'name': 'Bans', 'value':1}
    images_names = []
    path = f'''output/{event_name}_{request_time}'''
    os.mkdir(path)
    for scenario in scenarios:
        schemes_decoded = []
        for scheme in scenario['Schemes']:
            schemes_decoded.append(all_gg['ggall']['schemes'].index(scheme))
        data_input = {"specialRules":rules,"name": event_name + ' Round ' + str(scenario['Round']), "ruleset":"All", "strat": scenario['Strategy'], "deployment": scenario['Deployment'], "maxCrewSize": 50, "createdIn":"1.7.24", "created": "2004-04-02T21:37:00.000", "schemePool": schemes_decoded}
        imago = qrcode.make(json.dumps(data_input))
        imago = imago.resize((690, 690))
        imago.save(f'{path}/qr.png')
        image1 = Image.new('RGB', (1500, 750), color=(47,49,54))
        image2 = Image.open(f'{path}/qr.png')
        image1.paste(image2, (30, 30))
        image2.close
        os.remove(f'{path}/qr.png')
        fnt = ImageFont.truetype(font, 40)
        draw = ImageDraw.Draw(image1)
        w = draw.textlength(event_name, font=fnt)
        draw.text(xy=(1125-(w/2), 100), text=event_name, font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))
        w = draw.textlength(f'''Round {scenario['Round']}''', font=fnt)
        draw.text(xy=(1125-(w/2), 150), text=f'''Round {scenario['Round']}''', font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))
        w = draw.textlength(f'''Deployment: {scenario['Deployment']}''', font=fnt)
        draw.text(xy=(1125-(w/2), 200), text=f'''Deployment: {scenario['Deployment']}''', font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))
        w = draw.textlength(f'''Strategy: {scenario['Strategy']}''', font=fnt)
        draw.text(xy=(1125-(w/2), 250), text=f'''Strategy: {scenario['Strategy']}''', font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))
        w = draw.textlength('Schemes:', font=fnt)
        draw.text(xy=(1125-(w/2), 300), text='Schemes:', font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))    
        for num, scheme in enumerate(scenario['Schemes']):
            w = draw.textlength(f'''{scheme}''', font=fnt)
            y = 350 + num*50
            draw.text(xy=(1125-(w/2), y), text=f'''{scheme}''', font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))
        if '-vas' in options:
            image_vas = Image.new('RGB', (760, 750), color=(47,49,54))
            map_num = random.choice(range(1, len(vassal_maps)))
            while map_num in maps_used:
                map_num = random.choice(range(1, len(vassal_maps)))
            vassal_map = Image.open(f'vassal_maps/{map_num}.png')
            image_vas.paste(vassal_map, (30, 30))
            vassal_map.close
            draw = ImageDraw.Draw(image_vas)
            w = draw.textlength(f'[{map_num}] {vassal_maps[map_num]}', font=fnt)
            draw.text(xy=(375-(w/2), 50), text=f'[{map_num}] {vassal_maps[map_num]}', font=fnt, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0,0,0))
            new_image = Image.new('RGB', (image1.size[0] + image_vas.size[0], 750), color=(47,49,54))
            new_image.paste(image1, (0,0))
            new_image.paste(image_vas, (1500,0))
            image1 = new_image
            maps_used.append(map_num)
        image1.save(f'''{path}/{scenario['Round']}.png''')
        images_names.append(f'''{path}/{scenario['Round']}.png''')
    return images_names

def get_pule(message):
    user_input = message_read(message)
    if user_input == 'error':
        return 'error'
    else:
        gg_input = read_gg(user_input[1])
        strat_generated = strat_generator(user_input[0], gg_input)
        schemes_generated = scheme_generator(user_input[0], gg_input)
        scenarios = scenario_generator(user_input[0], strat_generated, schemes_generated)
        qr_codes = qrcode_generator(scenarios, user_input[2],user_input[3],user_input[4])
        return qr_codes