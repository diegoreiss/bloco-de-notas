CREATE TABLE IF NOT EXISTS nota(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(60) NOT NULL,
	data DATE NOT NULL,
	texto TEXT NOT NULL
);