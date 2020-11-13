from html.parser import HTMLParser
import requests


class CTFGameParser:
    def __init__(self, ctf_server):
        self.ctf_server = ctf_server
        self.game_finder = CTFGameFinder()
        self.game = 0

    # TODO: Do stats stuff
    def compile_stats(self):
        pass


class CTFGameFinder:
    def __init__(self):
        self.control = self.GameSearchControl()

    def find_game(self, ctf_server):
        self.control = self.GameSearchControl()

        html = requests.get('https://www.brawl.com/MPS/MPSStatsCTF.php').text
        parser = self.CTFGameLookupHTMLParser(self.control, ctf_server)
        parser.feed(html)

        return self.control.recent_game

    class GameSearchControl:
        def __init__(self):
            self.recent_game = 0
            self.game = 0
            self.server_search = False
            self.game_found = False
            self.game_search = False

    class CTFGameLookupHTMLParser(HTMLParser):
        def __init__(self, control, ctf_server):
            super().__init__()
            self.control = control
            self.ctf_server = ctf_server

        def error(self, message):
            pass

        def handle_starttag(self, tag, attrs):
            if self.control.game_found:
                pass
            elif tag == 'a':
                self.control.game_search = True

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            if self.control.game_found:
                pass
            elif self.control.game_search:
                self.control.game = int(data)
                self.control.game_search = False
                self.control.server_search = True
            elif self.control.server_search:
                if data[-4:] == '.com':
                    if data == self.ctf_server:
                        self.control.recent_game = self.control.game
                        self.control.game_found = True
                    self.control.server_search = False
