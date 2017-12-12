import psycopg2


class PostgresDb:
    conn = psycopg2.connect("host='localhost' dbname='telegram' user='gordon' password='localpass'")
    cur = conn.cursor()

    def __init__(self):

        self.cur.execute("""create table if not exists sessions(
                         pk SERIAL PRIMARY KEY,
                         chat_id int,
                         command varchar,
                         vars text array)""")
        self.conn.commit()

    # Session ---------------------------------------------------------------------/

    def add_session(self, chat_id, command):
        self.cur.execute("""insert into sessions(chat_id, command)
                                values({chat_id}, '{command}')""".format(chat_id=chat_id, command=command))
        self.conn.commit()

    def check_session(self, chat_id):
        self.cur.execute("""select chat_id, command, vars from sessions 
                                where chat_id={chat_id}""".format(chat_id=chat_id))
        return self.cur.fetchone()

    def clear_session(self, chat_id):
        self.cur.execute("""delete from sessions 
                                where chat_id={chat_id}""".format(chat_id=chat_id))
        self.conn.commit()

    def update_session(self, chat_id, var):
        self.cur.execute(
            """update sessions 
                    set vars=array_append(vars, '{var}') 
                        where chat_id={chat_id}""".format(var=var,
                                                          chat_id=chat_id))
        self.conn.commit()

    def remove_var_session(self, chat_id, var):
        self.cur.execute("""update sessions
                                set vars=array_remove(vars, '{var}') 
                                    where chat_id={chat_id}""".format(var=var,
                                                                      chat_id=chat_id))
        self.conn.commit()



