curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeColumn":"title","changeValueTo":"Test Update 1", "artist": "Test artist 1","title":"Test Insert song 2"}' \
  http://127.0.0.1:5100/api/resources/tracks/update
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeColumn":"title","changeValueTo":"Test Update 2","id":"4"}' \
  http://127.0.0.1:5100/api/resources/tracks/update
