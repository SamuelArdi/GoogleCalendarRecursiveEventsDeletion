import time


def printFormat():
    print(
        "Before adding your date and time, please read this first.",
        "\nThese are the format you'll need to enter in:\n",
        "\n----------------------------------------------------------",
        "\nDate format:",
        # date
        "\nDate: YYYY-MM-DD",
        "\nY = Year",
        "\nM = Month",
        "\nD = Day\n",
        # time
        "\nTime format",
        "\nTime: HH:MM:SS",
        "\nH = Hour (This uses the 24h format)",
        "\nM = Minute",
        "\nS = Second",
        "\n----------------------------------------------------------\n",
        "\n----------------------------------------------------------",
        # examples
        "\nExample 1:",
        "\nDate: 2025-06-25",
        "\nStart Time: 16:00:00",
        "\nEnd Time: 22:00:00\n"
        # example 2
        "\nExample 2:",
        "\nDate: 2008-07-18",
        "\nStart Time: 13:00:00",
        "\nEnd Time: 15:00:00\n"
        # example 3
        "\nExample 3:",
        "\nDate: 2004-02-12",
        "\nStart Time: 07:00:00",
        "\nEnd Time: 18:00:00",
        "\n----------------------------------------------------------\n",
    )


def animateWorkingFunction(functionWorking):
    anim = [
        # to upper case
        "loading",
        "Loading",
        "LOading",
        "LOAding",
        "LOADing",
        "LOADIng",
        "LOADINg",
        "LOADING",
        # back to lower case
        "lOADING",
        "loADING",
        "loaDING",
        "loadING",
        "loadiNG",
        "loadinG",
        "loading",
    ]

    i = 0
    while functionWorking:
        print(anim[i % len(anim)], end="\r")
        time.sleep(0.08)
        i += 1
