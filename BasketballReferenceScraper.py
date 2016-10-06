from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import string

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

def get_player_stats(player_url):
    # get urls to each year the player was active
    soup = make_soup(player_url)
    years_table = soup.find(id="per_game")
    years_urls = [BASE_URL + years.th.a["href"] for years in years_table.findAll("tr", {"class" : "full_table"})]
    return years_urls
    # loop over each year for the player's stats through each game that year
    


#def get_category_winner(category_url):
#    soup = make_soup(category_url)
#    #category = soup.find("h1", "headline headline-4088191").string
#    category = soup.find("h1", "headline").string
#    print category
#    winner = [h2.string for h2 in soup.findAll("h2", "boc1")]
#    runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]
#    return {"category": category, 
#            "category_url": category_url, 
#            "winner": winner, 
#            "runners_up": runners_up}

if __name__ == '__main__':
    
    years_urls = get_player_stats("http://www.basketball-reference.com/players/a/acyqu01.html")
    print years_urls
#    alphabet_urls = get_alphabet_urls()
#    active_player_urls = []
#    for letter_url in alphabet_urls:
#        active_player_urls_letter = get_player_urls(letter_url) 
#        print active_player_urls_letter
#        active_player_urls += active_player_urls_letter
#        sleep(1)

    #lastname_A = "http://www.basketball-reference.com/players/a/"
    #players_A = get_player_links(lastname_A)

    #print players_A

#    data = []
#    for category in categories:
#        winner = get_category_winner(category)
#        data.append(winner)
#        #sleep(1)
#
#    print data

