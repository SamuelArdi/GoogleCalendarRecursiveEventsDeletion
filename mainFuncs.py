import calendar
import re
import time as tm
import colorama as color
from requests import get

# initialize colorama
color.init()

RESET = color.Fore.RESET
RED = color.Fore.RED
GREEN = color.Fore.GREEN


class formatFunctions:
    def validateFormat(self, format, input, type):
        idx = 0
        for formatChar in format:
            if input[idx].isnumeric() is formatChar.isnumeric():
                # check if the separator is correct
                idx += 1
            else:
                # TODO: make the error message better
                print(
                    f"{RED}ERROR: {RESET}{input} does not match expected format at {input[:idx]}{RED}[{input[idx]}]{RESET}, the format expected is {input[:idx]}{GREEN}[{formatChar}]{RESET}"
                )
                return f"{type.upper()} FORMAT ERROR"

    def validateSeparator(self, separator, input, type):
        # instantly check with position based on type
        if type == "date":
            # 0000-00-00
            positions = [4, 7]
            for pos in positions:
                if ord(input[pos]) != ord(separator):
                    print(
                        f"{RED}ERROR: {RESET}Unexpected input separator at {input[:pos]}{RED}[{input[pos]}]{RESET}, expected separator {input[:pos]}{GREEN}[{separator}]{RESET}"
                    )
                    return "DATE SEPARATOR ERROR"

    def validDay(self, day, month, year):
        if int(day) > 31:
            print(RED + f"ERROR: {year}-{month}-[{day}], day can't be higher than 31")
            return "DATE DAY ERROR"
        elif day < 1:
            print(RED + f"ERROR: {year}-{month}-[0{day}], day can't be lower than 01")
            return "DATE DAY ERROR"

    def validDayLeap(self, day, month, year, isLeapYear):
        # if its a leap year
        if isLeapYear and day > 29:
            print(
                RED
                + f"ERROR: {year}-{month}-[{day}], day can't be higher than 29 on Febuary leap year"
            )
            return "DATE DAY ERROR"
        elif isLeapYear and day < 1:
            print(
                RED
                + f"ERROR: {year}-{month}-[{day}], day can't be higher than 28 on Febuary non-leap year"
            )
            return "DATE DAY ERROR"

        # if not leap year
        elif isLeapYear and day > 28:
            print(RED + "ERROR: Day can't be higher than 28 on Febuary non-leap year")
            return "DATE DAY ERROR"
        elif isLeapYear and day < 1:
            print(RED + "ERROR: Day can't be lower than 01")
            return "DATE DAY ERROR"


def viewEvents(eventsInList):
    if not eventsInList:
        print("There are no events on this date range")
        return
    else:
        # TODO: somtime later make this a .json file instead of a plain txt,
        # so it would ACTUALLY be easier to read than in the terminal
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

            # logging
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


# TODO: work on the exclusion thingy after the format validation
def recursiveEventsDeletion(entries, service, excluded):
    # WARN: the code below contains code that can DELETE events
    # be extremely careful when testing to try and not delete important events
    for event in entries:
        eventID = event["id"]
        print(f"Deleting {event['summary']}\nEventID: {eventID}\n")

        # WARN: below is what deletes the events, be careful around here
        service.events().delete(
            calendarId="primary", eventId=eventID, sendUpdates="all"
        ).execute()


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
        tm.sleep(0.08)
        i += 1
        if i == (anim.__len__()) * 2:
            break

    # the actual function code
    excludedDates = {}
    dateAmount = 1
    loopIterations = int(input("Amount of dates to exclude: "))
    print("Please enter the required information:")
    print("\nThe date and time format is the same as shown above")
    for i in range(loopIterations):
        print("\nDate #%s" % dateAmount)
        # TODO: check if the date and time is in the correct format
        date = input("Date: ")
        timeStart = input("Time Start: ")
        timeEnd = input("Time End: ")
        excludedDates[date] = {
            "startTime": f"{timeStart}{timeOffset}",
            "endTime": f"{timeEnd}{timeOffset}",
        }
        dateAmount += 1

    print(excludedDates)


def formatValidator(startDate, endDate, timeStart, timeEnd):
    n = int()
    correctFormat = {
        "dateFormat": f"{n}{n}{n}{n}-{n}{n}-{n}{n}",
        "timeFormat": f"{n}{n}:{n}{n}:{n}{n}",
    }
    funcs = formatFunctions()

    # NOTE: validating dates
    dateVars = [startDate, endDate]
    for inputDate in dateVars:
        output = funcs.validateFormat(correctFormat["dateFormat"], inputDate, "date")
        if output == "DATE FORMAT ERROR":
            return output

    for inputDate in dateVars:
        output = funcs.validateSeparator("-", inputDate, "date")
        if output == "DATE SEPARATOR ERROR":
            return output
    print(
        f"{GREEN}SUCCESS: {RESET}The input date format matches with the expected format"
    )

    # check if the dates are actually correct
    for date in dateVars:
        try:
            year = int(date[:4])
            month = int(date[5:-3])
            day = int(date[8:])

            # check year
            # this is may be weird, but ill just set the highest as 3000
            # and the lowest ill set it to 1900
            if year > 3000:
                print(RED + "ERROR: Year can't be higher than 2100")
                return "DATE YEAR ERROR"
            elif year < 1900:
                print(RED + "ERROR: Year can't be lower than 1900")
                return "DATE YEAR ERROR"
            # check month
            if month > 12:
                print(
                    RED + f"ERROR: month doesn't exist {date[:-5]}[{month}]{date[7:]}"
                )
                return "DATE MONTH ERROR"
            elif month < 1:
                print(
                    RED + f"ERROR: month doesn't exist {date[:-5]}[{month}0]{date[7:]}"
                )
                return "DATE MONTH ERROR"

            # check day
            if month == 2:  # check if this year is a leap year
                if calendar.isleap(year):
                    log = funcs.validDayLeap(day, month, year, True)
                    if log == "DATE DAY ERROR":
                        return log
                else:
                    log = funcs.validDayLeap(day, month, year, False)
                    if log == "DATE DAY ERROR":
                        return log
            else:
                log = funcs.validDay(day, month, year)
                if log == "DATE DAY ERROR":
                    return log
        except ValueError:
            lastHyphen = date.rfind("-")
            getDay = lastHyphen + 1
            overLen = len(date[getDay + 2 :])
            print(
                f"{RED}ERROR: {RESET}Unexpected input date day on {date[: lastHyphen + 1]}{RED}[{date[getDay:]}]{RESET}, expected input {date[: lastHyphen + 1]}{GREEN}[{date[getDay:-overLen]}]{RESET}"
            )
            return "DATE DAY FORMAT ERROR"
    print(f"{GREEN}SUCCESS: {RESET}Date values matches with expected values")

    # NOTE: validating time
    timeVars = [timeStart, timeEnd]
    for timeInput in timeVars:
        output = funcs.validateFormat(correctFormat["timeFormat"], timeInput, "time")
        if output == "TIME FORMAT ERROR":
            return output
    print(f"{GREEN}SUCCESS: {RESET}The time format matches with the expected format")

    for time in timeVars:
        try:
            # hh:mm:ss
            hour = int(time[:2])
            minute = int(time[3:-3])
            second = int(time[6:])

            # validate hour
            if hour > 23:
                print(
                    RED
                    + f"ERROR: [{hour}]:{minute}:{second} Hour can't be higher than 23"
                )
                return "TIME HOUR ERROR"
            elif hour < 0:
                print(
                    RED
                    + f"ERROR: [0{hour}]:{minute}:{second} Hour can't be lower than 01"
                )
                return "TIME HOUR ERROR"

            # validate minute
            if minute > 59:
                print(
                    RED
                    + f"ERROR: {hour}:[{minute}]:{second} Minute can't be higher than 59"
                )
                return "TIME MINUTE ERROR"
            elif minute < 0:
                print(
                    RED
                    + f"ERROR: {hour}:[0{minute}]:{second} Minute can't be lower than 01"
                )
                return "TIME MINUTE ERROR"

            # validate second
            if second > 59:
                print(
                    RED
                    + f"ERROR: {hour}:{minute}:[{second}] Second can't be higher than 59"
                )
                return "TIME SECOND ERROR"
            elif second < 0:
                print(
                    RED
                    + f"ERROR: {hour}:{minute}:[0{second}] Second can't be lower than 01"
                )
                return "TIME SECOND ERROR"
        except ValueError:
            lastColon = time.rfind(":")
            getSecond = lastColon + 1
            overLen = len(time[getSecond + 2 :])
            print(
                f"{RED}ERROR: {RESET}Unexpeced input time seconds on {time[: lastColon + 1]}{RED}[{time[getSecond:]}]{RESET}, expected input {time[: lastColon + 1]}{GREEN}[{time[getSecond:-overLen]}]{RESET}"
            )
            return "TIME SECOND FORMAT ERROR"
    print(f"{GREEN}SUCCESS: {RESET}Time values matches with expected values")
