import time
import datetime
from zoneinfo import ZoneInfo
import re

import mainFuncs as funcs

from getCredentials import getCreds as creds
from googleapiclient.discovery import build
from googleapiclient.model import HttpError


def main():
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

    try:
        service = build("calendar", "v3", credentials=creds())

        calendarEntry = service.calendars().get(calendarId="primary").execute()
        userTimeZone = ZoneInfo(calendarEntry["timeZone"])
        timeNow = datetime.datetime.now(userTimeZone)
        timeOffset = timeNow.strftime("%z")
        # i know this is a scuffed way to format it but fuck it,
        # if it works and it doesnt break anything, it works
        configuredOffset = f"{timeOffset[:3]}:{timeOffset[-2:]}"

        # WARN: REMEMBER THESE 2 LINES OF CODE
        timeMinInclude = f"2025-06-23T00:00:00{configuredOffset}"  # NOTE: Starting Date
        timeMaxInclude = f"2025-06-25T23:00:00{configuredOffset}"  # NOTE: Ending Date
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

        # NOTE: exclusion
        doExclusion = input(
            "Do you wish to add dates to exclude from the deletion process? [YES/no]: "
        ).lower()
        if doExclusion == "yes" or doExclusion != "no":
            datesExcluded = funcs.exclusion(eventsEntries, timeOffset)
        elif doExclusion == "no":
            print("Continuing deletion without exclusion")
        else:
            print("ERROR: Answer not recognized")

        # NOTE: deletion
        if not eventsEntries:
            print("There are no events on the dates specified")
            return
        else:
            # WARN: the code below contains code that can DELETE events
            # be extremely careful when testing to try and not delete important events
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
                funcs.viewEvents(eventsEntries)
                return
            elif confirmation == "yes":
                i = 0
                while funcs.recursiveEventsDeletion(eventsEntries, service):
                    print(anim[i % len(anim)], end="\r")
                    time.sleep(0.08)
                    i += 1
            else:
                print("ERROR: Answer not recognized")
                return

    except HttpError as err:
        print(f"An error occured:\n{err}")


if __name__ == "__main__":
    main()
