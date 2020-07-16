from multiprocessing import Process
from time import sleep


def f(name):
    sleep(10)
    return name


if __name__ == '__main__':
    print('main line')
    p = Process(target=f, args=('bob',))
    p.start()

    while True:
        print("hello")
        sleep(1)

