curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Test Insert song 2","album":"Test Album 1","artist":"Test artist 1","duration":"3:40","url":"C://songs/s23","arturl":"C;//song/img/s23"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Test Insert Song 2","album":"Test Album 2","artist":"Test artist 2","duration":"4:10","url":"C://songs/s23","arturl":"C;//song/img/s23"}' \
  http://127.0.0.1:5100/api/resources/tracks
