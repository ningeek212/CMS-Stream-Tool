from html.parser import HTMLParser
import requests
import re
import pandas.io.html as html
from pandas import DataFrame


# Stat table column names:
# name | kit_type | playtime | kills | deaths | damage_dealt | damage_received | hp_restored | sponge_launches
# fire_extinguished | players_teleported | mobs_spawned | fire_axes | flash_bombs | assassination_attempts | headshots
# best_ks | flags_recovered | flags_stolen | flags_dropped | flags_captured | time_with_flag

# Stat table kit names
# ARCHER | ASSASSIN | CHEMIST | DWARF | ELF | ENGINEER | HEAVY | MAGE | MEDIC | NECRO | NINJA | PYRO | SCOUT
# SOLDIER | FASHIONISTA

class CTFGameParser:
    def __init__(self, ctf_server):
        self.ctf_server = ctf_server
        self.game = 0
        self.stat_table = DataFrame()
        self.kit_table = DataFrame()
        self.player_kits = dict()

    def process_stats(self):
        # Load and find most recent game on ctf_server
        mps_html = requests.get('https://www.brawl.com/MPS/MPSStatsCTF.php').text
        parser = self.CTFGameLookupHTMLParser(self.ctf_server)
        parser.feed(mps_html)
        self.game = parser.get_game()
        parser.close()
        if self.game == 0:
            print('Could not find game on {0}'.format(self.ctf_server))
            return False

        # Locate the 2 tables and process both of them
        game_html = requests.get('https://www.brawl.com/MPS/MPSStatsCTF.php?game={0}'.format(self.game)).text
        table_loc = re.split('(<table width=\"100%\" border=\"1\">)|(</table>)', game_html)
        stat_table_html = table_loc[1] + table_loc[3] + table_loc[5]
        kit_table_html = table_loc[7] + table_loc[9] + table_loc[11]
        self.stat_table = html.read_html(stat_table_html)[0]
        self.kit_table = html.read_html(kit_table_html)[0]

        self.set_player_kits()

    def get_stats(self, stat_name, n=1):
        if not self.stat_table.empty:
            lower_stat_name = stat_name.lower()
            stats = self.stat_table.nlargest(n, lower_stat_name, 'all')  # Get largest n stats
            records = stats[['name', lower_stat_name]].to_records(index=False)  # Get IGN and stat from data frame
            test = list(records)  # Convert dataframe to list of tuples
            ret_val = []
            for player in test:
                player_name = player[0]
                ret_val.append((player_name, player[1], self.get_player_kit(player_name)))
            return ret_val
        else:
            return []

    def get_kit_stats(self, stat_name, kit_name, n=1):
        if not self.kit_table.empty:
            lower_stat_name = stat_name.lower()
            upper_kit_name = kit_name.upper()
            kit_stats = self.kit_table.loc[self.kit_table['kit_type'] == upper_kit_name]  # Get kit_name stats
            stats = kit_stats.nlargest(n, lower_stat_name, 'all')  # Get largest n stats
            records = stats[['name', lower_stat_name]].to_records(index=False)  # Get IGN and stat from data frame
            return list(records)  # Convert dataframe to list of tuples
        else:
            return []

    def get_player_kit(self, player_name):
        if not self.kit_table.empty:
            return self.player_kits[player_name]

    def get_player_stats(self, stat_name, player_name):
        if not self.kit_table.empty:
            lower_stat_name = stat_name.lower()
            return self.stat_table.loc[self.stat_table['name'] == player_name, ['name', lower_stat_name]].to_records(
                index=False)
        else:
            return []

    def set_player_kits(self):
        if not self.kit_table.empty:
            for index, row in self.stat_table.iterrows():
                player_name = row['name']
                kits = self.kit_table.loc[self.kit_table['name'] == player_name, ['kit_type', 'playtime']]
                player_kit = kits.nlargest(1, 'playtime').to_records(index=False)
                self.player_kits[player_name] = player_kit[0][0]

    class CTFGameLookupHTMLParser(HTMLParser):
        def __init__(self, ctf_server):
            super().__init__()
            self.recent_game = 0
            self.game = 0
            self.server_search = False
            self.game_found = False
            self.game_search = False
            self.ctf_server = ctf_server

        def get_game(self):
            return self.game

        def error(self, message):
            pass

        def handle_starttag(self, tag, attrs):
            if self.game_found:
                pass
            # The a tag only occurs directly in front of the game number.
            elif tag == 'a':
                self.game_search = True

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            if self.game_found:
                pass
            # Start searching for the server this game was located on
            elif self.game_search:
                self.game = int(data)
                self.game_search = False
                self.server_search = True
            # Check if this server matches ctf_server, and if so store the game number and stop searching
            elif self.server_search:
                if data[-4:] == '.com':
                    if data == self.ctf_server:
                        self.recent_game = self.game
                        self.game_found = True
                    self.server_search = False