# ==================================================
# THE YG REPORT BY ZO
# ==================================================
#
# TO DO LIST:
# Add the ability to search by artist
# Add ways of utilising other stats such as controversy
# Add a way of filtering by rate

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
#import matplotlib.figure as fig
#import difflib

def pandaDispToggle() :

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

pandaDispToggle() # Toggle this by uncommenting if you want to be able to view full tables regardless of terminal width

# ==================================================
# Toggling which rates to not include
# ==================================================

nctShineeToggle = 0

#nctShineeToggle = int(input("If you want to view results WITHOUT NCT rate or SHINee soloists rate, type 0.\nIf you want to view it WITHOUT any of the super gen rates (RVTWBP, EBS), type 1.\nIf you want to view it WITHOUT NCT rate, SHINee soloists rate, or the super gen rates, type 2.\nElse, type 3 to proceed. "))

#if nctShineeToggle != (0 or 1 or 2 or 3) :

    #nctShineeToggle = int(input("Please enter one of the numbers listed.\nIf you want to view results WITHOUT NCT rate or SHINee soloists rate, type 0. If you want to view it WITHOUT any of the super gen rates (RVTWBP, EBS), type 1. Else, type 2 to proceed. "))

# ==================================================
# Company artist arrays
# ==================================================

ygSoloists = ["B.I", "CL", "Daesung", "G-Dragon", "Jennie", "Jeon Somi", "Jisoo", "Lisa", "Rosé", "Taeyang"]

ygGroups = ["2NE1", "AKMU", "Allday Project", "Babymonster", "BIGBANG", "Blackpink", "Epik High", "GD x Taeyang", "iKon", "izna", "Jus2", "MEOVV", "miss A", "Treasure", "Winner"]

smSoloists = ["Baekhyun", "BoA", "Chen", "Doyoung", "Irene", "Jaehyun", "Jonghyun", "Joy", "Kai", "Key", "Mark", "Max Changmin", "Minho", "Onew", "Seulgi", "Sulli", "Taemin", "Taeyeon", "Taeyong", "Ten", "Wendy", "Yuta"]

smGroups = ["aespa", "EXO", "EXO-CBX", "f(x)", "Girls' Generation", "GOT the beat", "H.O.T.", "Hearts2Hearts", "NCT 127", "NCT Dojaejung", "NCT Dream", "NCT U", "NCT Wish", "Red Velvet", "Red Velvet I&S", "RIIZE", "SHINee", "Super Junior", "SuperM", "TVXQ", "WayV"]

jypeSoloists = ["J.Y. Park", "Jihyo", "Nayeon", "Park Jiyoon", "Rain", "Sunmi", "Tzuyu", "Yeji"]

jypeGroups = ["2AM", "2PM", "DAY6", "GOT7", "ITZY", "NMIXX", "Stray Kids", "Twice", "Twice/MISAMO", "Wonder Girls", "Xdinary Heroes"]

hybeSoloists = ["Agust D", "Beomgyu", "j-hope", "Huh Yunjin", "Jimin", "Jin", "Jungkook", "RM", "V", "Yeonjun"]

hybeGroups = ["BOYNEXTDOOR", "BTS", "Enhypen", "ILLIT", "Katseye", "LE SSERAFIM", "NewJeans","NU'EST", "NU'EST W", "Seventeen", "TWS", "TXT"]

ygArtists = ygSoloists + ygGroups
smArtists = smSoloists + smGroups
jypeArtists = jypeSoloists + jypeGroups
hybeArtists = hybeSoloists + hybeGroups

# ==================================================

# Cube artists?
# Former survival show contestants?
# BG vs GG? Soloists vs groups?

# ==================================================
# Cleaning r/kpoprates stat sheet csv
# ==================================================

rateCsv = pd.read_csv("kpoprates stats sheet.csv", header = 0, sep = ",")
rateCsv["Company alignment"] = ""
rateCsv["Num songs"] = "" # For calculating number of songs in rate
rateCsvTrim = rateCsv.drop(["Artist", "Year", "Unnamed: 4", "Controv.", "P#","Unnamed: 10", "11s", "≥10", "≥9", "<5", "<3", "0s","Unnamed: 18", "11%", "≥10%", "≥9%", "<5%", "<3%", "0%", "Unnamed: 25", "Bonus", "Date", "CU", "Win"], axis = 1)
rateCsvColumn = rateCsvTrim.rename(columns = {"Unnamed: 0": "Placement"})
rateCsvColumn.loc[rateCsvColumn["MainArtist"] == "2:00 PM", "MainArtist"] = "2PM"
rateCsvColumn.loc[rateCsvColumn["MainArtist"] == "2:00 AM", "MainArtist"] = "2AM"
rateCsvColumn.loc[rateCsvColumn["Placement"] != "", "Placement"] = ""
#print(rateCsvColumn["Placement"])
#exit()

# ==================================================
# Creating function to assign companies to each song
# ==================================================

deleteArray = []

def assignCompany(companyArtists, companyName) :

    for x in companyArtists :

        for i in (rateCsvColumn["ID"] - 1) :

            if x == rateCsvColumn["MainArtist"][i] or re.search(r'\b; ' + x + ';', rateCsvColumn["ArtistList"][i]) != None :

                #print(i)
                songId = int(rateCsvColumn["ID"][i])

                companyCheck = rateCsvColumn["Company alignment"][i]

                if companyCheck == "" :

                    rateCsvColumn.loc[rateCsvColumn["ID"] == songId, ["Company alignment"]] = companyName
                    
                else :

                    rateCsvColumn.loc[rateCsvColumn["ID"] == songId, ["Company alignment"]] = f"{companyName}, {companyCheck}"

# ==================================================
# Adding data to column for actual number of songs per rate (including bonus songs)
# ==================================================

ratesList = list(dict.fromkeys(rateCsvColumn["R#"]))
ratesListNames = list(dict.fromkeys(rateCsvColumn["Rate"]))

songNumbersList = []

counting = rateCsvColumn["R#"].tolist()

placementArray = []

for x in ratesList :

    z = 0
    y = 0

    placementArray = []

    #for z in rateCsvColumn["ID"] - 1 :

    for i in rateCsvColumn["R#"] :


        y = y + 1
        #z = z + 1
        songId = rateCsvColumn.iloc[y-1]["ID"]
        #print(songId)
        #placementArray = []


        if x == i :

            z = z + 1
            #y = y + 1

            #placementArray = []

            placementArray.append(1)

            rateCsvColumn.loc[rateCsvColumn["R#"] == x, ["Num songs"]] = counting.count(x)
            #rateCsvColumn.loc[rateCsvColumn["R#"] == x, ["Num songs"]] = rateCsvColumn["/"]

        #if songId == rateCsvColumn["ID"][i] :

        #if rateCsvColumn["Placement"]

        #for z in rateCsvColumn["ID"] - 1 :

            #if x == i :
            print(songId)

            #placementArray.append(1)
            testInt = int(len(placementArray))
            rateCsvColumn.loc[rateCsvColumn["ID"] == songId, ["Placement"]] = z
            #print(rateCsvColumn["Placement"][i])
            #print(len(placementArray))
            #print(rateCsvColumn["Placement"])
            #print(type(testInt))
            #print(z)

    #z = z + 1

    '''else :

        placementArray = []'''

#z = 0
    placementArray = []
    #print("You are here")

#exit()
           

# ==================================================
# Adding company alignments to songs by artists from Big 4
# ==================================================

assignCompany(smArtists, "SM")
assignCompany(ygArtists, "YG")
assignCompany(jypeArtists, "JYPE")
assignCompany(hybeArtists, "HYBE")

deleteArray = []

for x in ratesList :

    deleteArray = []

    for i in rateCsvColumn["ID"] - 1 :

        if  x == rateCsvColumn["R#"][i] : # rateCsvColumn["Company alignment"][i] != "" and

            if rateCsvColumn["Company alignment"][i] != "" :

                deleteArray.append(1)

        if len(deleteArray) == 0 :

            if rateCsvColumn["R#"][i] == x :

                rateCsvColumn = rateCsvColumn.drop(i, axis = 0)
        
    deleteArray = []

# ==================================================
# Removing Best Of rate results and toggling which other rates to remove
# ==================================================

for i in (rateCsvColumn["ID"] - 1) :

    if nctShineeToggle == 0 :

        if rateCsvColumn["R#"][i] == 21 or rateCsvColumn["R#"][i] == 26 or rateCsvColumn["R#"][i] == 1 or rateCsvColumn["Company alignment"][i] == "" :

            rateCsvColumn = rateCsvColumn.drop(i, axis = 0)

    elif nctShineeToggle == 1 :

        if rateCsvColumn["R#"][i] == 5 or rateCsvColumn["R#"][i] == 8 or rateCsvColumn["R#"][i] == 1 or rateCsvColumn["Company alignment"][i] == "" :

            rateCsvColumn = rateCsvColumn.drop(i, axis = 0)

    elif nctShineeToggle == 2 :

        if rateCsvColumn["R#"][i] == 5 or rateCsvColumn["R#"][i] == 8 or rateCsvColumn["R#"][i] == 21 or rateCsvColumn["R#"][i] == 26 or rateCsvColumn["R#"][i] == 1 or rateCsvColumn["Company alignment"][i] == "" :

            rateCsvColumn = rateCsvColumn.drop(i, axis = 0)

    elif rateCsvColumn["R#"][i] == 1 or rateCsvColumn["Company alignment"][i] == "" :

        rateCsvColumn = rateCsvColumn.drop(i, axis = 0)

ratesList = list(dict.fromkeys(rateCsvColumn["R#"]))
print(ratesList)
print(len(ratesList))
ratesListNames = list(dict.fromkeys(rateCsvColumn["Rate"]))

# ==================================================
# Assigning company songs to a variable for easy access
# ==================================================

def companyQuery(companyName) :
    
    query = companyName
    return rateCsvColumn[rateCsvColumn["Company alignment"].str.contains(query)]
    #print(companySongs)

def songShow(companyEntries) :

    print(companyEntries)

ygSongs = companyQuery("YG")
smSongs = companyQuery("SM")
jypeSongs = companyQuery("JYPE")
hybeSongs = companyQuery("HYBE")

# ==================================================
# Don't have to call these, it's just to show the query results, can conduct calculations without printing them, can toggle off with #
# ==================================================

songShow(jypeSongs) 
#songShow(smSongs)
#songShow(ygSongs)
#songShow(hybeSongs)

# ==================================================
# BEGINNING OF STAT COLLECTING SECTION
# ==================================================

# ==================================================
# FUNCTIONS
# ==================================================

# ==================================================
# These prints are to show the raw average placements of each companies songs, can toggle them on or off with #
# ==================================================

def averagePlacement(companySongs, companyName) :

    print(f"The average placement of {companyName} songs is {round(companySongs.loc[:, "Placement"].mean(), 2)} place.")
    return round(companySongs.loc[:, "Placement"].mean(), 2),"tester dester"

# ==================================================
# Calculating the average percentile finish of each companies songs
# ==================================================

def averagePercentile(companySongs, companyName) :

    placementArray = np.array([companySongs["Placement"] - 1])
    #print(placementArray)
    songsInRateArray = np.array([companySongs["Num songs"] - 1])
    percentileArray = (placementArray / songsInRateArray) * 100
    #print(percentileArray)
    print(f"The average percentile finish of {companyName} songs is the {round(np.average(percentileArray), 2)} percentile.")
    #print(percentileArray.size)

def averagePercentilePerRate(companySongs) :

    allPercentilesArray = []
    songsPerRate = []
        
    for x in ratesList :

        testArray = []
        songsPerRateCount = []

        for i in (companySongs["ID"] - 1) :

            averageArray = []

            if x == companySongs["R#"][i] :

                placement = int(companySongs["Placement"][i]) - 1
                songsInRate = companySongs["Num songs"][i] - 1
                percentileX = float((placement / songsInRate) * 100)
                percentile = round(percentileX, 2)

                averageArray.append(percentile)

                if len(averageArray) == 0 :

                    testArray.append(0)
                    songsPerRateCount.append(0)

                else :

                    percentileAverage = sum(averageArray) / len(averageArray)

                    testArray.append(percentileAverage)
                    songsPerRateCount.append(1)

        testArrayAverage = float(np.average(testArray))
        songsPerRateTotal = len(songsPerRateCount)
        allPercentilesArray.append(round(testArrayAverage, 2))
        songsPerRate.append(songsPerRateTotal)


    allPercentilesArray1 = np.array(allPercentilesArray)
    songsPerRate1 = np.array(songsPerRate)

    return allPercentilesArray1, songsPerRate1

ygAveragePercentileArray, ygSongsPerRate = averagePercentilePerRate(ygSongs)[0], averagePercentilePerRate(ygSongs)[1]
print(ygAveragePercentileArray)
print("here", len(ygAveragePercentileArray))
smAveragePercentileArray, smSongsPerRate = averagePercentilePerRate(smSongs)[0], averagePercentilePerRate(smSongs)[1]
jypeAveragePercentileArray,jypeSongsPerRate = averagePercentilePerRate(jypeSongs)[0], averagePercentilePerRate(jypeSongs)[1]
hybeAveragePercentileArray,hybeSongsPerRate = averagePercentilePerRate(hybeSongs)[0], averagePercentilePerRate(hybeSongs)[1]

#print(ygSongsPerRate, smSongsPerRate, jypeSongsPerRate, hybeSongsPerRate)

def plotAveragePercentileLine() :

    xLabels = ratesListNames
    xTicks = np.array(ratesList)

    mask = np.arange(1, len(ratesList) + 1)
    allPercentilesArray1 = np.array(ygAveragePercentileArray)
    allPercentilesArray2 = np.array(smAveragePercentileArray)
    allPercentilesArray3 = np.array(jypeAveragePercentileArray)
    allPercentilesArray4 = np.array(hybeAveragePercentileArray)
    plotMask1 = np.isfinite(allPercentilesArray1)
    plotMask2 = np.isfinite(allPercentilesArray2)
    plotMask3 = np.isfinite(allPercentilesArray3)
    plotMask4 = np.isfinite(allPercentilesArray4)

    z = np.polyfit(mask[plotMask1], allPercentilesArray1[plotMask1], 1)
    z1 = np.polyfit(mask[plotMask2], allPercentilesArray2[plotMask2], 1)
    z2 = np.polyfit(mask[plotMask3], allPercentilesArray3[plotMask3], 1)
    z3 = np.polyfit(mask[plotMask4], allPercentilesArray4[plotMask4], 1)
    p = np.poly1d(z)
    p1 = np.poly1d(z1)
    p2 = np.poly1d(z2)
    p3 = np.poly1d(z3)

    stackTest = np.stack((xTicks, ygAveragePercentileArray), axis = 1)
    print(stackTest)

    fig, ax = plt.subplots()

    ax.plot(mask[plotMask1], allPercentilesArray1[plotMask1], "ks--", ms = 5, path_effects=[pe.Stroke(linewidth=1.5, foreground='k'), pe.Normal()], mec = "black", mew = 0.2)
    ax.plot(mask[plotMask2], allPercentilesArray2[plotMask2], "s--", ms = 5, color = "hotpink", path_effects=[pe.Stroke(linewidth=1.5, foreground='k'), pe.Normal()], mec = "black", mew = 0.2)
    ax.plot(mask[plotMask3], allPercentilesArray3[plotMask3], "s--", ms = 5, color = "darkorange", path_effects=[pe.Stroke(linewidth=1.5, foreground='k'), pe.Normal()], mec = "black", mew = 0.2)
    ax.plot(mask[plotMask4], allPercentilesArray4[plotMask4], "s--", ms = 5, color = "green", path_effects=[pe.Stroke(linewidth=1.5, foreground='k'), pe.Normal()], mec = "black", mew = 0.2)
    ax.plot(mask[plotMask1], p(mask[plotMask1]), "k-")
    ax.plot(mask[plotMask2], p1(mask[plotMask2]), "-", color = "hotpink")
    ax.plot(mask[plotMask3], p2(mask[plotMask3]), "-", color = "darkorange")
    ax.plot(mask[plotMask4], p3(mask[plotMask4]), "-", color = "green")
    ax.set_xlim(0, len(ratesList) + 1)
    ax.set_ylim(0, 100)
    ax.set_facecolor("aliceblue")
    ax.grid(True)
    ax.set_xticks(range(1, len(ratesList) + 1, 1))
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    ax.tick_params(axis = "x", labelrotation = 270)
    ax.set_xticklabels(xLabels)

    #plt.table([xLabels, xTicks, allPercentilesArray1])

    # use alpha property to change transparency

    #plt.mfc("black")

    plt.show()

    # do bar chart for average placements and percentiles

plt.rcParams["font.family"] = "sans-serif"
# plt.rcParams["font.serif"] = ["Times New Roman"]

def plotAveragePercentileTable() :

    stackTest = np.stack((ratesList, ratesListNames, ygAveragePercentileArray, smAveragePercentileArray, jypeAveragePercentileArray, hybeAveragePercentileArray, ygSongsPerRate, smSongsPerRate, jypeSongsPerRate, hybeSongsPerRate), axis = 1)
    columnHeads = ["R#", "Rate name", "YG", "SM", "JYPE", "HYBE", "YG#", "SM#", "JYPE#", "HYBE#"]
    print(stackTest)
    print(len(stackTest))

    listLen = len(ratesList)

    #smColour = np.full([6, ])
    emptyArray = np.full([listLen], "aliceblue")
    print(emptyArray)
    print(len(emptyArray))
    smColour = np.resize(["lavenderblush", "pink"], int(listLen))
    print(smColour)
    print(len(smColour))
    ygColour = np.resize(["whitesmoke", "lightgrey"], int(listLen))
    jypeColour = np.resize(["papayawhip", "moccasin"], int(listLen))
    hybeColour = np.resize(["honeydew", "palegreen"], int(listLen))

    colourMatrix = np.stack((emptyArray, emptyArray, ygColour, smColour, jypeColour, hybeColour, ygColour, smColour, jypeColour, hybeColour), axis = 1)
    print(colourMatrix)

    dataLength = len(stackTest)

    tableCellText = []

    for row in stackTest :

        tableCellText.append([f"{str(x)}" for x in row])

    #print(tableCellText)


    testText = ygAveragePercentileArray.tolist()
    print(testText)
    print(type(testText))
    print(type(ygAveragePercentileArray))

    columnColours = ["lightblue", "lightblue", "grey", "hotpink", "darkorange", "green", "grey", "hotpink", "darkorange", "green"]

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.box(on = None)

    table = plt.table(cellText = tableCellText, colLabels = columnHeads, cellLoc = "center", loc = "center", colColours = columnColours, cellColours = colourMatrix)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    #print(font)

    #table.scale(0.8, 1)

    cellDict = table.get_celld()
    for i in range(0,len(columnHeads)):
        cellDict[(0,i)].set_height(.08)
        for j in range(1,len(tableCellText)+1):
            cellDict[(j,i)].set_height(.05)

    plt.show()

plotAveragePercentileTable()

plotAveragePercentileLine()

smAvgPlacement = averagePlacement(smSongs, "SM")[0]
#testerdester = averagePlacement(smSongs, "SM")[1]
ygAvgPlacement = averagePlacement(ygSongs, "YG")[0]
jypeAvgPlacement = averagePlacement(jypeSongs, "JYPE")[0]
hybeAvgPlacement = averagePlacement(hybeSongs, "HYBE")[0]

print(smAvgPlacement)
#print(testerdester)

def plotAveragePercentileBar() :

    x = np.array(["SM", "YG", "JYPE", "HYBE"])
    print(len(x))
    y = np.array([smAvgPlacement, ygAvgPlacement, jypeAvgPlacement, hybeAvgPlacement])
    print(len(x))
    colours = ["hotpink", "black", "darkorange", "green"]

    plt.bar(x, y, color = colours, edgecolor = "black")

    plt.show()

plotAveragePercentileBar()

# ==================================================
# PRINTING THE STATS
# ==================================================

print(rateCsvColumn)

# ==================================================
# Average placement
# ==================================================

smAvgPlacement = averagePlacement(smSongs, "SM")
ygAvgPlacement = averagePlacement(ygSongs, "YG")
jypeAvgPlacement = averagePlacement(jypeSongs, "JYPE")
hybeAvgPlacement = averagePlacement(hybeSongs, "HYBE")

# ==================================================
# Average percentile finish
# ==================================================

smAvgPercentile = averagePercentile(smSongs, "SM")
ygAvgPercentile = averagePercentile(ygSongs, "YG")
jypeAvgPercentile = averagePercentile(jypeSongs, "JYPE")
hybeAvgPercentile = averagePercentile(hybeSongs, "HYBE")

#print(rateCsvColumn)