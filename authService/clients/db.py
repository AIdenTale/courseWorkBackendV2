import psycopg2
from typing import  Tuple

from models.api import UserAuthReqModel

from models.exceptions import EmailAlreadyRegistered

DEFAULT_USER_ROLE = "user"

class PostgresClient():
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=auth user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432")

    def add_new_user(self, user: UserAuthReqModel) -> Tuple[int, str]:
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO public.users (name, surname, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                        (user.name, user.surname, user.email, user.password, DEFAULT_USER_ROLE))
        except psycopg2.errors.UniqueViolation:
            raise EmailAlreadyRegistered(user.email)

        cur.execute("SELECT users.id, users.role FROM public.users WHERE email = %s", (user.email,))
        records = cur.fetchall()

        cur.close()
        self.conn.commit()

        return records[0][0], records[0][1]