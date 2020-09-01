from bs4 import BeautifulSoup as bs
import requests


def get_names():
    game_name = input("Please select the name of a game you are searching for.\n"
                      "We will try our best to give you the average pricing online. "
                      "\nKeep in mind that this application only works for games \n"
                      "under NTSC-U/C for better accuracy:")
    console_name = input("What system is this game played on? (ex. Xbox 360, NES, Commodore 64)")

    return game_name.lower(), console_name.lower()


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

    return overall_price / len(prices)


def get(link):
    """
    pull html from the url link parameter.
    help from https://www.youtube.com/watch?v=ng2o98k983k
    """
    page = requests.get(link).text
    fetch = bs(page, 'lxml')
    return fetch


def check_format(price):
    if "See price" in price:
        return 0.00
    if "," in price:
        convert_price = ""
        for j in price:
            if j != ",":
                convert_price = convert_price + j
        price = convert_price

    if " " in price:
        price_range = price.split()
        price = (float(price_range[0]) + float(price_range[-1][1:])) / 2

    return price


def check_shipping(ship_html):
    if ship_html is None:
        return False
    elif str(ship_html.get_text()) == "Free shipping" or str(ship_html.get_text()) == "Freight":
        return False

    return True


def add_shipping(price, ship_check):
    shipping = ship_check.get_text()
    temp_ship = shipping.split()
    shipping = float(temp_ship[0][2:])
    price = float(price) + shipping

    return price


def filter_title(title, page):
    """
    Use for removing unwanted prices on games that will likely lead to a significantly higher price due to details given
     in the title of the listing. (ex. CIB, Sealed, Factory, Collector's Edition)
    """
    keywords = ["cib", "collector's", "collectors", "collector", "legendary", "special", "factory", "sealed",
                "complete", "in box", "lot", "games", "graded", "mint", "disc only", "disk", "rare",
                "repro", "reproduction", "manual only", "case only", "set", "bundle", "Steelbook", "steelbook"]

    listing_name = page.find(class_="s-item__title").get_text()

    for i in keywords:
        if i in listing_name.lower() and i not in title:
            return False

    return True


def get_prices(page_data, title):
    price_list = []

    for i in range(199):

        listing = page_data.find("li", {"data-view": "mi:1686|iid:" + str(i+1)}) #"srp-river-results" + str(i + 1))
        if listing is None:
            return average_price(price_list)

        games = listing.find(class_="s-item__price")  # finds price of item

        price = games.get_text()[1:]
        price = check_format(price)

        ship_check = ((listing.find(
            class_="s-item__shipping s-item__logisticsCost")))  # finds the shipping of item

        if check_shipping(ship_check) is True:
            price = add_shipping(price, ship_check)

        if filter_title(title, listing):
            price_list.append(float(price))

    return average_price(price_list)


def main():
    game, console = get_names()

    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + sub_space(game) + "+" + sub_space(console) + \
          "&_sacat=0&LH_BIN=1&Region%2520Code=NTSC%252DU%252FC%2520%2528US%252FCanada%2529&rt=nc&_oaa=1&_dcat=139973" \
          "&_ipg=200"

    page = get(url)
    average = get_prices(page, game)

    print("\n" + game + " on the " + console + " is approximately $"
          + str("{0:.2f}".format(average)))  # Used to remove large floating decimal numbers in the average

    print("\nKeep in mind that the average may vary depending on pricing based on quality and edition of copies")
    print("Also, games with similar names may accidentally be thrown into the average.")
    input()


main()
