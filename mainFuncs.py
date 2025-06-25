import re
import time


def viewEvents(eventsInList):
    if not eventsInList:
        print("There are no events on this/these day(s)")
        return
    else:
        open("output.txt", "w").close()  # cleans the file before appending
        for event in eventsInList:
            # variables
            start = event["start"].get("dateTime")
            startConfigured = re.split(r"[T+]", start)
            creatorEmail = event["creator"].get("email")
            eventStatus = event["status"]
            try:
                recurringEventId = event["recurringEventId"]
            except KeyError:
                recurringEventId = "empty"
            eventId = event["id"]
            eventOrganizerEmail = event["organizer"].get("email")

            # log
            print("\n----------------------------------------------------------\n")

            print(
                f"Date: {startConfigured[0]}",
                f"\nTime: {startConfigured[1]}",
                f"\nTitle: {event['summary']}",
            )

            print("\nStatus (confirmed = active): %s" % eventStatus)
            print("Event Creator Email: %s" % creatorEmail)
            print("Event Organizer Email: %s" % eventOrganizerEmail)

            print("\nEventID:\n%s" % eventId)
            print(
                "Recurring EventID (empty = not a recurring event):\n%s"
                % recurringEventId
            )

            # output log
            with open("output.txt", "a") as out:
                out.write(
                    "\n----------------------------------------------------------\n"
                )

                out.write(
                    f"\nDate: {startConfigured[0]}\nTime:{startConfigured[1]}\nEvent Title: {event['summary']}\n"
                )

                out.write("\nStatus (confirmed = active): %s" % eventStatus)
                out.write("\nEvent Creator Email: %s" % creatorEmail)
                out.write("\nEvent Organizer Email: %s\n" % eventOrganizerEmail)

                out.write("\nEventID:\n%s" % eventId)
                out.write(
                    "\nRecurring EventID (empty = not a recurring event):\n%s\n"
                    % recurringEventId
                )
    print("Finished permanently deleting all events")
    print(
        '\nTo make sure you aren\'t removing the wrong events, a file named "output.txt" bes been made with the contents from the terminal into the current working directory/folder'
    )
    print(
        'Make sure to read the "output.txt" file before making your decision to delete'
    )


def recursiveEventsDeletion(entries, service):
    # NOTE: This is the main part where you want to be careful
    for event in entries:
        eventID = event["id"]
        print(f"Deleting {event['summary']}\nEventID: {eventID}\n")

        # WARN: Especially this
        # service.events().delete(
        #     calendarId="primary", eventId=eventID, sendUpdates="all"
        # ).execute()
        # NOTE: disabled temporarily for testing


def exclusion(eventList, timeOffset):
    print("Entering exclusion mode")

    # hehehe animation go brrr
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
    while True:
        print(anim[i % len(anim)], end="\r")
        time.sleep(0.08)
        i += 1
        if i == (anim.__len__()) * 2:
            break

    # the actual function code
    print(
        "Before adding your dates to exclude, please read this first.",
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

    excludedDates = {}
    dateAmount = 1
    loopIterations = int(input("Amount of dates to exclude: "))
    print("Please enter the required information:")
    for i in range(loopIterations):
        print("\nDate #%s" % dateAmount)
        date = input("Date: ")
        timeStart = input("Time Start: ")
        timeEnd = input("Time End: ")
        excludedDates[date] = {
            "startTime": f"{timeStart}{timeOffset}",
            "endTime": f"{timeEnd}{timeOffset}",
        }
        dateAmount += 1

    print(excludedDates)
