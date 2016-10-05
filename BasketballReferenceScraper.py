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

def get_player_links(alphabet_url):
    soup = make_soup(alphabet_url)
    players = soup.find(id="players")
    #active_player_links = [BASE_URL + active["href"] for active in players.findAll("a")]
    active_player_links = [BASE_URL + active.a["href"] for active in players.findAll("strong")]
    return active_player_links

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
    
    alphabet_urls = get_alphabet_urls()
    active_player_urls = []
    for letter_url in alphabet_urls:
        active_player_urls_letter = get_player_links(letter_url) 
        active_player_urls += active_player_urls_letter

    print active_player_urls

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

