import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from . import USER_PARAMS

def getDBConnection(userParams):
    """
    Attempts to connect to the database university.
    If no such database exists, creates a database called university,
    and populates it with the sample data. if the database exists, but
    is not populated, populates it with data.
    """

    # connect to default db, drop university db if it exists, create fresh db
    conn = psycopg2.connect(**userParams, dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier("university"))
    )
    print("Database 'university' dropped.")

    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("university")))
    print("Database 'university' created.")

    cur.close()
    conn.close()

    # connect to university db
    conn = psycopg2.connect(**userParams, dbname="university")
    cur = conn.cursor()

    # populate db
    cur.execute(
        """
        CREATE TABLE students (
            student_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            enrollment_date DATE
        )
    """
    )

    cur.execute(
        """
        INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
        ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
    """
    )

    conn.commit()
    print("Database populated with initial data.")

    return conn
