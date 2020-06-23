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

for row in pit_stops_content[1:]:
    row = row.split(",")
    pit_stops.append(row)

for row in results_content[1:]:
    row = row.split(",")
    results.append(row)

for row in races_content[1:]:
    row = row.split(",")
    races.append(row)

for row in circuit_content[1:]:
    row = row.split(",")
    circuits.append(row)

race_id_in_years = dict()
pit_times_in_years = dict()
winner_ids = []
for race in races:
    year = race[1]
    id = race[0]
    if race_id_in_years.keys().__contains__(year):
        race_id_in_years[year].append(id)
    else:
        race_id_in_years.update({year:[id]})

pit_count = dict()
for pit in pit_stops:
    if pit_count.__contains__(pit[0]):
        dur = round((float(pit[6]) / 1000), 3)
        pit_count[pit[0]].append(dur)
    else:
        dur = round((float(pit[6]) / 1000), 3)
        pit_count.update({pit[0]:[dur]})

data_out = []
for year in race_id_in_years.keys():
    #print("Year: " ,year)
    for race in race_id_in_years[year]:
        track = ""
        trackName = ""
        for pit in pit_count.keys():
            if pit == race:  ## raceID
                total = sum(pit_count[pit])
                avgDuration = round(total / len(pit_count[pit]),3)
                count = len(pit_count[pit])
                for x in races:
                    if race == x[0]:
                        track = x[3]
                for x in circuits:
                    if x[0] == track:
                        trackName = x[2]
                data_out.append([race,year,track,trackName,avgDuration,count])



data_out.sort(key= lambda x: (x[3]),reverse=True)
data_out.insert(0,["raceID", "Year", "Track ID","Track Name",  "Avg. Duration", "Pit Count"])

a = np.asarray(data_out)
np.savetxt("pitstop_statistics.csv",a, delimiter=",", fmt="%s")

### AVG Pit Time Per Race ### Pit count per race ###

