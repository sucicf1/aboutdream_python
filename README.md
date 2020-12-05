to add a user execute
curl --header "Content-Type: application/json" --request POST --data "{\"username\":\"ivan\",\"password\":\"ivan\"}" http://localhost:5000/users/new

now you need to get the token for authentication with 
curl --header "Content-Type: application/json" --request POST --data "{\"username\":\"ivan\",\"password\":\"ivan\"}" http://localhost:5000/users/token

to add a message execute
curl --form "file=@moj.jpg" --form token="eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzExNDY4NCwiZXhwIjoxNjA3MTE1Mjg0fQ.eyJpZCI6MX0.bViVUkL_wuLu_UlRz3GO32fga5MKqED8XTs6KDy0BxidGTOXjn5VSFMoz1LjUup6EQd479xivKi37s2leDqxzQ" --form text="poruka" http://localhost:5000/messages

to delete message execute
curl --header "Content-Type: application/json" --request POST --data "{\"token\":\"eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzE5MzM3OSwiZXhwIjoxNjA3MTkzOTc5fQ.eyJpZCI6MX0.XL1MRwYrvVke6afCVF8fq6B2UU1CMEUc05gy6UcKDwlvog71drF2DbJomkR_C6tU1w55BE5CrTp25J5JLaedig\"}" http://localhost:5000/messages/delete/<int:_id>

to follow a user execute
curl --header "Content-Type: application/json" --request POST --data "{\"token\":\"eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzE5MzM3OSwiZXhwIjoxNjA3MTkzOTc5fQ.eyJpZCI6MX0.XL1MRwYrvVke6afCVF8fq6B2UU1CMEUc05gy6UcKDwlvog71drF2DbJomkR_C6tU1w55BE5CrTp25J5JLaedig\", \"followee_id\":\"2\"}" "http://localhost:5000/follow/add"

to stop following a user execute
curl --header "Content-Type: application/json" --request POST --data "{\"token\":\"eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzAzNDc4MCwiZXhwIjoxNjA3MDM1MzgwfQ.eyJpZCI6MX0.EqboYzxYeBsYZYkY7hRK5YzuacBYVB_TClNLdLyv8cjlArZdJuNr_gvsiPqJ8KEa2dVD9RXWnMS_doxpr0Ra9w\"}" "http://localhost:5000/follow/delete/<int:_id>"

to see a image open http://localhost:5000/image/<name>

to see all messages open http://localhost:5000/timeline

to see only messages of users you are following execute
curl --header "Content-Type: application/json" --request POST --data "{\"token\":\"eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzAzNDc4MCwiZXhwIjoxNjA3MDM1MzgwfQ.eyJpZCI6MX0.EqboYzxYeBsYZYkY7hRK5YzuacBYVB_TClNLdLyv8cjlArZdJuNr_gvsiPqJ8KEa2dVD9RXWnMS_doxpr0Ra9w\"}" "http://localhost:5000/timeline?followee=true"

you can apply variosu filters to both timeline. To see messages after some time using unicode time execute
curl --header "Content-Type: application/json" --request POST --data "{\"token\":\"eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzE5NjgwMywiZXhwIjoxNjA3MTk3NDAzfQ.eyJpZCI6MX0.Bb49JJiLlfmxo6QXScD3VwXamBmFX1aLXvv7IhpT0kU0dap51Q3iOPu7W4sC3qGLQyNwIzwjp8O4bmno64AnGA\"}" "http://localhost:5000/timeline?asc=false&start_date=1607190300&end_date=1607190480&followee=true&page=1"
