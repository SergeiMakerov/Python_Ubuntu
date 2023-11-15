import random
import string
import pytest
from checkers import checkout
import yaml
from datetime import datetime
import psutil


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return checkout(
        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]),
        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename,
                                                                                           data["bs"]), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return checkout(
        "rm -rf {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]),
        "")


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")
    # yield "bad_arx"
    # checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True)
def stat():
    with open('config.yaml') as f:
        data = yaml.safe_load(f)

    current_date = datetime.now()
    proc = psutil.getloadavg()
    inf = str("Count = {} Size = {}".format(data["count"], data["bs"]))

    with open("stat.txt", "a", encoding='utf8') as file:
        file.write(str(f'{current_date} {inf}  {proc} \n'))