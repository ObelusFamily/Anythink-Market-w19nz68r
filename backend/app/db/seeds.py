import sys

sys.path.append(".")
import time
import asyncio
from app.db.repositories.users import UsersRepository
from app.db.repositories.items import ItemsRepository
from app.db.repositories.comments import CommentsRepository
from app.core.settings.test import TestAppSettings
import asyncpg

settings = TestAppSettings()
# SQLAlchemy >= 1.4 deprecated the use of `postgres://` in favor of `postgresql://`
# for the database connection url
database_url = settings.database_url.replace("postgres://", "postgresql://")

seed_completed = False


async def seed():
    global seed_completed
    conn = await asyncpg.connect(database_url)

    items_repo = ItemsRepository(conn)
    users_repo = UsersRepository(conn)
    comments_repo = CommentsRepository(conn)

    for i in range(0, 100):
        user = await users_repo.create_user(
            **{
                "username": f"user-{i}",
                "password": f"password-{i}",
                "email": f"{i}@anythink-market.com",
            }
        )
        str_i = str(i)
        item = await items_repo.create_item(
            **{"slug": str_i, "title": str_i, "description": str_i, "seller": user}
        )
        await comments_repo.create_comment_for_item(
            **{"body": str_i, "item": item, "user": user}
        )
    seed_completed = True


asyncio.run(seed())

while not seed_completed:
    time.sleep(1)
