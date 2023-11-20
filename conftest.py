import random
import string
import pytest
from checkers import ssh_checkout, ssh_get
import yaml
from datetime import datetime
import psutil
from files import upload_files


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"],
                                                      data["folder_ext2"]),
                        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]),
                        ""):
            list_off_files.append(filename)

    return list_off_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "rm -rf {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"],
                                                       data["folder_ext2"]),
                        "")


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
                 "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "2222", "truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]),
                 "")
    # yield "bad_arx"
    # checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "2222", "/home/user/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)


@pytest.fixture(autouse=True, scope="module")
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True, scope="module")
def safe_log():
    with open("journalctl.txt", "w") as f:
        f.write(ssh_get("0.0.0.0", "user2", "2222", "journalctl --since '2023-11-20 12:00:00'"))


@pytest.fixture(autouse=True, scope="module")
def stat():

    current_date = datetime.now()
    proc = psutil.getloadavg()
    inf = str("Count = {} Size = {}".format(data["count"], data["bs"]))

    with open("stat.txt", "a", encoding='utf8') as file:
        file.write(str(f'{current_date} {inf}  {proc} \n'))