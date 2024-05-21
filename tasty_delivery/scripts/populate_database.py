
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
                INSERT INTO users (id, total, discount, status, is_active, is_deleted, created_at, updated_at)
                VALUES 
                    ('{order_1_id}', '25', '0', 'RECEBIDO', true, false, '{datetime.utcnow()}', null'),
                    ('{order_2_id}', '50', '0', 'RECEBIDO', true, false, '{datetime.utcnow()}', null'),
                    ('{order_3_id}', '30', '0', 'PRONTO', ' true, false, '{datetime.utcnow()}', null'),
                    ('{order_4_id}', '40', '0', 'PRONTO', true, false, '{datetime.utcnow()}', null')
                '''
            )
        )
        session.commit()

        session.close()

    except IntegrityError:
        pass
