import datetime
from inspect import _empty
from zoneinfo import ZoneInfo
import re

import mainFuncs as mFuncs
import otherFuncs as oFuncs

from getCredentials import getCreds as creds
from googleapiclient.discovery import build
from googleapiclient.model import HttpError


def main():
    try:
        service = build(
            "calendar", "v3", credentials=creds()
        )  # the center of this whole program, delete = program go brokie 😱

        calendarEntry = service.calendars().get(calendarId="primary").execute()
        userTimeZone = ZoneInfo(calendarEntry["timeZone"])
        timeNow = datetime.datetime.now(userTimeZone)
        timeOffset = timeNow.strftime("%z")
        # i know this is a scuffed way to format it but fuck it,
        # if it works and it doesnt break anything, it works
        configuredOffset = f"{timeOffset[:3]}:{timeOffset[-2:]}"

        oFuncs.printFormat()  # shows the required format
        # print("Please enter the date and time according to the format shown above:")
        dateMin = input("\nStart Date: ")
        dateMax = input(f"End Date (empty = {dateMin}): ")
        if len(dateMax) == 0:
            dateMax = dateMin
        # timeMin = input("\nStart Time: ")
        # timeMax = input("End Time (empty = 23:00:00): ")
        # if len(timeMax) == 0:
        #     timeMax = "23:00:00"
        mFuncs.formatValidator(dateMin, dateMax, timeMin = "00:00:00", timeMax = "23:00:00")
        return  # NOTE: exit here for testing

        # WARN: REMEMBER THESE 2 LINES OF CODE
        timeMinInclude = f"2025-06-23T00:00:00{configuredOffset}"  # NOTE: Starting Date
        timeMaxInclude = f"2025-06-27T23:00:00{configuredOffset}"  # NOTE: Ending Date
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
        datesExcluded = None
        doExclusion = input(
            "Do you wish to add dates to exclude from the deletion process? [YES/no]: "
        ).lower()
        if doExclusion == "yes" or doExclusion != "no":
            datesExcluded = mFuncs.exclusion(eventsEntries, timeOffset)
        elif doExclusion == "no":
            print("Continuing deletion without exclusion")
        else:
            print("ERROR: Answer not recognized")

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
                oFuncs.animateWorkingFunction(
                    mFuncs.recursiveEventsDeletion(
                        eventsEntries, service, datesExcluded
                    )
                )
            else:
                print("ERROR: Answer not recognized")
                return

    except HttpError as err:
        print(f"An error occured:\n{err}")


if __name__ == "__main__":
    main()
