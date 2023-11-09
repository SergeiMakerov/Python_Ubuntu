import string
import subprocess


def execute_command(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        if text in out:
            lst = out.split('\n')
            if text in lst:
                print('SUCCES')
                print(text.translate(str.maketrans('', '', string.punctuation)))
                return True
            else:
                print('FAIL')
                return False
    else:
        print('FAIL Result code != 0')
        return False


execute_command('cat /etc/os-release', 'VERSION_CODENAME=jammy')