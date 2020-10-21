DROP TABLE IF EXISTS JLPTVocab;

CREATE TABLE JLPTVocab (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  level CHAR(2) NOT NULL,
  kanji VARCHAR2(10),
  furigana VARCHAR2(10),
  hiragana VARCHAR2(5) NOT NULL,
  pos VARCHAR2(40),
  definition VARCHAR2(20),
  example VARCHAR2(50)
);