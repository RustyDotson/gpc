from bs4 import BeautifulSoup as bs
import requests


def get_names():
    game_name = input("Please select the name of a game you are searching for.\n"
                      "We will try our best to give you the average pricing online. "
                      "\nKeep in mind that this application only works for games \n"
                      "under NTSC-U/C for better accuracy:")
    console_name = input("What system is this game played on? (ex. Xbox 360, NES, Commodore 64)")

    return game_name, console_name


def sub_space(label):
    """
    replace spaces in labels with '+' so url searching is possible.
    """
    new_label = ""
    for i in label:
        if i == " ":
            new_label = new_label + "+"
        else:
            new_label = new_label + i
    return new_label


def average_price(prices):
    """
    get the average of a list of floats
    """

    overall_price = 0
    for i in prices:
        overall_price += i

    return overall_price/len(prices)


def get(link):
    """
    pull html from the url link parameter.
    help from https://www.youtube.com/watch?v=ng2o98k983k
    """
    page = requests.get(link).text
    fetch = bs(page, 'lxml')
    price_list = []

    for i in range(99):
        print(i)
        if fetch.find(id="srp-river-results-listing" + str(i + 1)) == None:
            return average_price(price_list)

        games = fetch.find(id="srp-river-results-listing" + str(i + 1)).find(class_="s-item__price")
        price = (games.get_text()[1:])

        if "," in price:
            convert_price = ""
            for j in price:
                if j != ",":
                    convert_price = convert_price + j
            price = convert_price

        if " " in price:
            price_range = price.split()
            price = (float(price_range[0]) + float(price_range[-1][1:]))/2

        #if float(price) > 1000.0:
        #    continue
        #else:
        price_list.append(float(price))

    return average_price(price_list)


def main():

    game, console = get_names()

    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + sub_space(game) + "+" + sub_space(console) + \
          "&_sacat=0&LH_BIN=1&Region%2520Code=NTSC%252DU%252FC%2520%2528US%252FCanada%2529&rt=nc&_oaa=1&_dcat=139973" \
          "&_ipg=200"

    print(url)
    average = get(url)

    print("\nThe average price of " + game + " on the " + console + " is approximately $"
          + str("{0:.2f}".format(average)))  # Used to remove large floating decimal numbers in the average

    print("\nKeep in mind that the average may vary depending on pricing based on quality and edition of copies")
    print("\nAlso, games with similar names may accidentally be thrown into the average.")


main()
