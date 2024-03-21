import requests
from bs4 import BeautifulSoup
import re

resultsURL = "https://liquipedia.net/valorant/Evil_Geniuses/Results"
pageURL = "https://liquipedia.net/valorant/Evil_Geniuses"

responseResults = requests.get(resultsURL)
pageResults = requests.get(pageURL)

resultsSoup = BeautifulSoup(responseResults.content, "html.parser")
pageSoup = BeautifulSoup(pageResults.content, "html.parser")

def getMatchHistoryRow(soup):
    tableDiv = soup.select_one(".table-responsive")
    table = tableDiv.find("table")
    tbody = table.find("tbody")
    rows = tbody.find_all('tr')
    return rows

def getRosterDivs(soup):
    outerDiv = soup.select_one("div.tabs-dynamic:nth-child(13) > div:nth-child(2)")
    rosterDivs = outerDiv.find_all('div')
    return rosterDivs
        
def getRosterHistory(rosterDivs):
    rosterSet = set()  
    for div in rosterDivs:
        rosterTables = div.find_all("table", {"class": "wikitable wikitable-striped roster-card"})
        for table in rosterTables:
            tbody = table.find('tbody')
            rows = tbody.find_all('tr', {"class": "Player"})
            for row in rows:
                cells = row.find_all('td')
                id = cells[0].text.strip()
                # Remove parentheses from the name
                name = re.sub(r'\(|\)', '', cells[2].text.strip())
                # Remove square brackets and duplicate prefix from the join date
                join_date = re.sub(r'\[.*\]', '', cells[4].text.strip()).replace("Join Date:", "")
                # Remove square brackets and duplicate prefix from the leave date
                leave_date = re.sub(r'\[.*\]', '', cells[5].text.strip()).replace("Leave Date:", "")
                playerInfo = f"ID: {id}, Name: {name}, Join Date: {join_date}, Leave Date: {leave_date}"
                rosterSet.add(playerInfo)
    print("\nRoster History")
    for playerInfo in rosterSet:
        print(playerInfo)    
        


def getFirstPlaces(tableRows):
    print("\nFirst Places")
    for row in tableRows:
        firstPlaceCell = row.find('td', {"class": "placement-1"})
        if firstPlaceCell is not None:
            cells = row.find_all('td')
            date = cells[0].text
            tournamentName = cells[4].text
            winnings = cells[-1].text
            print(f"Date: {date}, Tournament: {tournamentName}, Prize Winnings: {winnings}")

def getSTierEvents(tableRows):
    print("\nSTier Events (Top 3 Placements)")
    for row in tableRows:
        sTierCell = row.find('td', {"data-sort-value": "A1"})
        if sTierCell is not None:
            cells = row.find_all('td')
            date = cells[0].text
            placementCell = cells[1]
            if placementCell['data-sort-value'] in ["1", "2", "3"]:
                tournamentName = cells[4].text
                winnings = cells[-1].text
                placement = placementCell.text
                print(f"Date: {date}, Tournament: {tournamentName}, Prize Winnings: {winnings}, Placement: {placement}")
        


matchHistoryRows = getMatchHistoryRow(resultsSoup)
rosterDivs = getRosterDivs(pageSoup)

getFirstPlaces(matchHistoryRows)
getSTierEvents(matchHistoryRows)
getRosterHistory(rosterDivs)
