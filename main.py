from bs4 import BeautifulSoup as bs
import requests


def get_names():
    game_name = input("Please select the name of a game you are searching for.\n"
                      "We will try our best to give you the average pricing online. "
                      "\nKeep in mind that this application only works for games \n"
                      "under NTSC-U/C for better accuracy:")
    console_name = input("What system is this game played on? (ex. Xbox 360, NES, Commodore 64)")

    game_name = sub_space(game_name)
    console_name = sub_space(console_name)

    return game_name, console_name


def sub_space(label):
    """
    replaces spaces in labels with '+' so url searching is possible.
    """
    new_label = ""
    for i in label:
        if i == " ":
            new_label = new_label + "+"
        else:
            new_label = new_label + i
    return new_label

def get(link):
    """
    pull html from the url link parameter.
    help from https://www.youtube.com/watch?v=ng2o98k983k
    """
    page = requests.get(link).text
    fetch = bs(page, 'lxml')
    games = fetch.find("li")
    print(fetch.find(id="srp-river-results-listing1"))


def main():
    game, console = get_names()
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + game + "+" + console + \
          "&_sacat=0&LH_BIN=1&Region%2520Code=NTSC%252DU%252FC%2520%2528US%252FCanada%2529&rt=nc&_oaa=1&_dcat=139973" \
          "&_ipg=200 "
    print(url)
    get(url)


main()
