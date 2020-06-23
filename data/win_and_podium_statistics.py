from collections import Counter
import numpy as np
# open datafile, extract content into an array, and close.

datafile = open('drivers.csv', 'r')
driver_content = datafile.readlines()
datafile.close()


datafile = open('driver_standings.csv', 'r')
driver_standings_content = datafile.readlines()
datafile.close()

datafile = open('lap_times.csv', 'r')
lap_times_content = datafile.readlines()
datafile.close()

datafile = open('circuits.csv', 'r')
circuit_content = datafile.readlines()
datafile.close()

datafile = open('constructors.csv', 'r')
constructors_content = datafile.readlines()
datafile.close()

datafile = open('constructor_standings.csv', 'r')
constructor_standings_content = datafile.readlines()
datafile.close()

datafile = open('constructor_results.csv', 'r')
constructor_results_content = datafile.readlines()
datafile.close()

datafile = open('pit_stops.csv', 'r')
pit_stops_content = datafile.readlines()
datafile.close()

datafile = open('qualifying.csv', 'r')
qualifying_content = datafile.readlines()
datafile.close()

datafile = open('races.csv', 'r')
races_content = datafile.readlines()
datafile.close()

datafile = open('results.csv', 'r')
results_content = datafile.readlines()
datafile.close()

datafile = open('seasons.csv', 'r')
seasons_content = datafile.readlines()
datafile.close()

datafile = open('status.csv', 'r')
status_content = datafile.readlines()
datafile.close()

drivers = [] ## driverId	driverRef	number	code	forename	surname	dob	nationality	url
circuits = [] ## circuitId	circuitRef	name	location	country	lat	lng	alt	url
constructors = [] ## constructorId	constructorRef	name	nationality	url
constructors_results = [] ## constructorResultsId	raceId	constructorId	points	status
constructors_standings = [] ## constructorStandingsId	raceId	constructorId	points	position	positionText	wins
driver_standings = [] ## driverStandingsId	raceId	driverId	points	position	positionText	wins
lap_times = [] ## raceId	driverId	lap	position	time	milliseconds
pit_stops = [] ## raceId	driverId	stop	lap	time	duration	milliseconds
qualifying = [] ## qualifyId	raceId	driverId	constructorId	number	position	q1	q2	q3
races = []  ## raceId	year	round	circuitId	name	date	time	url
results = [] ## resultId	raceId	driverId	constructorId	number	grid	position	positionText	positionOrder	points	laps	time	milliseconds	fastestLap	rank	fastestLapTime	fastestLapSpeed	statusId
seasons = [] ## year	url
status = [] ## statusId	status

for row in driver_content[1:]:
    row = row.split(",")
    drivers.append(row)

for row in results_content[1:]:
    row = row.split(",")
    results.append(row)
    
for row in races_content[1:]:
    row = row.split(",")
    races.append(row)

racer_ids = []
winner_ids = []
for race in races:
    for result in results:
        if result[6] != '\N':
            print(result[6])
            if int(result[6]) <= 3 and int(result[1]) == int(race[0]):
                racer_ids.append(result[2])
                if int(result[6]) == 1:
                    winner_ids.append(result[2])

driver_podiums = dict(Counter(racer_ids))
driver_wins = dict(Counter(winner_ids))

driver_name = []
drivers_who_podium = []
for racer_id in driver_wins.keys():
    count = 0
    driver2 = []
    for driver in drivers:
        if int(driver[0]) == int(racer_id):
            driver_to_add = [driver[0], driver[4], driver[5], driver[6], driver[7], driver_podiums[racer_id], driver_wins[racer_id]]
    for result in results:
        if int(racer_id) == int(result[2]):
            count += 1
    driver_to_add.append(count)
    driver_name.append(driver_to_add)

total_length = len(driver_name)

for i in range(total_length):
    podium_percent = round((float(driver_name[i][5]) / float(driver_name[i][7])* 100), 2)
    win_percent = round((float(driver_name[i][6]) / float(driver_name[i][7])* 100), 2)
    driver_name[i].append(podium_percent)
    driver_name[i].append(win_percent)


driver_name.sort(key= lambda x: (x[6], x[9]),reverse=True)
driver_name.insert(0,["raceID", "Forename", "Surname", "DoB", "Nationality", "Podium Count", "Win Count", "Total Race", "Podium Percent", "Win Percent"])

a = np.asarray(driver_name)
np.savetxt("win_and_podium_statistics.csv",a, delimiter=",", fmt="%s")
