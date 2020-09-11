import os
import time
import pandas as pd
import threading
from itertools import combinations

# rca_arr = ['Microscope_online.py']
# svc_arr = ['cartservice', 'productcatalogservice']

rca_arr = ['Microscope_online.py', 'MicroRCA_online.py', 'tRCA_online.py']
svc_arr = ['cartservice', 'productcatalogservice', 'currencyservice',
           'checkoutservice', 'recommendationservice', 'paymentservice']
down_time = 180
fault_injection_path = 'kubectl apply -f /root/zik/fault-injection/hipster/'


def combine_svc():
    comb_svc = list(combinations(svc_arr, 2))
    svc_list = []
    for svc in comb_svc:
        svc = svc[0] + '+' + svc[1]
        svc_list.append(svc)
    return svc_list


def anomaly_detection():
    n = 0
    locsut_latency_pd = pd.read_csv('example_stats_history.csv')
    p90_avg = locsut_latency_pd['80%'][-20:].sum() / 20
    p50_avg = locsut_latency_pd['50%'][-20:].sum() / 20

    p90s = locsut_latency_pd['80%'][-3:]
    p50s = locsut_latency_pd['50%'][-3:]

    for p50 in p50s:
        print(p50/p50_avg)
        if (p50/p50_avg > 2):
            n = n + 1
    if n < 2:
        return False
    else:
        return True


def tRCA(rca_types, svc):
    global timer
    timer = threading.Timer(5, tRCA, (rca_types, svc))

    if (anomaly_detection()):
        # os.system('python3 %s --fault %s' % (rca_type, svc))
        for rca in rca_types:
            print('python3 %s --fault %s &' % (rca, svc))
        countdown(down_time)
        timer.start()
    else:
        countdown(down_time)
        timer.start()
        print('    ----    ')


def countdown(t):
    time_left = t
    while time_left > 0:
        print('left: %s s' % time_left)
        time.sleep(2)
        time_left = time_left - 2


if __name__ == '__main__':
    case = 1
    os.system('./headless_locust.sh &')
    print('==== RCA will be started in 3min ... ====')
    if case == 1:
        countdown(down_time)
        for svc in svc_arr:
            print(fault_injection_path + '%s.yaml' % svc)
            timer = threading.Timer(5, tRCA, (rca_arr, svc))
            timer.start()
            time.sleep(60)
            timer.cancel()
            print(fault_injection_path + '%s.yaml' % svc)
        print("==== ends ====")
    elif case == 2:
        svc_list = combine_svc()
        for svcs in svc_list:
            countdown(down_time)
            svc2 = svcs.split('+')
            # create fault injection
            for svc in svc2:
                # os.system('kubectl apply -f /root/zik/fault-injection/hipster/%s.yaml' % svc)
                print(fault_injection_path + '%s.yaml' % svc)
            # interval apply RCA
            timer = threading.Timer(5, tRCA, (rca_arr, svcs))
            timer.start()
            time.sleep(60)
            timer.cancel()
            # delete fault injection
            for svc in svc2:
                # os.system('kubectl delete -f /root/zik/fault-injection/hipster/%s.yaml' % svc)
                print(fault_injection_path + '%s.yaml' % svc)

    print('==== Experiment ends ====')
