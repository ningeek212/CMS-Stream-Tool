from html.parser import HTMLParser
import requests


class CTFGameParser:
    def __init__(self, ctf_server):
        self.ctf_server = ctf_server
        self.game_finder = CTFGameFinder()
        self.game = 0

    # TODO: Do stats stuff
    def compile_stats(self):
        test = CTFGameFinder()
        test.find_game(self.ctf_server)


class CTFGameFinder:

    def find_game(self, ctf_server):

        html = requests.get('https://www.brawl.com/MPS/MPSStatsCTF.php').text
        parser = self.CTFGameLookupHTMLParser(ctf_server)
        parser.feed(html)

        print(str(parser.get_game()))

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
            elif tag == 'a':
                self.game_search = True

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            if self.game_found:
                pass
            elif self.game_search:
                self.game = int(data)
                self.game_search = False
                self.server_search = True
            elif self.server_search:
                if data[-4:] == '.com':
                    if data == self.ctf_server:
                        self.recent_game = self.game
                        self.game_found = True
                    self.server_search = False
