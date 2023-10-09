import requests

def getSimpleParts(source, beginning, ending):
    data = ""
    BrIndex = source.find("<br />")
    if BrIndex == -1:
        startIndex = source.find(beginning)
        endIndex = source.find(ending, startIndex)
        data = source[startIndex + len(beginning) : endIndex]
    else:
        BrSpanIndex = source.find("</span></td>")
        data = source[BrIndex + len("<br />") : BrSpanIndex]
    return data


response = requests.get(
    "https://www.gismeteo.ru/diary/4980/2023/9/",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
)

# full body of the .html
# with open("readme.html", "w") as f:
#     f.write(response.text)


startIndex = response.text.find("<tbody>")
endIndex = response.text.find("</tbody>", startIndex)
finalString = response.text[startIndex : endIndex + len("<tbody>")]

# creating the file as .html
# print(finalString)
# with open("final.html", "w") as file:
#     file.write(finalString)

currentposition = 0
with open ("dataset.csv","w") as dataset:
    appendData=[]
    while True:
        toBeAppended=""
        
        startCenter = finalString.find('<tr align="center">', currentposition)
        if startCenter==-1:
            break
        endCenter = finalString.find("</tr>", startCenter)
        currentposition = endCenter + len("</tr>")

        finalCenter = finalString[startCenter : endCenter + len("</tr>")]

        arr = []
        incremental = 0

        while finalCenter.find("<td", incremental) != -1:
            beginningIndex = finalCenter.find("<td", incremental)
            endingIndex = finalCenter.find("</td>", beginningIndex)
            incremental = endingIndex
            string = finalCenter[beginningIndex : endingIndex + len("</td>")]
            arr.append(string)

        # 0 counter
        print(getSimpleParts(arr[0], "<td class=first>", "</td>"))
        # 1D temp
        print(getSimpleParts(arr[1], "<td class='first_in_group positive'>", "</td>"))
        # 2D pressure
        print(getSimpleParts(arr[2], "<td>", "</td>"))
        # 5D wind
        print(getSimpleParts(arr[5], "<td><span>", "</span></td>"))
        # 6N temp
        print(getSimpleParts(arr[6], "<td class='first_in_group positive'>", "</td>"))
        # 7N pressure
        print(getSimpleParts(arr[7], "<td>", "</td>"))
        # 10N wind
        print(getSimpleParts(arr[10], "<td><span>", "</span></td>"))
        
        print("--------------------")


# 0         COUNTER
# 1,2,5     DAY
# 6,7,10    EVENING
