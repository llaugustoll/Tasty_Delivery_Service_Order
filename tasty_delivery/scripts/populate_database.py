
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from adapter.database.db import get_db


def populate():
    try:
        session = next(get_db())

        session.execute(
            text(
                f'''
                INSERT INTO orders (id, total, discount, status, is_active, is_deleted, created_at, updated_at)
                VALUES 
                    (1, '25', '0', 'RECEBIDO', true, false, '{datetime.utcnow()}', null'),
                    (2, '50', '0', 'RECEBIDO', true, false, '{datetime.utcnow()}', null'),
                    (3, '30', '0', 'PRONTO', ' true, false, '{datetime.utcnow()}', null'),
                    (4, '40', '0', 'PRONTO', true, false, '{datetime.utcnow()}', null')
                '''
            )
        )
        session.commit()

        session.close()

    except IntegrityError:
        pass
