from typing import Sequence

import requests
from sqlalchemy import Select, delete, select
from sqlalchemy.dialects import sqlite

from orienter.databasor.schemas import UserSchema
from . import models
from .session import Session
from ..configurator import configuration


def exec_select(query: Select) -> Sequence:
    response = requests.post(configuration.WEB_APP_URL, json={
        'query': str(query.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))})
    if 200 <= response.status_code < 300:
        return response.json()
    raise RuntimeError(f"pehapezor.php returned a {response.status_code} status code. Content: {response.text}")


def exec_query(query) -> bool:
    response = requests.post(configuration.WEB_APP_URL, json={
        'query': str(query.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))})
    if 200 <= response.status_code < 300:
        return response.json()['success']
    raise RuntimeError(f"pehapezor.php returned a {response.status_code} status code. Content: {response.text}")


if __name__ == "__main__":
    with Session.begin() as session:
        q = select(models.User)
        result = exec_select(q)
        user_schema = UserSchema()
        for user_dict in result:
            user = user_schema.load(user_dict, session=session)
            print(user.first_name, user.last_name)

        q = delete(models.User).where(models.User.user_id == 170)
        success = exec_query(q)
        print('success', success)
