import datetime
from zoneinfo import ZoneInfo
import re

from getCredentials import getCreds as creds
from googleapiclient.discovery import build
from googleapiclient.model import HttpError


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


def main():
    try:
        service = build("calendar", "v3", credentials=creds())

        calendarEntry = service.calendars().get(calendarId="primary").execute()
        userTimeZone = ZoneInfo(calendarEntry["timeZone"])
        timeNow = datetime.datetime.now(userTimeZone)
        timeOffset = timeNow.strftime("%z")
        # i know this is a scuffed way to do it but fuck it,
        # if it works and it doesnt break anything, it works
        configuredOffset = f"{timeOffset[:3]}:{timeOffset[-2:]}"

        # WARN: REMEMBER THESE 2 LINES OF CODE
        min = f"2025-06-23T00:00:00{configuredOffset}"  # NOTE: Starting Date
        max = f"2025-06-23T23:00:00{configuredOffset}"  # NOTE: Ending Date
        # WARN: THEY ARE THE DATE RANGES

        eventsInDateRange = (
            service.events()
            .list(
                calendarId="primary",
                orderBy="startTime",
                timeMin=min,
                timeMax=max,
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
            # WARN: the code below contains code that can DELETE events
            # be extremely careful when testing to try and not delete important events
            startDate = re.split(r"[T+]", min)
            endDate = re.split(r"[T+]", max)
            print(
                "Google is going to delete all events starting from:\n",
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
                viewEvents(eventsEntries)
                return
            elif confirmation == "yes":
                # NOTE: This is the main part where you want to be careful
                for event in eventsEntries:
                    eventID = event["id"]
                    print(f"Deleting {event['summary']}\nEventID: {eventID}\n")

                    # WARN: Especially this
                    service.events().delete(
                        calendarId="primary", eventId=eventID, sendUpdates="all"
                    ).execute()
            else:
                print("Answer not recognized, please try again")
                return

    except HttpError as err:
        print(f"An error occured:\n{err}")


if __name__ == "__main__":
    main()
