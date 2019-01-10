import json
import random
import uuid
import calendar
import pprint
import numpy as np
import names
import os
import time
import sys
import py2exe

from multiprocessing import Pool
from datetime import datetime, timedelta, timezone

numInMio = 1
number_Missions = int(numInMio * 1000000)
number_blocks = int(numInMio * 1600)
block_size = number_Missions//number_blocks  # Block_size should be ~625

# TODO
# txt, 1m Mission, blocksize 1600 = 349sek
# txt to json, 10m = 3455sek
# 30m = 8900sek

# Open, eventually create file to be written into
# f = open("mp_missions" + str(number_Missions//1000000) + "M.txt", "a+")

f = open("mp_missions.txt", "a+")

# Import Lastnames
l = open("sources/last-names.txt", "r")
lastnames = l.read().title().split("\n")
l.close()


def mainP():
    # MultiProcessingTry

    p = Pool()
    for i in range(number_blocks):
        p.apply_async(generateMissionBlock, args=(i,), callback=writeToFile)
    p.close()
    p.join()

    f.close()

    # toJsonFile
    thisFile = "mp_missions.txt"
    base = os.path.splitext(thisFile)[0]
    os.rename(thisFile, base + str(number_Missions//1000) + "k.json")


def generateMissionBlock(i):
    mBlock = ""
    ages = randomAgeSet(block_size)
    for _ in range(block_size):
        mBlock += randomMission(ages)
    return mBlock


def writeToFile(s):
    f.write(s)


def randomMission(ages):
    uuid = randomUUID()
    devicetype = getDeviceType()
    gender = getSex()
    cpr = bool(random.getrandbits(1)) if devicetype != "CORPULS_CPR" else False
    date = datetimeToUTC(randomDate()) * 1000

    # Different MissionTypes depending on devicetype
    if devicetype == "CORPULS3" or devicetype == "CORPULS_WEB_LIVE":
        mission = {
            "missionUuid": uuid,
            "markers": {
                "MISSION_UUID": uuid,
                "MISSION_ID": getMissionID(date),
                "MISSION_DURATION_MS":  {"$numberLong": str(random.randint(50000, 12000000))},
                "MASTER_DATA_DEVICE_ID": getDeviceID(),
                "DEVICE_DIM_SERIAL": "B" + str(random.randint(0, 100001856997501) + 100000000000000),
                "DEVICE_TYPE": devicetype,
                "DEVICE_VERSION": getVersion(devicetype),
                "PATIENT_SEX": gender.upper(),
                "PATIENT_FIRST_NAME": names.get_first_name(gender=gender) if gender != "unknown" else names.get_first_name(),
                "PATIENT_SURNAME": lastnames[random.randint(0, len(lastnames)-1)],
                "PATIENT_AGE": getAge(ages),
                "PATIENT_ID": getPatientID(),
                "PATIENT_CASE_NUMBER": getPatientID(),
                "TRENDS_HR_MEAN": float(random.randrange(35, 130)),
                "TRENDS_PI_MEAN": float(random.randrange(0, 20)),
                "TRENDS_SPCO_MEAN": float(random.randrange(0, 20)),
                "TRENDS_SPHB_MEAN": float(random.randrange(3, 16)),
                "TRENDS_SPMET_MEAN": float(random.randrange(0, 8)),
                "TRENDS_SPO_2_MEAN": float(random.randrange(80, 100)),
                "NIBP_COUNT": random.randrange(0, 12),
                "MISSION_START_DATE": {
                    "ts_utc": date,
                    "timezone": "GMT+00:00",
                    "ts_local": date,
                    "daytime": 49081000
                },
                "CO_2_TREND_AVAILABLE": bool(random.getrandbits(1)),
                "SHOCK_AVAILABLE": bool(random.getrandbits(1)),
                "CPR_FEEDBACK_AVAILABLE": cpr,
                "DECG_AVAILABLE": bool(random.getrandbits(1)),
                "ATTACHMENTS_AVAILABLE": bool(random.getrandbits(1)),
                "MISSION_TEST_FLAG": bool(random.getrandbits(1))
            }
        }
        miss = toJson(mission) + "\n"
        return miss
    elif devicetype == "CORPULS_CPR":
        mission = {
            "missionUuid": uuid,
            "markers": {
                "MISSION_UUID": uuid,
                "MISSION_ID": getMissionID(date),
                "MISSION_DURATION_MS":  {"$numberLong": str(random.randint(50000, 12000000))},
                "MASTER_DATA_DEVICE_ID": getDeviceID(),
                "DEVICE_DIM_SERIAL": "B" + str(random.randint(0, 100001856997501) + 100000000000000),
                "DEVICE_TYPE": devicetype,
                "DEVICE_VERSION": getVersion(devicetype),
                "MISSION_START_DATE": {
                    "ts_utc": date,
                    "timezone": "GMT+00:00",
                    "ts_local": date,
                    "daytime": 49081000
                },
                "MISSION_TEST_FLAG": bool(random.getrandbits(1)),
                "MECHANICAL_REANIMATION_AVAILABLE": bool(random.getrandbits(1)),
                "CPR_COMPRESSIONS_AMOUNT": random.randint(0, 500),
                "CPR_COMPRESSIONS_DEPTH_AVERAGE": random.randrange(3, 7),
                "CPR_COMPRESSIONS_DEPTH_MAXIMUM": random.randrange(5, 9),
                "CPR_COMPRESSIONS_DEPTH_MINIMUM": random.randrange(1, 3),
                "CPR_COMPRESSIONS_DEPTH_STANDARD_DEVIATION": random.randrange(0, 1),
                "CPR_COMPRESSIONS_FORCE_AVERAGE": random.randint(100, 700),
                "CPR_COMPRESSIONS_FORCE_MAXIMUM": random.randint(500, 900),
                "CPR_COMPRESSIONS_FORCE_MINIMUM": random.randint(10, 300),
                "CPR_COMPRESSIONS_FORCE_STANDARD_DEVIATION": random.randint(0, 100),
                "CPR_COMPRESSIONS_GOOD": random.randint(0, 30),
                "CPR_COMPRESSIONS_RATE_STANDARD_DEVIATION": random.randrange(0, 2),
                "CPR_COMPRESSIONS_TOO_DEEP": random.randint(0, 30),
                "CPR_COMPRESSIONS_TOO_FAST": random.randint(0, 30),
                "CPR_COMPRESSIONS_TOO_SHALLOW": random.randint(0, 30),
                "CPR_COMPRESSIONS_TOO_SLOW": random.randint(0, 30)
            }
        }
        miss = toJson(mission) + "\n"
        return miss
    elif devicetype == "CORPULS_AED":
        mission = {
            "missionUuid": uuid,
            "markers": {
                "MISSION_UUID": uuid,
                "MISSION_ID": getMissionID(date),
                "MISSION_DURATION_MS":  {"$numberLong": str(random.randint(50000, 12000000))},
                "MASTER_DATA_DEVICE_ID": getDeviceID(),
                "DEVICE_DIM_SERIAL": "B" + str(random.randint(0, 100001856997501) + 100000000000000),
                "DEVICE_TYPE": devicetype,
                "TRENDS_HR_MEAN": float(random.randrange(35, 130)),
                # if devicetype == "CORPULS3" else None,
                "AED_BOOT_MODE": getAEDBootMode(),
                "DEVICE_VERSION": getVersion(devicetype),
                "MISSION_START_DATE": {
                    "ts_utc": date,
                    "timezone": "GMT+00:00",
                    "ts_local": date,
                    "daytime": 49081000
                },
                "SHOCK_AVAILABLE": bool(random.getrandbits(1)),
                "CPR_FEEDBACK_AVAILABLE": cpr
            }
        }
        miss = toJson(mission) + "\n"
        return miss
    else:  # CORPULS1
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
                "PATIENT_SURNAME": lastnames[random.randint(0, len(lastnames)-1)],
                "PATIENT_AGE": getAge(ages),
                "PATIENT_ID": getPatientID(),
                "PATIENT_CASE_NUMBER": getPatientID(),
                "TRENDS_HR_MEAN": float(random.randrange(35, 130)),
                "TRENDS_PI_MEAN": float(random.randrange(0, 20)),
                "TRENDS_SPCO_MEAN": float(random.randrange(0, 20)),
                "TRENDS_SPHB_MEAN": float(random.randrange(3, 16)),
                "TRENDS_SPMET_MEAN": float(random.randrange(0, 8)),
                "TRENDS_SPO_2_MEAN": float(random.randrange(80, 100)),
                # if devicetype == "CORPULS3" else None,
                "NIBP_COUNT": random.randrange(0, 12),
                "DEVICE_VERSION": getVersion(devicetype),
                "MISSION_START_DATE": {
                    "ts_utc": date,
                    "timezone": "GMT+00:00",
                    "ts_local": date,
                    "daytime": 49081000
                },
                "CO_2_TREND_AVAILABLE": bool(random.getrandbits(1)),
                "SHOCK_AVAILABLE": bool(random.getrandbits(1)),
                "CPR_FEEDBACK_AVAILABLE": cpr,
                "ATTACHMENTS_AVAILABLE": bool(random.getrandbits(1)),
                "MISSION_TEST_FLAG": bool(random.getrandbits(1))
            }
        }
        miss = toJson(mission) + "\n"
        return miss

    # Standard Missiontype
    """ mission = {
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
            "PATIENT_SURNAME": lastnames[random.randint(0, len(lastnames)-1)],
            "PATIENT_AGE": getAge(ages),
            "PATIENT_ID": getPatientID(),
            "PATIENT_CASE_NUMBER": getPatientID(),
            "TRENDS_HR_MEAN": float(random.randrange(35, 130)),
            "TRENDS_PI_MEAN": float(random.randrange(0, 20)),
            "TRENDS_SPCO_MEAN": float(random.randrange(0, 20)),
            "TRENDS_SPHB_MEAN": float(random.randrange(3, 16)),
            "TRENDS_SPMET_MEAN": float(random.randrange(0, 8)),
            "TRENDS_SPO_2_MEAN": float(random.randrange(80, 100)),
            # if devicetype == "CORPULS3" else None,
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
            "CPR_FEEDBACK_AVAILABLE": cpr,

            "DECG_AVAILABLE": bool(random.getrandbits(1)) if devicetype == "CORPULS3" else False,
            "ATTACHMENTS_AVAILABLE": bool(random.getrandbits(1)) if devicetype == "CORPULS3" else False,
            "MISSION_TEST_FLAG": bool(random.getrandbits(1)),
            "MECHANICAL_REANIMATION_AVAILABLE": bool(random.getrandbits(1)) if devicetype == "CORPULS_CPR" else False,
        } """


def getPatientID():
    num = random.randint(1, 2)
    if num % 2 == 0:
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


def getAEDBootMode():
    num = random.randint(0, 4)
    if num == 0:
        return "AED"
    elif num == 1:
        return "Info"
    elif num == 2:
        return "Unbekannt"
    elif num == 3:
        return "kleiner Selbsttest"
    else:
        return "großer Selbsttest"


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
    elif devicetype == "CORPULS_CPR":
        return "cCPR-" + str(random.randint(0, 3)) + "." + str(random.randint(0, 5)) + "." + str(random.randint(0, 7)) + "_b15"
    elif devicetype == "CORPULS_AED":
        return "00C" + "0" + str(random.randint(0, 5))
    elif devicetype == "CORPULS_WEB_LIVE":
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


def randomAgeSet(numberAges):
    mu, sigma = 46, 30  # mean and standard deviation
    ageSet = np.random.normal(mu, sigma, numberAges)
    ageList = []
    for age in ageSet:
        age = int(age)
        if age < 2 or age > 102:
            age = random.randint(34, 58)
        ageList.append(age)
    return ageList


""" def nameSet(gender):
    nameSet = []
    for i in range(number_Missions+1)
        names.append(names.get_full_name(
            gender=gender) if gender != "unknown" else names.get_full_name()), """


def getAge(ages):
    age = ages[0]
    ages.pop(0)
    return age


def getAgeOLD(ages):
    random_index = random.randint(0, len(ages)-1)
    age = ages[random_index]
    ages.pop(random_index)
    return age


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
    printMission(toJson(randomMission(1)))


if __name__ == "__main__":
    number_Missions = int(sys.argv[1])
    # number_Missions = 10000
    if number_Missions < 10000:
        number_blocks = 4
    else:
        number_blocks = int((number_Missions//10000) * 16)
    block_size = number_Missions//number_blocks

    mainP()
