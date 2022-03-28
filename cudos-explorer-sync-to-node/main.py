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
    elif not errors:
        err_free_iterations += 1


@repeat(every(settings.REMINDER).hours)
def reminder():
    global reminders_sent
    if settings.silent_mode():
        if reminders_sent < settings.REMINDER:
            emit.slack(["Status - REMIND"])
        else:
            emit.slack(list(checks.recorded_errors.values()))
            reminders_sent = 0
        reminders_sent += 1
    else:
        emit.slack(["Status - OK"])


if __name__ == '__main__':
    emit.slack(["Start monitoring"])
    while True:
        run_pending()
        time.sleep(1)
        if err_free_iterations == settings.SELF_CHECK_INTERVAL:
            if settings.silent_mode():
                settings.silent_mode("OFF")
                checks.recorded_errors.clear()
                reminders_sent = 0
            err_free_iterations = 0
