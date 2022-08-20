import pprint
import datetime
from requests import get
from pprint import PrettyPrinter
from jinja2 import Template

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()

DATA = {
    "GAMES": [],
    "GAME_LINKS": []
}


def generate_link_template(link, data):
    template = link
    j2_template = Template(template)
    return j2_template.render(data)


def generate_scoreboard_template(data):
    template = """========================
{{ date }}{% for game in games %}{% if game['hTeam']['score']|int > game['vTeam']['score']|int %}
    {{ game['hTeam']['triCode'] }} vs. {{ game['vTeam']['triCode'] }}
    {{ game['hTeam']['score'] }}     {{ game['vTeam']['score'] }}
    
    {{ game['hTeam']['triCode']}} wins against {{ game['vTeam']['triCode'] }}{% else %}
    {{ game['vTeam']['triCode'] }} vs. {{ game['hTeam']['triCode'] }}
    {{ game['vTeam']['score'] }}     {{ game['hTeam']['score'] }}
    
    {{ game['vTeam']['triCode']}} wins against {{ game['hTeam']['triCode'] }}{% endif %}
    --------------------{% endfor %}"""

    j2_template = Template(template)
    return j2_template.render(data)


def get_games():
    number_of_games = 0
    calendar = get_links()['calendar']
    calendar_data = get(BASE_URL + calendar).json()
    scoreboard = get_links()['scoreboard']
    for key in list(calendar_data.keys()):
        if key.isnumeric():
            if calendar_data[key] != 0:
                DATA["GAMES"].append(key)
                DATA['gameDate'] = key
                DATA["GAME_LINKS"].append(generate_link_template(scoreboard, DATA))

    for num, link in enumerate(DATA["GAME_LINKS"]):
        game_data = get(BASE_URL + link).json()
        game_data["date"] = datetime.datetime.strptime(DATA["GAMES"][num], "%Y%m%d").strftime('%Y, %B %d')
        # printer.pprint(game_data)
        print(generate_scoreboard_template(game_data))
        number_of_games += game_data['numGames']
    print(number_of_games)
    return DATA["GAME_LINKS"]


def get_links():
    data = get(BASE_URL + ALL_JSON).json()
    links = data['links']
    # printer.pprint(links)
    return links


def get_scoreboard():
    calendar = get_links()['calendar']
    calendar_data = get(BASE_URL + calendar).json()

    printer.pprint(get_games())
    # printer.pprint(DATA['gameDate'])
    scoreboard = get_links()['scoreboard']
    game_data = get(BASE_URL + scoreboard).json()
    printer.pprint(game_data)


get_games()
# get_scoreboard()
