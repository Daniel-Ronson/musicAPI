curl \
  --header "Content-type: application/json" \
  --request DELETE \
  --data '{"id": 1}' \
  http://127.0.0.1:5100/api/resources/tracks/delete/1
  curl \
  --header "Content-type: application/json" \
  --request DELETE \
  --data '{"id": 3}' \
  http://127.0.0.1:5100/api/resources/tracks/delete/3
