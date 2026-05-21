from celery import shared_task


@shared_task
def aggregate_events_task():

    print("TASK EXECUTED")

    return "done"