-- $ sqlite3 music.db < sqlite.sql

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
    id INTEGER primary key,
    userid INTEGER,
    title VARCHAR,
    description VARCHAR NULL
);

INSERT INTO playlist(userid,title,description) VALUES (1,'first playlist','cool songs');

DROP TABLE IF EXISTS playlist_tracks;
CREATE TABLE playlist_tracks(
    playlist_id INTEGER,
    track_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES playlist(id),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    UNIQUE(username)
);

/*
-- $ sqlite3 descriptions.db < sqlite.sql

*DROP TABLE IF EXISTS descriptions;
*CREATE TABLE descriptions (
	*id INTEGER PRIMARY KEY AUTOINCREMENT,
	*description VARCHAR,
	*username VARCHAR,
	*url VARCHAR
	*FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
	*FOREIGN KEY (url) REFERENCES tracks(url) ON DELETE CASCADE
);
*/
