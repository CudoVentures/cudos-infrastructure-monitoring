import datetime

from schedule import every, repeat, run_pending
import time

import checks
import settings
import emit

err_free_iterations = 0
reminders_sent = 0


@repeat(every(settings.SCHEDULE_TIME).minutes)
def job():
    global err_free_iterations
    errors = checks.check_sync()
    if errors and not settings.silent_mode():
        emit.slack(errors)
        err_free_iterations = 0
        settings.silent_mode("ON")
        checks.recorded_errors_timestamp = datetime.datetime.now().date()
        checks.recorded_errors = errors[0]
    elif not errors:
        err_free_iterations += 1


@repeat(every(settings.REMINDER).hours)
def reminder():
    global reminders_sent
    if settings.silent_mode():
        if reminders_sent < settings.REMINDER:
            emit.slack(["Status - REMIND"])
        elif reminders_sent < settings.REMINDER * 2:
            emit.slack(["Status - REMIND with TIMESTAMP"])
        else:
            emit.slack(["Status - REMIND with ERROR"])
        reminders_sent += 1


if __name__ == '__main__':
    emit.slack(["Start monitoring"])
    while True:
        run_pending()
        time.sleep(1)
        if err_free_iterations == settings.SELF_CHECK_INTERVAL:
            if settings.silent_mode():
                settings.silent_mode("OFF")
                checks.recorded_errors_timestamp = ""
                checks.recorded_errors = ""
                reminders_sent = 0
            emit.slack(["Status - OK"])
            err_free_iterations = 0
