import threading

# Creating threads


def create_threads(list, function):

    threads = []

    for ip in list:
        # args is a tuple with a single element
        th = threading.Thread(target=function, args=(ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()
