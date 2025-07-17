import datetime
from zoneinfo import ZoneInfo
import re
import colorama as color

import mainFuncs as mfuncs
import otherFuncs as ofuncs

from getCredentials import getCreds as creds
from googleapiclient.discovery import build
from googleapiclient.model import HttpError

color.init()

RESET = color.Fore.RESET
RED = color.Fore.RED
GREEN = color.Fore.GREEN


def main():
    try:
        service = build("calendar", "v3", credentials=creds())

        calendarEntry = service.calendars().get(calendarId="primary").execute()
        userTimeZone = ZoneInfo(calendarEntry["timeZone"])
        timeNow = datetime.datetime.now(userTimeZone)
        timeOffset = timeNow.strftime("%z")
        dateToday = datetime.datetime.today().strftime("%Y-%m-%d")
        # i know this is a scuffed way to do it but fuck it,
        # if it works and it doesnt break anything, it works
        configuredOffset = f"{timeOffset[:3]}:{timeOffset[-2:]}"

        ofuncs.printFormat()
        print("Please enter the date and time according to the format shown above")

        dateStart = input(f"\nStart Date (empty = {dateToday}): ")
        dateEnd = input(f"End Date (empty = {dateToday}): ")
        if len(dateStart) == 0:
            dateStart = dateToday
        if len(dateEnd) == 0:
            dateEnd = dateStart

        timeStart = input("\nStart Time (empty = 00:00:00): ")
        timeEnd = input("End Time (empty = 23:00:00): ")
        if len(timeStart) == 0:
            timeStart = "00:00:00"
        if len(timeEnd) == 0:
            timeEnd = "23:00:00"

        # validate format
        ifFormatValid = mfuncs.formatValidator(dateStart, dateEnd, timeStart, timeEnd)
        if ifFormatValid is not True:
            print(f"{RED}FAILURE: Format is not valid, please try again{RESET}")
            return "FORMAT ERROR"

        # WARN: REMEMBER THESE 2 LINES OF CODE
        timeMin = f"{dateStart}T{timeStart}{configuredOffset}"  # NOTE: Starting Date
        timeMax = f"{dateEnd}T{timeEnd}{configuredOffset}"  # NOTE: Ending Date
        # WARN: THEY ARE THE DATE RANGES

        eventsInDateRange = (
            service.events()
            .list(
                calendarId="primary",
                orderBy="startTime",
                timeMin=timeMin,
                timeMax=timeMax,
                singleEvents=True,
                timeZone=userTimeZone,
            )
            .execute()
        )
        eventsEntries = eventsInDateRange.get("items", [])

        if not eventsEntries:
            print("There are no events on the dates specified")
            return
        else:
            startDate = re.split(r"[T+]", timeMin)
            endDate = re.split(r"[T+]", timeMax)
            print(
                "\nGoogle is going to delete all events starting from:\n",
                f"{startDate[0]} | {startDate[1]}, until:\n",
                f"{endDate[0]} | {endDate[1]}",
            )
            confirmation = input(
                "Are you sure you want to delete events in that specified date range? [yes/NO/view]: "
            )
            confirmation = confirmation.lower()
            if confirmation is None:
                return
            elif confirmation == "no":
                return
            elif confirmation == "view":
                mfuncs.viewEvents(eventsEntries)
                return
            elif confirmation == "yes":
                # WARN: the code below contains code that can DELETE events
                # be extremely careful when testing to try and not delete important events
                for event in eventsEntries:
                    eventID = event["id"]
                    print(f"Deleting {event['summary']}\nEventID: {eventID}\n")

                    # WARN: below is what deletes the events, becareful when tinkering here
                    service.events().delete(
                        calendarId="primary", eventId=eventID, sendUpdates="all"
                    ).execute()
            else:
                print("Answer not recognized, please try again")
                return

    except HttpError as err:
        print(f"An error occured:\n{err}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interupption detected, exiting...")
