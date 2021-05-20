# should install requests, win10toast via pip
import requests
import time
import os.path
import sys
from win10toast import ToastNotifier


CHECK_PERIOD = 300  # unit: sec
# CHECK_PERIOD = 10  # fortest
RELIABLE_URL = "https://1.1.1.1/"
URL_TO_CHECK = ["https://student.kaist.ac.kr/web/main",
                "https://student.kaist.ac.kr/web/api/banners",
                "https://student.kaist.ac.kr/web/api/boards"
                ]





def check(URL): # False may caused by either Server problem or internet connection problem
    # return False # fortest
    try:
        response = requests.get(URL)
        if (response.status_code == 200):
            return True
        
        else:
            raise Exception

    except:
        return False


def check_internet_connection():
    # return True # fortest
    return check(RELIABLE_URL)
    

def resource_path(relative_path):   # to find icon file
    """ Get absolute path to resource, works for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)





toaster = ToastNotifier()
toaster.show_toast(title    = "check_UA SERVER",
                   msg      = "Server check start successfully\n" + time.strftime('%c', time.localtime(time.time())),
                   icon_path= resource_path("UA.ico"),
                   duration = CHECK_PERIOD,
                   threaded = True
                   )





while (True):
    server_status = True
    unavailable_URL = []

    
    for URL in URL_TO_CHECK:
        if (not check(URL)):
            server_status = False
            unavailable_URL.append(URL)





    if (server_status):                     # Server Fine
        print("Server fine.", time.strftime('%c', time.localtime(time.time()))) # Not will be shown in final program. (hidden shell)

    
    else:
        if (check_internet_connection()):   # Server in TROUBLE
            print("Please check the server!!", time.strftime('%c', time.localtime(time.time())))
            toaster.show_toast(title    = "UA SERVER WARNING",
                               msg      = "Cannot retrieve request from server properly. Please Check\n" + str(unavailable_URL) + '\n' + time.strftime('%c', time.localtime(time.time())),
                               icon_path= resource_path("UA.ico"),
                               duration = CHECK_PERIOD,
                               threaded = True
                               )

            
        else:                               # Internet Problem
            print("Internet Connection Problem..", time.strftime('%c', time.localtime(time.time())))

            """
            Or you may use below, if you want to alert your connection problem
            toaster.show_toast(title    = "INTERNAL WARNING",
                               msg      = "Found internet connection problem.. Please Check\n" + time.strftime('%c', time.localtime(time.time())),
                               icon_path="UA.ico",
                               duration = CHECK_PERIOD,
                               threaded = True
                               )
            """





    time.sleep(CHECK_PERIOD)
