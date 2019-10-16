-- :name all_descriptions :many
SELECT username, url, description FROM descriptions WHERE username=? AND url=?;
