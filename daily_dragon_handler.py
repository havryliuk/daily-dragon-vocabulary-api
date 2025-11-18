from mangum import Mangum

from daily_dragon.daily_dragon_app import app

mangum_handler = Mangum(app)


def daily_dragon_handler(event, context):
    return mangum_handler(event, context)
