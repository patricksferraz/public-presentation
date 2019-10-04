import psycopg2


class Postgres:
    def __init__(
        self,
        host="172.18.0.2",
        db="address",
        user="postgres",
        pas="mysecretpass",
    ):
        self.postgres_url = host
        self.postgres_db = db
        self.postgres_user = user
        self.postgres_pw = pas
        self.con = self.connect()
        self.cur = self.con.cursor()

    def connect(self):
        try:
            return psycopg2.connect(
                host=self.postgres_url,
                database=self.postgres_db,
                user=self.postgres_user,
                password=self.postgres_pw,
            )
        except Exception as e:
            return e

    def close(self):
        self.con.close()

    def get_state(self, state: str, limit: int, page: int) -> list:
        """Return all states of postgres database

        Arguments:
            state {str} -- State name for search
            limit {int} -- Results limit
            page {int} -- Results page
            cur {cursor} -- Cursor postgres for database

        Returns:
            list -- all states from database
        """
        sql = f"""
            SELECT id, nome, sigla
            FROM estado WHERE nome ILIKE '%{state}%'
            ORDER BY nome
            LIMIT {limit} OFFSET {page * limit};
            """

        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_city(self, data: dict, limit: int, page: int) -> list:
        """Return all cities of postgres database

        Arguments:
            data {dict} -- Dictionary with {"state": state, "city": city}
                key-value pair
            limit {int} -- Results limit by state
            page {int} -- Results page
            cur {cursor} -- Cursor postgres for database

        Returns:
            list -- all cities from database
        """
        sql = f"""
            SELECT es.id,
                es.nome,
                es.sigla,
                array_agg(array[
                    cast(ci.id AS TEXT),
                    cast(ci.id_estado AS TEXT),
                    ci.nome
                ])
            FROM estado es INNER JOIN (
                SELECT c.id, c.id_estado, c.nome
                FROM cidade c INNER JOIN estado e
                    ON c.id_estado = e.id
                WHERE e.nome ILIKE '%{data["state"]}%'
                    AND c.nome ILIKE '%{data["city"]}%'
                ORDER BY c.nome ASC
                LIMIT {limit} OFFSET {page * limit}
            ) AS ci
                ON es.id = ci.id_estado
            GROUP BY es.id, es.nome, es.sigla
            ORDER BY es.nome ASC;
            """

        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_place(self, data: dict, limit: int, page: int) -> list:
        """Return all places of postgres database

        Arguments:
            data {dict} -- Dictionary with
                {"state": state, "city": city, "place": place} key-value pair
            limit {int} -- Results limit by state
            page {int} -- Results page
            cur {cursor} -- Cursor postgres for database

        Returns:
            list -- all places from database
        """
        sql = f"""
            SELECT e.id,
                e.nome,
                e.sigla,
                array_agg(array[
                    cast(c.id AS TEXT),
                    cast(c.id_estado AS TEXT),
                    c.nome,
                    c.place
                ])
            FROM estado e INNER JOIN (
                SELECT c.id,
                    c.id_estado,
                    c.nome,
                    string_agg(concat_ws(
                        ',',
                        cast(p.cep AS TEXT),
                        cast(p.id_estado AS TEXT),
                        cast(p.id_cidade AS TEXT),
                        p.bairro,
                        p.logradouro
                    ), ';') AS place
                FROM cidade c INNER JOIN (
                    SELECT p.cep,
                        p.id_estado,
                        p.id_cidade,
                        p.bairro,
                        p.logradouro
                    FROM cep p INNER JOIN cidade c
                        ON p.id_cidade = c.id INNER JOIN estado e
                        ON c.id_estado = e.id
                    WHERE e.nome ILIKE '%{data["state"]}%'
                        AND c.nome ILIKE '%{data["city"]}%'
                        AND (cast(p.cep as TEXT) ILIKE '%{data["place"]}%'
                            OR p.bairro ILIKE '%{data["place"]}%'
                            OR p.logradouro ILIKE '%{data["place"]}%'
                        )
                    ORDER BY p.bairro ASC, p.logradouro ASC
                    LIMIT {limit} OFFSET {page * limit}
                ) AS p
                    ON c.id = p.id_cidade
                GROUP BY c.id, c.id_estado, c.nome
            ) AS c
                ON e.id = c.id_estado
            GROUP BY e.id, e.nome, e.sigla
            """

        self.cur.execute(sql)
        return self.cur.fetchall()
