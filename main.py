import datetime
from zoneinfo import ZoneInfo
import re
import colorama as color

import mainFuncs as mFuncs
import otherFuncs as oFuncs

from getCredentials import getCreds as creds
from googleapiclient.discovery import build
from googleapiclient.model import HttpError

# initializing colorama
color.init()

# setting global color values
RESET = color.Fore.RESET
RED = color.Fore.RED
GREEN = color.Fore.GREEN


def main():
    try:
        service = build(
            "calendar", "v3", credentials=creds()
        )  # the center of this whole program, delete = program go brokie 😱

        calendarEntry = service.calendars().get(calendarId="primary").execute()
        userTimeZone = ZoneInfo(calendarEntry["timeZone"])
        timeNow = datetime.datetime.now(userTimeZone)
        timeOffset = timeNow.strftime("%z")
        dateToday = datetime.datetime.today().strftime("%Y-%m-%d")
        # i know this is a scuffed way to format it but fuck it,
        # if it works and it doesnt break anything, it works
        configuredOffset = f"{timeOffset[:3]}:{timeOffset[-2:]}"

        oFuncs.printFormat()  # shows the required format
        # print("Please enter the date and time according to the format shown above:")
        dateStart = input(f"\nStart Date (empty = {dateToday}): ")
        if len(dateStart) == 0:
            dateStart = dateToday
        dateEnd = input(f"End Date (empty = {dateStart}): ")
        if len(dateEnd) == 0:
            dateEnd = dateStart

        timeStart = input("\nStart Time (emtpy = 00:00:00): ")
        if len(timeStart) == 0:
            timeStart = "00:00:00"
        timeEnd = input("End Time (empty = 23:00:00): ")
        if len(timeEnd) == 0:
            timeEnd = "23:00:00"

        isFormatValid = mFuncs.formatValidator(dateStart, dateEnd, timeStart, timeEnd)
        if isFormatValid is not True:
            print(f"{RED}FAILURE: Format is not valid, please try again{RESET}")

        # NOTE: exclusion
        datesExcluded = None
        doExclusion = input(
            "\nDo you wish to add dates to exclude from the deletion process? [YES/no]: "
        ).lower()
        if doExclusion == "yes" or doExclusion != "no":
            # datesExcluded = mFuncs.exclusion(eventsEntries, timeOffset)
            datesExcluded = mFuncs.exclusion()
        elif doExclusion == "no":
            print("Continuing deletion without exclusion")
        else:
            print("ERROR: Answer not recognized")

        return "exit"  # NOTE: temporarily return here for testing
        # WARN: REMEMBER THESE 2 LINES OF CODE
        timeMinInclude = (
            f"{dateStart}T{timeStart}{configuredOffset}"  # NOTE: Starting Date
        )
        timeMaxInclude = f"{dateEnd}T{timeEnd}{configuredOffset}"  # NOTE: Ending Date
        # WARN: THEY ARE THE DELETION DATE RANGE

        eventsInDateRange = (
            service.events()
            .list(
                calendarId="primary",
                orderBy="startTime",
                timeMin=timeMinInclude,
                timeMax=timeMaxInclude,
                singleEvents=True,
                timeZone=userTimeZone,
            )
            .execute()
        )
        eventsEntries = eventsInDateRange.get("items", [])

        # NOTE: deletion
        if not eventsEntries:
            print("There are no events on the dates specified")
            return
        else:
            startDate = re.split(r"[T+]", timeMinInclude)
            endDate = re.split(r"[T+]", timeMaxInclude)
            print(
                "Google is going to delete all events starting from:\n",
                f"{startDate[0]} | {startDate[1]}, until:\n",
                f"{endDate[0]} | {endDate[1]}",
            )
            confirmation = input(
                "Are you sure you want to delete events in that specified date range? [yes/NO/view]: "
            )
            confirmation = confirmation.lower()
            if confirmation is None or confirmation == "no":
                return
            elif confirmation == "view":
                mFuncs.viewEvents(eventsEntries)
                return
            elif confirmation == "yes":
                # oFuncs.animateWorkingFunction(
                #     mFuncs.recursiveEventsDeletion(
                #         eventsEntries, service, datesExcluded
                #     )
                # )

                # WARN: the code below contains code that can DELETE events
                # be extremely careful when testing to try and not delete important events
                for event in eventsEntries:
                    eventID = event["id"]
                    print(f"Deleting {event['summary']}\nEventID: {eventID}\n")

                    # WARN: below is what deletes the events, be careful around here
                    # service.events().delete(
                    #     calendarId="primary", eventId=eventID, sendUpdates="all"
                    # ).execute()
            else:
                print("ERROR: Answer not recognized")
                return

    except HttpError as err:
        print(f"An error occured:\n{err}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interruption detected, exiting...")
