import json
import requests

region_locale = {
    'us': ['us', 'en_US', 'en'],
#    'kr': ['kr', 'ko_KR', 'ko'],
#    'tw': ['tw', 'zh_TW', 'zh'],
    'eu': ['eu', 'en_GB', 'en']
}

def get_mythic_progression(player_dictionary):
    achievements = player_dictionary["achievements"]
    plus_two = 0
    plus_five = 0
    plus_ten = 0

    if 33096 in achievements["criteria"]:
        index = achievements["criteria"].index(33096)
        plus_two = achievements["criteriaQuantity"][index]

    if 33097 in achievements["criteria"]:
        index = achievements["criteria"].index(33097)
        plus_five = achievements["criteriaQuantity"][index]

    if 33098 in achievements["criteria"]:
        index = achievements["criteria"].index(33098)
        plus_ten = achievements["criteriaQuantity"][index]

    return {
        "plus_two": plus_two,
        "plus_five": plus_five,
        "plus_ten": plus_ten
    }


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

    equipped_ivl = player_dict["items"]["averageItemLevelEquipped"]
    mythic_progress = get_mythic_progression(player_dict)

    # iLvL
    return_string += "Equipped Item Level: %s\n" % equipped_ivl

    # Mythic Progression
    return_string += "Mythics: +2: %s, +5: %s, +10: %s\n" % (mythic_progress["plus_two"],
                                                             mythic_progress["plus_five"],
                                                             mythic_progress["plus_ten"])

async def mythic(client, region, api_key, message):
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
                                                   "Use: !test3 <name> <server> <region>\n"
                                                   "Hyphenate Two Word Servers (Ex: Twisting-Nether)")
