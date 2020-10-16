#!/usr/bin/env python3

from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="takakura.yusuke@gmail.com",
            first_name="Iosif",
            last_name="Takakura",
            password="password",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser takakura.yusuke@gmail.com")
    init()
    print("Superuser created")
