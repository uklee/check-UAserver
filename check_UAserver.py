# should install requests, win10toast via pip
import requests
import time
from win10toast import ToastNotifier


CHECK_PERIOD = 300  # unit: sec
RELIABLE_URL = "https://1.1.1.1/"
URL_TO_CHECK = ["https://student.kaist.ac.kr/web/main",
                "https://student.kaist.ac.kr/web/api/banners",
                "https://student.kaist.ac.kr/web/api/boards"
                ]


def check(URL): # False may caused by either Server problem or internet connection problem
    try:
        response = requests.get(URL)
        if (response.status_code == 200):
            return True
        
        else:
            raise Exception

    except:
        return False


def check_internet_connection():
    # return True #fortest
    return check(RELIABLE_URL)
    





toaster = ToastNotifier()

while (True):
        server_status = True


        
        for URL in URL_TO_CHECK:
            if (not check(URL)):
                server_status = False




        if (server_status):                     # Server Fine
            print("Server fine.", time.strftime('%c', time.localtime(time.time()))) # Not will be shown in final program. (hidden shell)
        
        else:
            if (check_internet_connection()):   # Server in TROUBLE
                print("Please check the server!!", time.strftime('%c', time.localtime(time.time())))
                toaster.show_toast(title    = "UA SERVER WARNING",
                                   msg      = "Cannot retrieve request from server properly. Please Check\n" + time.strftime('%c', time.localtime(time.time())),
                                   icon_path="UA.ico",
                                   duration = CHECK_PERIOD
                                   )

                

            else:                               # Internet Problem
                print("Internet Connection Problem..", time.strftime('%c', time.localtime(time.time())))

                """
                Or you may use below, if you want to alert your connection problem
                toaster.show_toast(title    = "INTERNAL WARNING",
                                   msg      = "Found internet connection problem.. Please Check\n" + time.strftime('%c', time.localtime(time.time())),
                                   icon_path="UA.ico",
                                   duration = CHECK_PERIOD
                                   )
                """




        time.sleep(CHECK_PERIOD)

    
