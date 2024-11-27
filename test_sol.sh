#!/bin/bash

echo "Adding transactions"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}' "http://localhost:8000/add"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"}' "http://localhost:8000/add"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "DANNON", "points":-200, "timestamp": "2022-10-31T15:00:00Z"}' "http://localhost:8000/add"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"}' "http://localhost:8000/add"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}' "http://localhost:8000/add"

echo "Spending points"
curl --request POST --header "Content-Type: application/json" --data '{"points": 5000}' "http://localhost:8000/spend"

echo "Getting balance"
curl --request GET "http://localhost:8000/balance"

# Using base shell to see the output (not shutdown immediately)
$SHELL