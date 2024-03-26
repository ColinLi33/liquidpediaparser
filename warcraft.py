import requests
from bs4 import BeautifulSoup
import re
import csv

pageURL = "https://liquipedia.net/warcraft/Evil_Geniuses"
resultsURL = pageURL + "/Results"

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
    tableDiv = soup.select_one("div.table-responsive:nth-child(9)")
    table = tableDiv.find("table")
    tbody = table.find("tbody")
    rows = tbody.find_all('tr', {"class": "Player"})
    return rows
        
def getRosterHistory(rosterRows):
    rosterSet = set()  
    for row in rosterRows:
        cells = row.find_all('td')
        id = cells[0].text.strip()
        name = re.sub(r'\(|\)', '', cells[2].text.strip())
        joinDate = re.sub(r'\[.*\]', '', cells[4].text.strip()).replace("Join Date:", "").replace('\xa0', '').strip()
        leaveDate = re.sub(r'\[.*\]', '', cells[5].text.strip()).replace("Leave Date:", "").replace('\xa0', '').strip()
        playerInfo = [id, name, joinDate, leaveDate]
        rosterSet.add(tuple(playerInfo))
    with open('./warcraft/roster_history.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Join Date", "Leave Date"]) 
        for playerInfo in rosterSet:
            writer.writerow(list(playerInfo)) 
        
def getFirstPlaces(tableRows):
    firstPlaces = set()
    for row in tableRows:
        firstPlaceCell = row.find('td', {"class": "placement-1"})
        if firstPlaceCell is not None:
            cells = row.find_all('td')
            date = cells[0].text
            tournamentName = cells[4].text
            winnings = cells[-1].text
            firstPlaceInfo = [date, tournamentName, winnings]
            firstPlaces.add(tuple(firstPlaceInfo))

    with open('./warcraft/first_places.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Tournament", "Prize Winnings"]) 
        for firstPlaceInfo in firstPlaces:
            writer.writerow(list(firstPlaceInfo))

def getSTierEvents(tableRows):
    sTierEvents = set()
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
                sTierEventInfo = [date, tournamentName, winnings, placement]
                sTierEvents.add(tuple(sTierEventInfo))

    with open('./warcraft/s_tier_events.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Tournament", "Prize Winnings", "Placement"]) 
        for sTierEventInfo in sTierEvents:
            writer.writerow(list(sTierEventInfo)) 
        
matchHistoryRows = getMatchHistoryRow(resultsSoup)
rosterDivs = getRosterDivs(pageSoup)

getFirstPlaces(matchHistoryRows)
getSTierEvents(matchHistoryRows)
getRosterHistory(rosterDivs)
