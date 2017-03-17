import json
import requests

#Declare the current raid to gather boss kills from
cRAID = ['The Nighthold']

region_locale = {'us': ['us', 'en_US', 'en']}

def get_char(name, server, target_region, api_key):
    r = requests.get("https://%s.api.battle.net/wow/character/%s/%s?fields=items+progression+achievements&locale=%s&apikey=%s" % (
            region_locale[target_region][0], server, name, region_locale[target_region][1], api_key))

    if r.status_code != 200:
        raise Exception("Could Not Find Character (No 200 from API)")

    player_dict = json.loads(r.text)

    r = requests.get(
        "https://%s.api.battle.net/wow/data/character/classes?locale=%s&apikey=%s" % (
            region_locale[target_region][0], region_locale[target_region][1], api_key))
    if r.status_code != 200:
        raise Exception("Could Not Find Character Classes (No 200 From API)")
    class_dict = json.loads(r.text)
    class_dict = {c['id']: c['name'] for c in class_dict["classes"]}

    equipped_ilvl = player_dict["items"]["averageItemLevelEquipped"]
    average_ilvl = player_dict["items"]["averageItemLevel"]

    #Test
def get_raid_progression(player_dictionary, raid):
    r = (x for x in player_dictionary["progression"]["raids"] if x["name"] in cRAID)

    #Test if previous command worked
    
    for boss in r["bosses"]:
        boss_name = boss["name"]
        return_string = ''
        return_string += "Boss Name: %s" % boss_name
"""
    nkills = 0
    hkills = 0
    mkills = 0
    boss_name = boss
    
    boss_kills = {}
    for boss in r["bosses"]:
        boss_kills[boss_name] = {
            'bossName': boss["name"],
            'nkills': boss["normalKills"],
            'hkills': boss["heroicKills"],
            'mkills': boss["mythicKills"]
        }

    return {boss_kills}

    return_string = ''
    return_string += "**%s** - **%s** - **%s %s**\n" % (
        name.title(), server.title(), player_dict['level'], class_dict[player_dict['class']])
    return_string += '```CSS\n'  # start Markdown

    # iLvL
    return_string += "Equipped Item Level: %s\n" % equipped_ilvl
    return_string += "Average Item Level: %s\n\n" % average_ilvl
    
    #Boss Output
    for raid, data in raid_progress.items():
        progress = data['progress']
        return_string += "**%s Bosses Killed\n**" % cRaid
        return_string += '{boss}: {nkills} (N) - {hkills} (H) - {mkills} (M)\n'.format(
            boss=progress['bossName'],
            nkills=progress['nkills'],
            hkills=progress['hkills'],
            mkills=progress['mkills']
        )

    return_string += '```'  # end Markdown

"""

    return return_string

async def kills(client, region, api_key, message):
    target_region = region
    try:
        i = str(message.content).split(' ')
        name = i[1]
        server = 'thrall'
        if len(i) == 4 and i[3].lower() in region_locale.keys():
            target_region = i[3].lower()
        character_info = get_char(name, server, target_region, api_key)
        await client.send_message(message.channel, character_info)
    except Exception as e:
        print(e)
        await client.send_message(message.channel, "Error With Name or Server\n"
                                                   "Use: !prog <name> <server> <region>\n"
                                                   "Hyphenate Two Word Servers (Ex: Twisting-Nether)")
