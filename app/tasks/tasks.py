import asyncio
from time import sleep

from app.database import async_session_maker_null_pool
from app.tasks.celery_app import celery_instance
from app.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")


async def get_bookings_with_today_checkin_helper():
    print("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
