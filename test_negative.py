import yaml
from checkers import checkout_negative


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    # Извлечение файлов из архива
    def test_step1(self, make_bad_arx):
        assert checkout_negative("cd {}; 7z e bad_arx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                                 "ERRORS"), "test1 FAIL"

    # Целостность архива
    def test_step2(self):
        assert checkout_negative("cd {}; 7z t bad_arx.7z".format(data["folder_out"]), "ERRORS"), "test2 FAIL"