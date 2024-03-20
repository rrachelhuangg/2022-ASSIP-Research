import matplotlib.pyplot as plot
from plotly.graph_objs import Bar, Layout
from plotly import offline
import json
import os

def visualizeComparisons():
        plot.style.use("seaborn-notebook")
        titles = returnTitlesforVisualization("Song Comparisons")
        numbers = []
        for title in titles:
            numbers.append(compareData(title, "Song Comparisons"))
        fig = plot.figure(figsize = (11, 6))
        plot.bar(titles[5:15], numbers[5:15], color = "blue", width = 0.5)
        plot.xlabel("Compared Song Titles")
        fig.autofmt_xdate()
        plot.ylabel("Comparison in Number Format")
        plot.title("Comparing Songs")
        plot.savefig("Visualization.png", bbox_inches = "tight")
        plot.show()

def returnTitlesforVisualization(inputSong):
    musicDatabase = "data/Music Database.json"
    comparisons = "data/Comparisons.json"
    count = 0
    songs = []
    titles = []
    index = 0
    with open(comparisons, "w") as file:
        with open(musicDatabase) as file_obj:
            lines = file_obj.readlines()
            for line in lines:
                if "Title:" in line:
                    titles.append(line[7:])
    return titles

def returnComparisonsforVisualization(inputSong):
    musicDatabase = "data/Music Database.json"
    comparisons = "data/Comparisons.json"
    count = 0
    songs = []
    titles = []
    index = 0
    with open(comparisons, "w") as file:
        with open(musicDatabase) as file_obj:
            lines = file_obj.readlines()
            for line in lines:
                if "Title:" in line:
                    songs.append(str(compareData(line[7:], inputSong)) + "\n")
                    titles.append(line)
    return songs
    
def recommendSong(inputSong):
    musicDatabase = "data/Music Database.json"
    comparisons = "data/Comparisons.json"
    count = 0
    songs = []
    titles = []
    index = 0
    with open(comparisons, "w") as file:
        with open(musicDatabase) as file_obj:
            lines = file_obj.readlines()
            
            for line in lines:
                if "Title:" in line:
                    file.write(str(compareData(line[7:], inputSong)) + "\n")
                    songs.append(str(compareData(line[7:], inputSong)) + "\n")
                    titles.append(line)
    closest = min([int(i) for i in songs])
    for song in range(len(songs)):
        if int(songs[song]) == closest:
            index = song
            break
    closestSong = titles[index]
    print("The most similar song in the database to your input song is:", closestSong[7:])
    

def compareData(song1, song2):
    with open("data/Music Database.json") as f:
        contents = f.readlines()
    lineCount1 = 0
    lineCount2 = 0
    startOne = 0
    startTwo = 0
    notes1 = ""
    notes2 = ""
    for content in contents: 
        lineCount1 += 1
        lineCount2 += 1 
        if song1 in content: 
            startOne = lineCount1 + 2 
            continue
        if song2 in content:
            startTwo = lineCount2 + 2
            continue 
    for a in range(startOne-1, startOne + 5): 
        notes1 += contents[a]
    for b in range(startTwo-1, startTwo + 5):
        notes2 += contents[b]
    notes = "abcdefgABCDEFG"
    cleanedNotes1 = ""
    cleanedNotes2 = ""
    for char in notes1:
        if char in notes:
            cleanedNotes1 += char
    for char2 in notes2:
        if char2 in notes:
            cleanedNotes2 += char2
    return match(cleanedNotes1, cleanedNotes2)
    

def writeData(path):
    musicDatabase = "data/Music Database.json"
    os.chdir(path)
    with open(musicDatabase, "w") as file_obj:
        for file in os.listdir():
            file_obj.write(readData(file))


def readData(fileName): 
     with open(fileName) as file_object:
        title = ""
        notes = ""
        lineCount = 0
        startIndex = 0
        alphabet = "abcdefg[]()z"
        lines = file_object.readlines()
        for line in lines:
           lineCount += 1
           if line[0:2] == "T:":
               title += line[2:].lstrip()
           if "p!" in line[0:100]:
               startIndex = lineCount
               break
           if line[1] in alphabet:
               startIndex = lineCount
               break
        for n in range(startIndex-1, len(lines) - 1):
            if len(notes) < 500:
                notes += lines[n]
        return "Title: " + title + "\n" + "Notes: " + notes + "\n"

def match(str1, str2): #analyzes temporal patterns and chromatic scale values
    length1 = len(str1)
    length2 = len(str2)
    grid = [ [ 0 for y in range(length1 + 1)] for x in range(length2 + 1)] 
    noteValues = {"C":1, "D":2, "E":3, "F":4, "G":5, "A":6, "B":7}
    genericPatterns = ["AAAA", "ABAB"]
    for baseCaseH in range(length1 + 1):
        grid[0][baseCaseH] = baseCaseH
    for baseCaseV in range(length2 + 1):
        grid[baseCaseV][0] = baseCaseV
    count = 0
    for i in range(1, length1):
        for j in range(1, length2):
            if patternConverter(str1[i-1:i+3]) == patternConverter(str2[j-1:j+3]):
                count += 1
            if str1[i-1] == str2[j-1]:
                grid[j][i] = grid[j-1][i-1]
            else:
                grid[j][i] = min((grid[j-1][i-1] + 1),(grid[j-1][i] + 1),(grid[j][i-1] + 1))         
    valueOnestringOne = 0
    valueOnestringTwo = 0
    valueTwostringOne = 0
    valueTwostringTwo = 0
    for key in noteValues.keys():
        if str1[0].upper() == key:
            valueOnestringOne = noteValues[key]
        if str2[0].upper() == key:
            valueOnestringTwo = noteValues[key]
        if str1[1].upper() == key:
            valueTwostringOne = noteValues[key]
        if str2[1].upper() == key:
            valueTwostringTwo = noteValues[key]
    differenceOne = abs(valueTwostringOne - valueOnestringOne)
    differenceTwo = abs(valueTwostringTwo - valueOnestringTwo)
    check = abs(differenceTwo - differenceOne)
    return abs(grid[length2 - 1][length1 - 1] - count) + check


def patternConverter(inputString):
    genericString = ""
    a = inputString[0]
    if inputString[1] != inputString[0]:
        b = inputString[1]
    else:
        b = a
    for char in inputString:
        if char == a:
            genericString += "A"
        elif char == b:
            genericString += "B"
        else:
            genericString += char     
    return genericString


def printGrid(gridToPrint):
    for line in gridToPrint:
        print(" ".join(map(str, line))) 

def main():
    run = True
    while(run):
        visualizeComparisons()
        runAgain = input("Run again? (y/n)")
        if runAgain == "n":
            run = False

main()









