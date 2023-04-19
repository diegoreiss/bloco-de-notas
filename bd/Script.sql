CREATE TABLE IF NOT EXISTS categoria(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome VARCHAR(30) NOT NULL
    cor VARCHAR(30) NULL
)

CREATE TABLE IF NOT EXISTS nota(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(60) NOT NULL,
	data DATE NOT NULL,
	texto TEXT NOT NULL,
    last_update DATETIME NULL,
    categoria_id INTEGER,
    CONSTRAINT fk_nota_categoria
        FOREIGN KEY(categoria_id)
        REFERENCES categoria(id)
);

CREATE TRIGGER IF NOT EXISTS atualiza_last_update
AFTER UPDATE ON nota
FOR EACH ROW
BEGIN
	UPDATE nota SET last_update = datetime('now', 'localtime') WHERE id = OLD.id;
END;