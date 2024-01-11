import csv
import sys
import datetime
import calendar
import holidays

print("hello world\n")

####################################################################################################
### Create datetime objects to define peak travel times.
### Some TfL stations have a few minutes "grace period", as described on the TfL website below
### https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-1798-1718
### However, I decided to use official peak times in case TfL changes their grace period policy.
####################################################################################################
morning_peak_start = datetime.time(6, 30)
morning_peak_end = datetime.time(9, 29)
evening_peak_start = datetime.time(16, 0)
evening_peak_end = datetime.time(18, 59)

'''
public_holidays = holidays.GB(subdiv="ENG", years=2024).items()
print(public_holidays)

test_date = datetime.date(2024, 12, 25)
print(test_date)
print("datetime.date({0}, {1}, {2})".format(test_date.year, test_date.month, test_date.day) in public_holidays)
print(type(public_holidays))
'''

####################################################################################################
### Journey objects store one row of data from TfL's CSV output of all underground travel.
####################################################################################################
class Journey:
    date = None

    def __init__(self, date, start_time, end_time, journey_or_action, charge, credit, balance, note):
        self.date = datetime.date(int(date[7:]), 
                                  list(calendar.month_abbr).index(date[3:6]), 
                                  int(date[:2]))
        self.start_time = datetime.time(int(start_time[:2]), 
                                        int(start_time[3:]))
        self.end_time = end_time
        self.journey_or_action = journey_or_action
        self.charge = float(charge)
        self.credit = credit
        self.balance = balance
        self.note = note
    
    def is_weekend(self):
        return self.date.isoweekday() < 6
    
    def is_public_holiday(self):
        #return self.date in holidays.GB(subdiv="ENG", years=2023).items()
        return False
    
    def is_off_peak_time(self):
        during_morning_peak = morning_peak_start <= self.start_time <= morning_peak_end
        during_evening_peak = evening_peak_start <= self.start_time <= evening_peak_end
        return not during_morning_peak and not during_evening_peak
    
    def off_peak_savings(self):
        return (self.charge * 0.5)


####################################################################################################
### Open the CSV file and create a reader for it.
### Skip the first row (blank) and second row (header).
####################################################################################################
travel_logs = open(sys.argv[1])
log_reader = csv.reader(travel_logs, delimiter=',')
next(log_reader)
next(log_reader)


####################################################################################################
### Create a Journey object for each row of the input and add all the Journeys to a list.
####################################################################################################
all_journeys = []
for row in log_reader:
    if len(row[4]) > 0:
        all_journeys.append(Journey(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    #date_string = str(row[0])
    #print("Year {0}\t Month: {1}\t Day: {2}".format(date_string[7:], list(calendar.month_abbr).index(date_string[3:6]), date_string[:2]))
    #print("Date: {0} is type {1}".format(date_string, type(date_string)))


total_savings = 0
for journey in all_journeys:
    #print(journey.is_off_peak_time() or journey.is_weekend())
    if journey.is_off_peak_time() or journey.is_weekend():
        total_savings += journey.off_peak_savings()
    #print(journey.start_time)
    #print(journey.is_off_peak_time())
    #print("\n")

print("You saved a total of {0} GBP in this period by travelling off-peak".format(round(total_savings, 2)))