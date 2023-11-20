import yaml
from checkers import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    # Создание и обноление архива
    def test_step1(self):
        result1 = ssh_checkout("0.0.0.0", "user2", "2222",
                               "cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type_archive"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; ls".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, "test1 FAIL"

    # Извлечение файлов из архива
    def test_step2(self, make_files):
        result1 = ssh_checkout("0.0.0.0", "user2", "2222",
                               "cd {}; 7z e arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; ls".format(data["folder_ext"]), make_files[0])
        assert result1 and result2, "test2 FAIL"

    # Целостность архива
    def test_step3(self):
        assert ssh_checkout("0.0.0.0", "user2", "2222","cd {}; 7z t arx2.7z".format(data["folder_out"]),
                            "Everything is Ok"), "test3 FAIL"

    # Обновление данных
    def test_step4(self):
        assert ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z u {}/arx2.7z".format(data["folder_in"], data["folder_out"]),
                            "Everything is Ok"), "test4 FAIL"

    # Очистить содержимое архива
    def test_step5(self):
        assert ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z d arx2.7z".format(data["folder_out"]),
                            "Everything is Ok"), "test5 FAIL"

    # Вывести список содержимого архива
    def test_step6(self):
        result1 = ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z l arx2.7z".format(data["folder_out"]), "Path = arx2.7z")
        result2 = ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; ls".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, "test6 FAIL"

    # Извлечение архива в указаную директорию
    def test_step7(self):
        result1 = ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; 7z x arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext2"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "2222", "cd {}; ls".format(data["folder_ext2"]), "qwe")
        assert result1 and result2, "test7 FAIL"