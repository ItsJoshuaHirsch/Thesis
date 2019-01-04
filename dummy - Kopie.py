import json
import random
import uuid
import calendar
import pprint
import numpy as np
import matplotlib.pyplot as plt
import names


from datetime import datetime, timedelta, timezone


number_Missions = 10000


def main():
    missions = []
    text = ""
    f = open("missions" + str(number_Missions//1000) + "k.txt", "w")
    for i in range(number_Missions):
        # text += toJson(randomMission()) + "\n"
        f.write(toJson(randomMission()) + "\n")
        # missions.append(randomMission())


def randomMission():
    uuid = randomUUID()
    devicetype = getDeviceType()
    gender = getSex()
    date = datetimeToUTC(randomDate()) * 1000
    mission = {
        "missionUuid": uuid,
        "markers": {
            "MISSION_UUID": uuid,
            "DEVICE_DIM_SERIAL": "B" + str(random.randint(0, 100001856997501) + 100000000000000),
            "DEVICE_TYPE": devicetype,
            "PATIENT_SEX": gender.upper(),
            "PATIENT_FIRST_NAME": names.get_first_name(gender=gender) if gender != "unknown" else names.get_first_name(),
            # "PATIENT_SURNAME": names.get_last_name(),
            "PATIENT_AGE": getAge(),
            "DEVICE_VERSION": getVersion(devicetype),
            "MISSION_START_DATE": {
                "ts_utc": date,
                "timezone": "GMT+00:00",
                "ts_local": date,
                "daytime": 49081000
            },

        }
    }
    return mission


def getDeviceType():
    number = np.random.choice(np.arange(1, 6), p=[0.15, 0.1, 0.04, 0.06, 0.65])
    if number == 1:
        return "CORPULS1"
    elif number == 2:
        return "CORPULS_CPR"
    elif number == 3:
        return "CORPULS_AED"
    elif number == 4:
        return "CORPULS_WEB_LIVE"
    else:
        return "CORPULS3"


def getVersion(devicetype):
    if devicetype == "CORPULS1":
        return "REL-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b1_C1_BP"
    elif devicetype == "CORPULSCPR":
        return "REL-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b1_CCPR_BP"
    elif devicetype == "CORPULSAED":
        return "REL-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b1_CAED_BP"
    elif devicetype == "CORPULSWEB":
        return "REL-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b1_CWEB_BP"
    else:
        return "REL-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b1_C3_BP"


def getSex():
    number = np.random.choice(np.arange(1, 4), p=[0.15, 0.25, 0.6])
    if number == 1:
        return "female"
    elif number == 2:
        return "male"
    else:
        return "unknown"


def randomAgeSet():
    mu, sigma = 46, 30  # mean and standard deviation
    ageSet = np.random.normal(mu, sigma, number_Missions)
    ageList = []
    for age in ageSet:
        age = int(age)
        if age < 2 or age > 102:
            age = random.randint(34, 58)
            # age = abs(age - 4)
        ageList.append(age)
    return ageList


ages = randomAgeSet()


def getAge():
    random_index = random.randint(0, len(ages)-1)
    age = ages[random_index]
    ages.pop(random_index)
    return age


def printAges(s):
    mu, sigma = 46, 30
    count, bins, ignored = plt.hist(s, 30, normed=True)
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
             np.exp(- (bins - mu)**2 / (2 * sigma**2)), linewidth=2, color='r')
    plt.show()


def plotData(d):
    n, bins, patches = plt.hist(x=d, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('My Very Own Histogram')
    plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(top=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

    plt.show()


# printAges(ages)

# ages = randomAgeSet()
# print(ages)


def randomUUID():
    return str(uuid.uuid4())


def randomDate():
    step = timedelta(seconds=1)
    start = datetime(2013, 1, 1, tzinfo=timezone.utc)
    end = datetime.now(timezone.utc)
    random_date = start + random.randrange((end - start) // step + 1) * step
    return random_date


def datetimeToUTC(dt):
    return calendar.timegm(dt.utctimetuple())


def toJson(mission):
    return json.dumps(mission)


def printMission(mission):
    print(mission)


def getRandomMission():
    printMission(toJson(randomMission()))


main()
