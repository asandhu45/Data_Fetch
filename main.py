# Amanjot Singh Sandhu
# ICA04
#1232_2850_A04

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

selection = ''
url = ''
returnedDict = {}


def getpage(**kwargs):
    global url
    link = "https://www.memoryexpress.com/Search/Products?"
    custURL = ''
    masterURL = ''

    for key, val in kwargs.items():
        custURL += f"&{key}={val}"
    masterURL = link + custURL + '&'
    reqGet = requests.get(masterURL)

    print(masterURL)
    if reqGet.status_code == requests.codes.ok:
        print("Request Status Code: " + str(reqGet.status_code))
        url = reqGet.text
    else:
        print(reqGet.status_code)


def parsepage(webRes):
    bs = BeautifulSoup(webRes, 'html.parser')
    title = bs.title.get_text()
    summaryList = bs.findAll("div", class_='c-shca-icon-item__summary-list')

    dict = {}

    for div in summaryList:
        spans = div.findAll('span')
        size = 10
        for span in spans:
            value = span.text.strip()
            if value.startswith('$'):
                price = float(value.strip('$').replace(' ', '').replace(',', ''))
                minRange = (price // size) * size
                maxRange = minRange + size
                rangeT = (minRange, maxRange)
                if rangeT not in dict:
                    dict[rangeT] = [price]
                else:
                    dict[rangeT].append(price)

    print(f"In {title}, Found [{len(dict.items())}]")
    returnedDict = dict
    return dict


def save(dictionary, fName):
    fileList = os.listdir()
    sortedDict = {}
    sortedDict = dictionary.items()
    i = 1
    while fName in fileList:
        fName = f"{fName}_{i}.txt"
        i += 1
    try:
        with open(f"{fName}", 'w') as file:

            file.write(f"{fName} Saved\n")
            file.write(f"Price information as of : {datetime.now().isoformat()}\n\n")
            file.write(f"In , Found [{len(sortedDict)}]\n")
            for rng, prices in sortedDict:
                file.write(f"Price Range :{str(rng):16} : {prices}\n")
            print(f"{fName} Saved.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# ---------------------------------------------------------------------------------------------------------------- #
def menu():
    """
    Shows User the menu and ask for input
    Only Quit if Q is entered
    Keeps running in a loop if invalid response is entered
    :return: Nothing - Call other functions
    """
    print(' ---Menu--- ')
    print('g : Web Search')
    print('p : Parse Page')
    print('s : Save')
    print('q : Quit')

    # User Selection
    global selection

    global returnedDict
    # Get the user selection
    selection = input('Selection : ').lower()
    global url

    # If the user selects g
    if selection == 'g':
        search = input('Search [psu]: ') or ('psu')
        pageSize = input('Page Size [40/[80]/120]: ') or ('80')
        sort = input('Sort [Relevance/Price/PriceDesc/[Manufacturer]]: ') or ('Manufacturer')
        getpage(Search=search, PageSize=pageSize, Sort=sort)

    if selection == 'p':
        if len(url) > 1:
            returnedDict = parsepage(url)
            for rng, prices in returnedDict.items():
                print(f"Price Range :{str(rng):16} : {prices}")

    if selection == 's':
        name = input("Please Enter an Amazing Name: ") or ("Out.txt")

        save(returnedDict, name)


# ---------------------------------------------------------------------------------------------------------------- #
# Actual Implementation
# User cant leave the menu till he quits (Q)
while True:
    menu()
    if selection == 'q':
        break
# ---------------------------------------------------------------------------------------------------------------- #
