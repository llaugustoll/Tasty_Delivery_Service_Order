
from datetime import datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from tasty_delivery.adapter.database.db import get_db


def populate():
    try:
        session = next(get_db())

        order_1_id = uuid4()
        order_2_id = uuid4()
        order_3_id = uuid4()
        order_4_id = uuid4()

        session.execute(
            text(
                f'''
                INSERT INTO users (id, username, name, email, cpf, hashed_password, is_active, is_deleted, created_at, updated_at, scopes)
                VALUES 
                    ('{order_1_id}', 'joao@email.com', 'João', 'joao@email.com', '11122233344', '{get_password_hash('password')}', true, false, '{datetime.utcnow()}', null, '{{admin}}'),
                    ('{order_2_id}', 'victor@email.com', 'Victor', 'victor@email.com', '22233344455', '{get_password_hash('password')}', true, false, '{datetime.utcnow()}', null, '{{admin}}'),
                    ('{order_3_id}', 'tais@email.com', 'Tais', 'tais@email.com', '33344455566', '{get_password_hash('password')}', true, false, '{datetime.utcnow()}', null, '{{admin}}'),
                    ('{order_4_id}', 'augusto@email.com', 'Augusto', 'augusto@email.com', '44455566677', '{get_password_hash('password')}', true, false, '{datetime.utcnow()}', null, '{{admin}}')
                '''
            )
        )
        session.commit()

        session.close()

    except IntegrityError:
        pass
