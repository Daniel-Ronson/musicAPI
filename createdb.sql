-- $ sqlite3 tracks.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    duration VARCHAR,  
    url VARCHAR,     
    artUrl VARCHAR NULL,
    UNIQUE(title, artist)
);
INSERT INTO tracks(title,album,artist,duration,url) VALUES('song title','album title','artist name','3.04','c://music/uniquesong');

DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist (
    title VARCHAR,
    description VARCHAR

);