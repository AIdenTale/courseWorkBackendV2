import psycopg2
from typing import Tuple, Any

from authService.models.api import User, UserLoginRequest
from authService.models.exceptions import EmailAlreadyRegistered

DEFAULT_USER_ROLE = "user"
conn = psycopg2.connect("dbname=auth user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432")

def make_sql_request(query, args):
    cur = conn.cursor()
    cur.execute(query, args)

    records = cur.fetchall()
    cur.close()
    conn.commit()

    return records

def add_new_user(user: User) -> Tuple[int, str]:
        try:
            records = make_sql_request("INSERT INTO public.users (name, surname, email, password, role) VALUES (%s, %s, %s, %s, %s) RETURNING id, role",
                        (user.name, user.surname, user.email, user.password, DEFAULT_USER_ROLE))
        except psycopg2.errors.UniqueViolation:
            raise EmailAlreadyRegistered(user.email)

        return records[0][0], records[0][1]

def get_user_by_login_and_password(user: UserLoginRequest) -> Tuple[int, str] | None:
        records = make_sql_request("SELECT users.id, users.role FROM public.users WHERE email = %s AND password = %s", (user.email,user.password,))
        if len(records) == 0:
            return None
        return records[0][0], records[0][1]



def get_user_by_id(userID) -> tuple[Any, ...] | None:
        records =  make_sql_request("SELECT users.email, users.name, users.surname, users.role FROM public.users WHERE id = %s", (userID,))
        if len(records) == 0:
            return None
        return records[0]
