from dataclasses import dataclass
import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(f"{db_name}.db")

        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS dados_pessoais (nome_da_rua TEXT NOT NULL, cpf TEXT NOT NULL UNIQUE, identificador INTEGER PRIMARY KEY)"
        )

        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)"
        )

    def add(self, note):
        self.conn.execute(
            "INSERT INTO note (title, content) VALUES (?, ?)",
            (note.title, note.content)
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM note")
        return [Note(id, title, content) for id, title, content in cursor]

    def update(self, entry):
        self.conn.execute(
            "UPDATE note SET title = ?, content = ? WHERE id = ?",
            (entry.title, entry.content, entry.id)
        )
        self.conn.commit()

    def delete(self, note_id):
        self.conn.execute(
            "DELETE FROM note WHERE id = ?",
            (note_id,)
        )
        self.conn.commit()


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
