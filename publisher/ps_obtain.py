import psutil
import time


def cpu_util_value():
    # return {'utilization': psutil.cpu_percent(interval=1)}
    return psutil.cpu_percent(interval=1)


def ram_util_percent():
    # return {'utilization': psutil.virtual_memory().percent}
    return psutil.virtual_memory().percent


def net_util_value():
    first_time_stamp = psutil.net_io_counters(
        pernic=False).bytes_sent + psutil.net_io_counters(pernic=False).bytes_recv
    time.sleep(5)
    second_time_stamp = psutil.net_io_counters(
        pernic=False).bytes_sent + psutil.net_io_counters(pernic=False).bytes_recv
    return second_time_stamp - first_time_stamp
