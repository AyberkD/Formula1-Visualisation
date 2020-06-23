#1023	2019	14	14	Italian Grand Prix	08/09/2019	13:10:00	https://en.wikipedia.org/wiki/2019_Italian_Grand_Prix

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

drivers = []  ## driverId	driverRef	number	code	forename	surname	dob	nationality	url
circuits = []  ## circuitId	circuitRef	name	location	country	lat	lng	alt	url
constructors = []  ## constructorId	constructorRef	name	nationality	url
constructors_results = []  ## constructorResultsId	raceId	constructorId	points	status
constructors_standings = []  ## constructorStandingsId	raceId	constructorId	points	position	positionText	wins
driver_standings = []  ## driverStandingsId	raceId	driverId	points	position	positionText	wins
lap_times = []  ## raceId	driverId	lap	position	time	milliseconds
pit_stops = []  ## raceId	driverId	stop	lap	time	duration	milliseconds
qualifying = []  ## qualifyId	raceId	driverId	constructorId	number	position	q1	q2	q3
races = []  ## raceId	year	round	circuitId	name	date	time	url
results = []  ## resultId	raceId	driverId	constructorId	number	grid	position	positionText	positionOrder	points	laps	time	milliseconds	fastestLap	rank	fastestLapTime	fastestLapSpeed	statusId
seasons = []  ## year	url
status = []  ## statusId	status

for row in driver_content[1:]:
    row = row.split(",")
    drivers.append(row)

for row in lap_times_content[1:]:
    row = row.split(",")
    lap_times.append(row)

for row in results_content[1:]:
    row = row.split(",")
    results.append(row)

for row in races_content[1:]:
    row = row.split(",")
    races.append(row)

for row in qualifying_content[1:]:
    row = row.split(",")
    qualifying.append(row)

driver_laps = dict()
pit_times_in_years = dict()


for lap in lap_times:
    monza_driver_id = int(lap[1])
    monza_driver_lapno = int(lap[2])
    monza_driver_laptime = lap[4] ### Time in MM:SS:ss format
    if float(lap[0]) == 1023:
        if driver_laps.keys().__contains__(monza_driver_id):
            driver_laps[monza_driver_id].append([monza_driver_lapno,monza_driver_laptime])
        else:
            driver_laps.update({monza_driver_id:[[monza_driver_lapno,monza_driver_laptime]]})

data_out = []

for driver in driver_laps.keys():
    driver_id = driver
    year = 2019
    track_name = 'Italian Grand Prix'
    driver_name = ''
    for x in drivers:
        if int(x[0]) == driver:
            forename = x[4][1:-1]
            surname = x[5][1:-1]
            driver_name = forename + ' '+ surname
            continue
    for laps in driver_laps[driver]:
        #print(laps)
        lapNo = laps[0]
        lapTime = laps[1]
        data_out.append([driver_id,driver_name,14,track_name,year,lapNo,lapTime])

data_out.sort(key= lambda x: (x[0],x[5]),reverse=False)
data_out.insert(0,["driverID", "driverName", "TrackID", "Track Name","Year", "Lap No", "Lap Time"])

a = np.asarray(data_out)
np.savetxt("monza_2020_statistics.csv",a, delimiter=",", fmt="%s")
