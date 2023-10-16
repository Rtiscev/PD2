import os
import requests
import datetime
from dateutil.relativedelta import relativedelta

translations = {"Ю": "S", "С": "N", "З": "W", "В": "E", "м": "m", "с": "s"}


def getSimpleParts(source, beginning, ending):
    data = ""
    BrIndex = source.find("<br />")
    positiveIndex = source.find("<td class='first_in_group'>")
    # if positive Found
    nullIndex = source.find("label_icon label_small screen_icon")
    if nullIndex != -1:
        data = "null"
    elif positiveIndex != -1:
        startIndex = source.find("<td class='first_in_group'>")
        endIndex = source.find(ending, startIndex)
        data = source[startIndex + len("<td class='first_in_group'>") : endIndex]
    # if <br/> is not found
    elif BrIndex == -1:
        startIndex = source.find(beginning)
        endIndex = source.find(ending, startIndex)
        data = source[startIndex + len(beginning) : endIndex]
    # if <br/> is found (there won't be other conditins here)
    else:
        BrSpanIndex = source.find("</span></td>")
        data = source[BrIndex + len("<br />") : BrSpanIndex]
    return data


def russianWindNotationsToEnglish(source):
    data = ""
    for str in source:
        isFound = False
        savedValue = ""
        for key in translations:
            if key == str:
                isFound = True
                savedValue = translations[key]
        data += savedValue if isFound else str

    return data


# if it exists, delete it
if os.path.exists("dataset.csv"):
    os.remove("dataset.csv")

# save current Date
currentDate = datetime.date.today()

# open file in append Mode (why not)
with open("dataset.csv", "a") as dataset:
    for day in range(30):
        currentDate -= (
            relativedelta(months=0) if (day == 0) else relativedelta(months=1)
        )

        response = requests.get(
            f"https://www.gismeteo.ru/diary/4980/{currentDate.year}/{currentDate.month}/",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
        )

        startIndex = response.text.find("<tbody>")
        endIndex = response.text.find("</tbody>", startIndex)
        finalString = response.text[startIndex : endIndex + len("<tbody>")]

        currentposition = 0
        appendData = []

        while True:
            toBeAppended = ""

            startCenter = finalString.find('<tr align="center">', currentposition)
            if startCenter == -1:
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

            # date
            toBeAppended += f"{currentDate.year}/{currentDate.month}" + ","
            # 0 counter
            toBeAppended += getSimpleParts(arr[0], "<td class=first>", "</td>") + ","
            # 1D temp
            toBeAppended += (
                getSimpleParts(arr[1], "<td class='first_in_group positive'>", "</td>")
                + ","
            )
            # 2D pressure
            toBeAppended += getSimpleParts(arr[2], "<td>", "</td>") + ","
            # 5D wind
            toBeAppended += (
                russianWindNotationsToEnglish(
                    getSimpleParts(arr[5], "<td><span>", "</span></td>")
                )
                + ","
            )
            # 6N temp
            toBeAppended += (
                getSimpleParts(arr[6], "<td class='first_in_group positive'>", "</td>")
                + ","
            )
            # 7N pressure
            toBeAppended += getSimpleParts(arr[7], "<td>", "</td>") + ","
            # 10N wind
            toBeAppended += (
                russianWindNotationsToEnglish(
                    getSimpleParts(arr[10], "<td><span>", "</span></td>")
                )
                + "\n"
            )
            appendData.append(toBeAppended)

        for item in appendData:
            dataset.write(item)
