from schedule import every, repeat, run_pending
import time

import checks
import settings
import emit

err_free_iterations = 0


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


@repeat(every(settings.REMINDER).minutes)
def reminder():
    if settings.silent_mode():
        emit.slack(["Status - REMIND"])


if __name__ == '__main__':
    while True:
        run_pending()
        time.sleep(1)
        if err_free_iterations == settings.SELF_CHECK_INTERVAL:
            if settings.silent_mode():
                settings.silent_mode("OFF")
            emit.slack(["Status - OK"])
            err_free_iterations = 0
