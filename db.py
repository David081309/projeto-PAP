import mysql.connector
import pandas as pd
from mysql.connector import Error, IntegrityError


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "projeto16"


# ─────────────────────────────────────────────
# LIGAÇÃO À BASE DE DADOS
# ─────────────────────────────────────────────

def get_connection(use_database=True):
    """
    Cria ligação ao MySQL.
    Se use_database=False, liga apenas ao servidor MySQL.
    Se use_database=True, liga diretamente à base de dados projeto16.
    """

    if use_database:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ─────────────────────────────────────────────
# INICIALIZAÇÃO DA BASE DE DADOS
# ─────────────────────────────────────────────

def init_db():
    """
    Cria a base de dados e as tabelas necessárias para a aplicação.
    Mantém o mesmo nome da função usada no app.py.
    """

    cnx = get_connection(use_database=False)
    cur = cnx.cursor()

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cnx.commit()

    cur.close()
    cnx.close()

    cnx = get_connection(use_database=True)
    cur = cnx.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS incomes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            description VARCHAR(255) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            income_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            description VARCHAR(255) NOT NULL,
            category VARCHAR(100) NOT NULL,
            kind VARCHAR(100) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            expense_date DATE NOT NULL,
            is_recurring TINYINT NOT NULL DEFAULT 0,
            frequency VARCHAR(50),
            next_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            target_amount DECIMAL(10,2) NOT NULL,
            saved_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
            deadline DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    cnx.commit()
    cur.close()
    cnx.close()


# ─────────────────────────────────────────────
# UTILIZADORES
# ─────────────────────────────────────────────

def create_user(username, password):
    cnx = get_connection()
    cur = cnx.cursor()

    try:
        cur.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (username, password)
        )
        cnx.commit()
        return True

    except IntegrityError:
        return False

    finally:
        cur.close()
        cnx.close()


def get_user(username, password):
    cnx = get_connection()
    cur = cnx.cursor()

    cur.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = %s AND password = %s
        """,
        (username, password)
    )

    user = cur.fetchone()

    cur.close()
    cnx.close()

    return user


def user_exists(username):
    cnx = get_connection()
    cur = cnx.cursor()

    cur.execute(
        """
        SELECT id
        FROM users
        WHERE username = %s
        """,
        (username,)
    )

    user = cur.fetchone()

    cur.close()
    cnx.close()

    return user is not None


# ─────────────────────────────────────────────
# RECEITAS
# ─────────────────────────────────────────────

def add_income(user_id, description, amount, income_date):
    cnx = get_connection()
    cur = cnx.cursor()

    cur.execute(
        """
        INSERT INTO incomes 
        (user_id, description, amount, income_date)
        VALUES (%s, %s, %s, %s)
        """,
        (
            int(user_id),
            description,
            float(amount),
            str(income_date)
        )
    )

    cnx.commit()
    cur.close()
    cnx.close()


def get_incomes(user_id):
    cnx = get_connection()

    query = """
        SELECT *
        FROM incomes
        WHERE user_id = %s
        ORDER BY income_date DESC
    """

    df = pd.read_sql_query(
        query,
        cnx,
        params=(int(user_id),)
    )

    cnx.close()

    return df


# ─────────────────────────────────────────────
# DESPESAS
# ─────────────────────────────────────────────

def add_expense(
    user_id,
    description,
    category,
    kind,
    amount,
    expense_date,
    is_recurring=0,
    frequency=None,
    next_date=None
):
    cnx = get_connection()
    cur = cnx.cursor()

    cur.execute(
        """
        INSERT INTO expenses
        (
            user_id,
            description,
            category,
            kind,
            amount,
            expense_date,
            is_recurring,
            frequency,
            next_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            int(user_id),
            description,
            category,
            kind,
            float(amount),
            str(expense_date),
            int(is_recurring),
            frequency,
            str(next_date) if next_date else None
        )
    )

    cnx.commit()
    cur.close()
    cnx.close()


def get_expenses(user_id):
    cnx = get_connection()

    query = """
        SELECT *
        FROM expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC
    """

    df = pd.read_sql_query(
        query,
        cnx,
        params=(int(user_id),)
    )

    cnx.close()

    return df


def delete_expense(record_id, user_id):
    cnx = get_connection()
    cur = cnx.cursor()

    cur.execute(
        """
        DELETE FROM expenses
        WHERE id = %s AND user_id = %s
        """,
        (
            int(record_id),
            int(user_id)
        )
    )

    cnx.commit()
    cur.close()
    cnx.close()


# ─────────────────────────────────────────────
# METAS DE POUPANÇA
# ─────────────────────────────────────────────

def add_goal(user_id, title, target_amount, saved_amount, deadline):
    cnx = get_connection()
    cur = cnx.cursor()

    cur.execute(
        """
        INSERT INTO goals
        (
            user_id,
            title,
            target_amount,
            saved_amount,
            deadline
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            int(user_id),
            title,
            float(target_amount),
            float(saved_amount),
            str(deadline)
        )
    )

    cnx.commit()
    cur.close()
    cnx.close()


def get_goals(user_id):
    cnx = get_connection()

    query = """
        SELECT *
        FROM goals
        WHERE user_id = %s
        ORDER BY id DESC
    """

    df = pd.read_sql_query(
        query,
        cnx,
        params=(int(user_id),)
    )

    cnx.close()

    return df