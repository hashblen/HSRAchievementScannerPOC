from datetime import datetime
import requests
import os.path
import json
from cookie import COOKIE


ACHIEVEMENT_DATA_URL = "https://github.com/Dimbreath/StarRailData/raw/master/ExcelOutput/AchievementData.json"
TEXT_DATA_URL = "https://raw.githubusercontent.com/Dimbreath/StarRailData/master/TextMap/TextMapEN.json"
STARDB_CHIVE_API_URL = "https://stardb.gg/api/users/me/achievements/"

# Returns True if it downloaded, False otherwise.
def download():
    if os.path.exists("processed_data.json"):
        last_modified = os.path.getmtime("processed_data.json")
        URL = "https://api.github.com/repos/Dimbreath/StarRailData/commits/master"
        PARAMS = {'Accept': 'application/vnd.github+json'}
        print("Checking last commit time...")
        commit = requests.get(url=URL, params=PARAMS).json()
        commit_date = datetime.strptime(commit["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        if last_modified > commit_date:
            print("Files are more recent than last commit, not downloading them.")
            return False
    print("Files either don't exist or are older than the last commit.")
    print("Downloading files...")
    with open("dimbreath_data.json", 'wb') as db_data_file:
        db_data_file.write(requests.get(ACHIEVEMENT_DATA_URL).content)
    with open("dimbreath_textmap.json", 'wb') as db_textmap_file:
        db_textmap_file.write(requests.get(TEXT_DATA_URL).content)
    print("Done downloading files.")
    return True


def process():
    with open('dimbreath_data.json', 'r') as db_data_file:
        db_data = json.load(db_data_file)
    with open('dimbreath_textmap.json', 'r', encoding='utf-8') as db_textmap_file:
        db_textmap = json.load(db_textmap_file)

    data = {}
    for achievement in db_data.values():
        a_id = achievement["AchievementID"]
        text_hash = achievement["AchievementTitle"]["Hash"]
        title = db_textmap[str(text_hash)]
        print("Found achievement:", a_id, "\twith text hash", text_hash, "\ttitle:", title)
        data[title] = a_id

    with open('processed_data.json', 'w', encoding='utf-8') as proc_data_file:
        json.dump(data, proc_data_file, indent=4, ensure_ascii=False)

def check_chive(cid: int):
    r = requests.put(STARDB_CHIVE_API_URL + str(cid), cookies={"id": COOKIE})
    if r.status_code == 200:
        print(f"PUT request on id {cid} successful")
    else:
        print(f"PUT request on id {cid} failed with status code: {r.status_code}")
        print(r.text)

def uncheck_chive(cid: int):
    r = requests.delete(STARDB_CHIVE_API_URL + str(cid), cookies={"id": COOKIE})
    if r.status_code == 200:
        print(f"DELETE request on id {cid} successful")
    else:
        print(f"DELETE request on id {cid} failed with status code: {r.status_code}")
        print(r.text)

def save_completed_list(L: list[int]):
    with open('completed_chives_list.json', 'w') as cclf:
        json.dump({"completed_list": L}, cclf)

def open_completed_list() -> list[int]:
    with open('completed_chives_list.json', 'r') as cclf:
        return json.load(cclf)["completed_list"]
