import flask_webserver.flask_server as fs
import ctf_game_parser
from time import sleep

fs.start_server()
fs.overlay_status_dict["stats_card"]["status"] = 0

# sleep(2)

stats_parser = ctf_game_parser.CTFGameParser(input("Enter the match server IP: "))


def top_damage_comparison():
    fs.stats = []
    for stat in stats_parser.get_stats("damage_dealt", 2):
        fs.stats.append(fs.Stat("Damage Dealt", stat[1], stat[0], ""))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Top Damage Comparison"
    fs.show_stats_card()


def headshots_kills_killstreak():
    fs.stats = []
    headshots = stats_parser.get_stats("headshots")[0]
    kills = stats_parser.get_stats("kills")[0]
    killstreak = stats_parser.get_stats("best_ks")[0]
    fs.stats.append(fs.Stat("Most Headshots", headshots[1], headshots[0], ""))
    fs.stats.append(fs.Stat("Most Kills", kills[1], kills[0], ""))
    fs.stats.append(fs.Stat("Highest Killstreak", killstreak[1], killstreak[0], ""))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Map Info Goes Here"


def archer_headshots_comparison():
    fs.stats = []
    for stat in stats_parser.get_stats("headshots", 2):
        fs.stats.append(fs.Stat("Headshots", stat[1], stat[0], "(Archer)"))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Archer Comparison"


def archer_damage_taken_comparison():
    fs.stats = []
    for stat in stats_parser.get_kit_stats("damage_received", "archer", 2):
        fs.stats.append(fs.Stat("Damage Received", stat[1].round(1), stat[0], "(Archer)"))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Archer Comparison"


def offense_statistics():
    fs.stats = []
    captured = stats_parser.get_stats("flags_captured")[0]
    stolen = stats_parser.get_stats("flags_stolen")[0]
    flag_time = stats_parser.get_stats("time_with_flag")[0]
    fs.stats.append(fs.Stat("Most Flags Captured", captured[1], captured[0], ""))
    fs.stats.append(fs.Stat("Most Flags Stolen", stolen[1], stolen[0], ""))
    fs.stats.append(fs.Stat("Most time with Flag", flag_time[1], flag_time[0], ""))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Offense Statistics"


def medic_pressure():
    fs.stats = []
    for stat in stats_parser.get_kit_stats("damage_received", "medic", 2):
        fs.stats.append(fs.Stat("Damage Received", stat[1].round(1), stat[0], "(Medic)"))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Medic Pressure"


def pyro_damage_dealt():
    fs.stats = []
    for stat in stats_parser.get_kit_stats("damage_dealt", "pyro", 2):
        fs.stats.append(fs.Stat("Damage Dealt", stat[1], stat[0], "(Pyro)"))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Pyro Damage Dealt"


def pyro_damage_received():
    fs.stats = []
    for stat in stats_parser.get_kit_stats("damage_received", "pyro", 2):
        fs.stats.append(fs.Stat("Damage Received", stat[1], stat[0], "(Pyro)"))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Pyro Damage Received"


def assassin_comparison():
    fs.stats = []
    kills = stats_parser.get_kit_stats("kills", "assassin")[0]
    fs.stats.append(fs.Stat("Most Assassin Kills", kills[1], kills[0], "(Assassin)"))
    recoveries = stats_parser.get_kit_stats("flags_recovered", "assassin")[0]
    fs.stats.append(fs.Stat("Most Assassin Recoveries", recoveries[1], recoveries[0], "(Assassin)"))
    fs.overlay_status_dict["stats_card"]["map_info"] = "Assassin Comparison"


card_list = [top_damage_comparison, headshots_kills_killstreak, archer_headshots_comparison,
             archer_damage_taken_comparison, offense_statistics, medic_pressure, pyro_damage_dealt,
             pyro_damage_received, assassin_comparison]

cards_list = [
    [top_damage_comparison, "Shows the top two damage dealers in the last game"],
    [headshots_kills_killstreak, "Shows the player with the most headshots, the most kills, "
                                 "and the highest killstreak"],
    [archer_headshots_comparison, "Compares the amount of headshots of the top 2 archers"],
    [archer_damage_taken_comparison, "Compares the amount of damage taken by the archers"],
    [offense_statistics, "Shows the players with the most captures, steals and time with flag"],
    [medic_pressure, "Compares the amount of damage taken"],
    [pyro_damage_dealt, "Compares the amount of damage done by the two pyros"],
    [pyro_damage_received, "Compares the amount of damage received by the two pyros"],
    [assassin_comparison, "Shows the assassin players with the most kills and recoveries"]
]


def select_card_to_display():
    stats_parser.process_stats()
    print("=========")
    print("Please select which card you would like to display from the list below")
    count = 1
    for card in cards_list:
        print("[{}] \033[94m{}\033[0m - {}".format(count, card[0].__name__, card[1]))
        count += 1
    response = int(input("Please make your selection: "))-1
    print("You have chosen \033[94m{} - {}\033[0m".format(cards_list[response][0].__name__, cards_list[response][1]))
    print("Displaying card for 20 seconds")
    cards_list[response][0]()
    fs.show_stats_card()
    sleep(20)
    print("Hiding card")
    fs.hide_stats_card()
