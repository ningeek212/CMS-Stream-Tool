import flask_webserver.flask_server as fs
import ctf_game_parser
from time import sleep

fs.start_server()
fs.overlay_status_dict["stats_card"]["status"] = 0

sleep(2)

stats_parser = ctf_game_parser.CTFGameParser("2.mcctf.com")
stats_parser.process_stats()


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
        fs.stats.append(fs.Stat("Damage Recieved", stat[1].round(1), stat[0], "(Archer)"))
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
        fs.stats.append(fs.Stat("Damage Recieved", stat[1].round(1), stat[0], "(Medic)"))
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

while True:
    fs.hide_stats_card()
    sleep(2)
    for card in card_list:
        card()
        fs.show_stats_card()
        sleep(5)
        fs.hide_stats_card()
        sleep(5)