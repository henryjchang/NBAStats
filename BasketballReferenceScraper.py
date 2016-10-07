from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import string
import unicodecsv as csv



#players sorted in alphabetical order by last name
#i.e. http://www.basketball-reference.com/players/a/aldrila01.html
# when on a specific letter, active players are bolded, which is signified by the <strong></strong> around their hyperlink
#Each player in <tr data-row="num"></tr>
BASE_URL = "http://www.basketball-reference.com"



def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_alphabet_urls():
    #skip x, since no nba players w/ last name starting with x
    x = ['x']
    alphabet = list(string.ascii_lowercase)
    alphabet_urls = [BASE_URL + "/players/" + letter + "/" for letter in alphabet if letter not in x]
    return alphabet_urls

def get_player_urls(alphabet_url):
    """Returns dictionary mapping player name to player's url"""
    soup = make_soup(alphabet_url)
    players = soup.find(id="players")
    active_player_names = [active.a for active in players.findAll("strong")]
    active_player_urls = {active.a.string : BASE_URL + active.a["href"] for active in players.findAll("strong")}
    return active_player_urls

def get_player_years_urls(player_url):
    # get urls to each year the player was active
    soup = make_soup(player_url)
    years_table = soup.find(id="per_game")
    years_urls = [BASE_URL + years.th.a["href"] for years in years_table.findAll("tr", {"class" : "full_table"})]
    return years_urls

def get_player_year_stats(player_name, player_year_url):
    """ get player's stats through each game that year 
    name date age team at opponent minutes fg fga fg_pct fg3 fg3a fg3_pct ft fta ft_pct orb drb trb ast stl blk tov pts plus_minus 
    """
    soup = make_soup(player_year_url)
    game_table = soup.find("table", {"class" : "row_summable sortable stats_table"}).find("tbody")
    games = game_table.findAll("tr", id)
    name = player_name
    data_all = []
    for game in games:
        if game.find("td", {"data-stat" : "reason"}) == None: # exclude games with Inactive/DNP/Injury
            if game.find("td", {"data-stat" : "date_game"}) == None: #exclude header rows
                continue

            date = game.find("td", {"data-stat" : "date_game"}).a.string
            age = game.find("td", {"data-stat" : "age"}).string
            team = game.find("td", {"data-stat" : "team_id"}).a.string
            at = game.find("td", {"data-stat" : "game_location"}).string
            opponent = game.find("td", {"data-stat" : "opp_id"}).a.string
            minutes = game.find("td", {"data-stat" : "mp"}).string
            fg = game.find("td", {"data-stat" : "fg"}).string
            fga = game.find("td", {"data-stat" : "fga"}).string
            fg_pct = game.find("td", {"data-stat" : "fg_pct"}).string
            fg3 = game.find("td", {"data-stat" : "fg3"}).string
            fg3a = game.find("td", {"data-stat" : "fg3a"}).string
            fg3_pct = game.find("td", {"data-stat" : "fg3_pct"}).string
            ft = game.find("td", {"data-stat" : "ft"}).string
            fta = game.find("td", {"data-stat" : "fta"}).string
            ft_pct = game.find("td", {"data-stat" : "ft_pct"}).string
            orb = game.find("td", {"data-stat" : "orb"}).string
            drb = game.find("td", {"data-stat" : "drb"}).string
            trb = game.find("td", {"data-stat" : "trb"}).string
            ast = game.find("td", {"data-stat" : "ast"}).string
            stl = game.find("td", {"data-stat" : "stl"}).string
            blk = game.find("td", {"data-stat" : "blk"}).string
            to = game.find("td", {"data-stat" : "tov"}).string
            pts = game.find("td", {"data-stat" : "pts"}).string
            plus_minus = game.find("td", {"data-stat" : "plus_minus"}).string
            data = [name, date, age, team, at, opponent, minutes, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, to, pts, plus_minus]
            data_all.append(data) 
            sleep(1)

    return data_all


if __name__ == '__main__':

    alphabet_urls = get_alphabet_urls()
    active_player_urls = {}
    for letter_url in alphabet_urls:
        active_player_urls_letter = get_player_urls(letter_url) 
        active_player_urls.update(active_player_urls_letter)
        sleep(1)

    fout = open('stats.csv', 'a')
    for name, url in sorted(active_player_urls.iteritems()):
        years_urls = get_player_years_urls(url)
        for year_url in years_urls:
            data = get_player_year_stats(name, year_url)
            for row in data:
                for column in row:
                    fout.write('%s,' % column)
                fout.write('\n')
        #raw_input("Press Enter to continue...")
    fout.close()


