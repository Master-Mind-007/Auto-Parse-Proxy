import requests
import threading
import os 
import time
import platform

def test(type):
    if type in ['http', 'https']:
        with open("https.txt", "r") as f:
            data = f.read().split("\n")
    else:
        with open("{}.txt".format(type), "r") as f:
            data = f.read().split("\n")
    print('> {} {} proxies will be checked'.format(len(data), type))

    if os.path.exists('{}_checked.txt'.format(type)):
        try:
            if platform.system() == 'Windows':
                os.system('del {}_checked.txt'.format(type))
                os.system(f'fsutil file createnew {type}_checked.txt 0 ')
            else:  # Assuming it's Linux
                os.system('rm {}_checked.txt'.format(type))
                os.system(f'touch {type}_checked.txt')
        except:
            pass
    
    def process(i):
        try:
            requests.get("https://icanhazip.com/", proxies={type: f"{type}://{i}"}, timeout=30,)
        except:
            pass
        else:
            with open("{}_checked.txt".format(type), "a+") as f:
                f.write(i + "\n")

    for i in data:
        while threading.active_count() > 7000:
            time.sleep(3)
        threading.Thread(target=process, args=(i,)).start()

    while threading.active_count() > 1:
        time.sleep(1)
    
if __name__ == '__main__':
    test('socks4')
    test('socks5')
    test('http')
    test('https')
