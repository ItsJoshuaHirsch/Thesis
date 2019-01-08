import json
import random
import uuid
import calendar
import pprint
import numpy as np
import matplotlib.pyplot as plt
import names
import os


from multiprocessing import Pool
from datetime import datetime, timedelta, timezone


number_Missions = 100000


def main():
    missions = []
    text = ""

    f = open("missions" + str(number_Missions//1000) + "k.txt", "w")
    # f = open('missions' + str(number_Missions//1000) + 'k.json', 'w')

    for i in range(number_Missions):

        # print(toJson(randomMission()) + ",")
        # text += toJson(randomMission()) + "\n"
        f.write(toJson(randomMission()) + "\n")
    f.close()
    thisFile = "missions" + str(number_Missions//1000) + "k.txt"
    base = os.path.splitext(thisFile)[0]
    os.rename(thisFile, base + ".json")
    # json.dump(missions, f)
    # pprint.pprint(missions)
    # print(missions)


def randomMission():
    uuid = randomUUID()
    devicetype = getDeviceType()
    gender = getSex()
    # firstname, lastname = str(name).split()
    date = datetimeToUTC(randomDate()) * 1000
    mission = {
        "missionUuid": uuid,
        "markers": {
            "MISSION_UUID": uuid,
            "MISSION_ID": getMissionID(date),
            "MISSION_DURATION_MS":  {"$numberLong": str(random.randint(50000, 12000000))},
            "MASTER_DATA_DEVICE_ID": getDeviceID(),
            "DEVICE_DIM_SERIAL": "B" + str(random.randint(0, 100001856997501) + 100000000000000),
            "DEVICE_TYPE": devicetype,
            "PATIENT_SEX": gender.upper(),
            "PATIENT_FIRST_NAME": names.get_first_name(gender=gender) if gender != "unknown" else names.get_first_name(),
            # "PATIENT_FIRST_NAME": firstname,
            # "PATIENT_SURNAME": lastname,
            "PATIENT_AGE": getAge(),
            "PATIENT_ID": getPatientID(),
            "PATIENT_CASE_NUMBER": getPatientID(),
            "TRENDS_HR_MEAN": float(random.randrange(35, 130)),
            "TRENDS_PI_MEAN": float(random.randrange(0, 20)),
            "TRENDS_SPCO_MEAN": float(random.randrange(0, 20)),
            "TRENDS_SPHB_MEAN": float(random.randrange(3, 16)),
            "TRENDS_SPMET_MEAN": float(random.randrange(0, 8)),
            "TRENDS_SPO_2_MEAN": float(random.randrange(80, 100)),
            "NIBP_COUNT": random.randrange(0, 12),
            "DEVICE_VERSION": getVersion(devicetype),
            "MISSION_START_DATE": {
                "ts_utc": date,
                "timezone": "GMT+00:00",
                "ts_local": date,
                "daytime": 49081000
            },
            "CO_2_TREND_AVAILABLE": bool(random.getrandbits(1)) if devicetype != "CORPULS_CPR" else False,
            "SHOCK_AVAILABLE": bool(random.getrandbits(1)) if devicetype != "CORPULS_CPR" else False,
            "CPR_FEEDBACK_AVAILABLE": bool(random.getrandbits(1)) if devicetype != "CORPULS_CPR" else False,
            "DECG_AVAILABLE": bool(random.getrandbits(1)) if devicetype == "CORPULS3" else False,
            "ATTACHMENTS_AVAILABLE": bool(random.getrandbits(1)) if devicetype == "CORPULS3" else False,
            "MISSION_TEST_FLAG": bool(random.getrandbits(1))
        }
    }
    return mission


def getPatientID():
    num = random.randint(0, 3)
    if num % 3 == 0:
        return str(random.randint(10000, 99999))
    else:
        return ""


def getDeviceID():
    num = random.randint(0, 3)
    if num == 0:
        return "VAL" + str(random.randint(0, 22))
    elif num == 1:
        return "VER-" + str(random.randint(0, 22))
    elif num == 2:
        return str(random.randint(10000, 99999))
    else:
        return ""


def getMissionID(date):
    return datetime.fromtimestamp(date / 1e3).strftime("%Y%m%d%H%M%S")


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
        return "C1_" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b1"
    elif devicetype == "CORPULSCPR":
        return "cCPR-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b15"
    elif devicetype == "CORPULSAED":
        return "00C" + "0" + str(random.randint(0, 5))
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


""" def nameSet(gender):
    nameSet = []
    for i in range(number_Missions+1)
        names.append(names.get_full_name(
            gender=gender) if gender != "unknown" else names.get_full_name()),

names = nameSet() """
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
