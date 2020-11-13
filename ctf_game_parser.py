from html.parser import HTMLParser
import requests
import re
import pandas.io.html as html


class CTFGameParser:
    def __init__(self, ctf_server):
        self.ctf_server = ctf_server
        self.game = 0
        self.stat_table = []
        self.kit_table = []

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


test = CTFGameParser('1.ctfmatch.brawl.com')
test.process_stats()