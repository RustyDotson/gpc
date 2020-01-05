from bs4 import BeautifulSoup as bs
import requests
import os


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
    elif str(ship_html.get_text()) == "Free Shipping":
        return False
    return True


def add_shipping(price, ship_check):

    shipping = ship_check.get_text()
    temp_ship = shipping.split()
    shipping = float(temp_ship[0][2:])
    price = float(price) + shipping

    return price


def get_prices(page_data):
    price_list = []

    for i in range(199):

        if page_data.find(id="srp-river-results-listing" + str(i + 1)) is None:
            return average_price(price_list)

        games = page_data.find(id="srp-river-results-listing" + str(i + 1)).find(class_="s-item__price")  # finds
        # price of item

        price = games.get_text()[1:]
        price = check_format(price)

        ship_check = ((page_data.find(id="srp-river-results-listing" + str(i + 1)).find(
            class_="s-item__shipping s-item__logisticsCost")))  # finds the shipping of item

        if check_shipping(ship_check) is True:
            price = add_shipping(price, ship_check)

        price_list.append(float(price))

    return average_price(price_list)


def main():
    game, console = get_names()

    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + sub_space(game) + "+" + sub_space(console) + \
          "&_sacat=0&LH_BIN=1&Region%2520Code=NTSC%252DU%252FC%2520%2528US%252FCanada%2529&rt=nc&_oaa=1&_dcat=139973" \
          "&_ipg=200"

    print(url)
    page = get(url)

    average = get_prices(page)

    print("\nThe average price of " + game + " on the " + console + " is approximately $"
          + str("{0:.2f}".format(average)))  # Used to remove large floating decimal numbers in the average

    print("\nKeep in mind that the average may vary depending on pricing based on quality and edition of copies")
    print("\nAlso, games with similar names may accidentally be thrown into the average.")


main()
