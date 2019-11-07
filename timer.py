import datetime
import time


def round_time_up(date_time, time_delta):
    round_to = time_delta.total_seconds()
    seconds  = (date_time - date_time.min).seconds

    if seconds % round_to == 0:
        rounding = (seconds + round_to / 2) // round_to * round_to
    else:
        rounding = seconds // round_to * round_to

    return date_time + datetime.timedelta(0, rounding - seconds, 
            -date_time.microsecond) + time_delta


class Timer:
    def __init__(self, dt_log, dt_update):
        self.dt_log    = datetime.timedelta(seconds=dt_log)
        self.dt_update = datetime.timedelta(seconds=dt_update)

        # Define first (rounded) time to log
        now = self.now()
        self.next_log    = round_time_up(now, self.dt_log)
        self.next_update = round_time_up(now, self.dt_update)


    def now(self):
        return datetime.datetime.utcnow() 


    def do_log(self):
        if self.now() >= self.next_log:
            self.next_log += self.dt_log
            return True
        else:
            return False


    def do_update(self):
        if self.now() >= self.next_update:
            self.next_update += self.dt_update
            return True
        else:
            return False




if __name__ == '__main__':

    timer = Timer(dt_log=30, dt_update=5)

    while True:
        print(datetime.datetime.utcnow().isoformat())
        if timer.do_log():
            print('Logging!, next={}'.format(timer.next_log.isoformat()))
        if timer.do_update():
            print('Update!, next={}'.format(timer.next_update.isoformat()))

        time.sleep(0.5)
