from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from db import models


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        if not event.from_user.id:
            return await event.answer(text='Нужно установить в настройках username, чтобы пользоваться этим ботом')
        if not models.User.exists(username=event.from_user.username):
            await models.User.update_or_create(user_id=event.from_user.id,
                                               username=event.from_user.username,
                                               answer_count=0
                                               )
        return await handler(event, data)
