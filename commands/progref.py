def get_raid_progression(player_dictionary, raid):
    r = [x for x in player_dictionary["progression"]
    ["raids"] if x["name"] in raid][0]
    normal = 0
    heroic = 0
    mythic = 0

    for boss in r["bosses"]:
        if boss["normalKills"] > 0:
            normal += 1
        if boss["heroicKills"] > 0:
            heroic += 1
        if boss["mythicKills"] > 0:
            mythic += 1

    return {"normal": normal,
            "heroic": heroic,
            "mythic": mythic,
            "total_bosses": len(r["bosses"])}

    # Build raid progression
    raid_progress = {}
    for raid in RAIDS:
        raid_name = raid[0]
        raid_abrv = raid[1]
        raid_progress[raid_name] = {
            'abrv': raid_abrv,
            'progress': get_raid_progression(player_dict, raid_name)
        }

    # Raid Progression
    for raid, data in raid_progress.items():
        progress = data['progress']
        return_string += '{abrv}\n {normal}/{total} (N)\n {heroic}/{total} (H)\n {mythic}/{total} (M)\n\n'.format(
            abrv=data['abrv'],
            normal=progress['normal'],
            heroic=progress['heroic'],
            mythic=progress['mythic'],
            total=progress['total_bosses']
        )
