"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый
тип на кириллице.
"""
import chardet
import subprocess
import platform
import locale


def test_ping(site):

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', site]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    default_encoding = locale.getpreferredencoding()
    print(default_encoding)

    for line in result.stdout:
        line = line.decode(default_encoding).encode(default_encoding)
        print(line.decode(default_encoding))


if __name__ == "__main__":

    site_1 = 'yandex.ru'
    site_2 = 'youtube.com'

    test_ping(site_1)
    test_ping(site_2)


