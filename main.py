from multiprocessing import connection
import requests
import time

r = requests.get('https://apps.pittcountync.gov/apps/health/restrate/Restaurant/Search/Score?minScore=0&maxScore=100')

#Gather
listOfUrls = r.text.splitlines()[59::12]
listOfNames = r.text.splitlines()[60::12]
listOfScores = r.text.splitlines()[67::12]

# Init empty lists for collection
listOfCodesClean = []
listOfUrlsClean = []
listOfNamesClean = []
listOfScoresClean = []
listOfDataset = []

for name in listOfNames:
   name=name[32:]
   listOfNamesClean.append(name)
for score in listOfScores:
    score=score[28:-5]
    listOfScoresClean.append(score)
for url in listOfUrls:
    url = url[37:-2]
    url = "https://apps.pittcountync.gov" + url
    listOfUrlsClean.append(url)

counter = 0
for url in listOfUrlsClean:
    if len(url) < 84:
        continue
    datasetList = []
    listOfCodesHere = []
    try:
        webpage = requests.get(url)
    except:
        print("Too Long")
        time.sleep(15)
        webpage = requests.get(url)

    codes = webpage.text.splitlines()[64::5]
    for code in codes:
        code = code[24:]
        code = code.replace('</td>', "")
        listOfCodesHere.append(code)

    listOfCleanCodesInner = []
    for code in listOfCodesHere:
        try:
            if code[0] in ['0','1','2','3','4','5','6','7','8','9', '.']:
                listOfCleanCodesInner.append(code)
        except IndexError:
            continue

    datasetList.append(listOfNamesClean[counter])
    datasetList.append(listOfScoresClean[counter])
    datasetList.append(", ".join(listOfCleanCodesInner))
    listOfDataset.append(datasetList)
    counter+=1

outputFile = open("data.txt","w")
for dataset in listOfDataset:
    outputFile.write("|".join(dataset))
    outputFile.write("\n")

    
    
