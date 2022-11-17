
from asyncio.log import logger
import email
from email import message

from celery import shared_task

from celery.utils.log import get_task_logger

from django.conf import settings

from django.core.mail import send_mail

from Library_mngmnt.celery import app

from .models import IssueBook

import datetime

from datetime import date, timedelta

logger = get_task_logger(__name__)


@app.task(name= 'send_reminder')
def send_reminder():
    try:
        
        ib_objects = IssueBook.objects.filter(status="issued")
        # print(ib_objects)
      
        today = date.today()

        for is_date in ib_objects:

            dates = is_date.issue_date

            exceed_days = dates + datetime.timedelta(days = 7)

            # print(exceed_days)

            if today > exceed_days:

                mail = is_date.user.email
                title = is_date.book.title
                author = is_date.book.author


                send_mail(
                    subject = 'Book Return Date Exceeds.!!!',
                    message = 'Reminder: Your Book' '\t' f"{title} by {author}, return date exceeds 7 days, \n \n Kindly return the same ASAP..! \n \n Happy Reading...",
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [mail],
                    fail_silently = False,
                )

                print("Reminder mail has been sent")
              

            else:
                print('Not Exceeded')
                pass

    except Exception as e:
        print(e)


@shared_task
def send_issue_mail(email, message):
    logger.info("inside send mail task")

    send_mail(
        subject = 'Book Issued Successfully',
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [email],
        fail_silently = False,
    ) 

    print("Book issued mail has been sent")
    return "Done"


@shared_task
def send_return_mail(email, message):
    logger.info("inside send mail task")

    send_mail(
        subject = 'Book Returned Successfully',
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [email],
        fail_silently = False,
    )

    print("Book return mail has been sent")
    return "Done"
