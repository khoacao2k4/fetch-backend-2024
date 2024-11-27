#!/bin/bash

echo "Adding transactions"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "DANNON", "points": 1000, "timestamp": "2022-10-31T10:00:00Z"}' "http://localhost:8000/add"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "UNILEVER", "points": 500, "timestamp": "2022-10-31T11:00:00Z"}' "http://localhost:8000/add"
curl --request POST --header "Content-Type: application/json" --data '{"payer": "DANNON", "points":-500, "timestamp": "2022-10-31T15:00:00Z"}' "http://localhost:8000/add"

echo "Spending points"
echo "First one should fail with 400"
curl --request POST --header "Content-Type: application/json" --data '{"points": 1100}' "http://localhost:8000/spend"
echo "Second one should succeed with 200"
curl --request POST --header "Content-Type: application/json" --data '{"points": 750}' "http://localhost:8000/spend"

echo "Getting balance"
curl --request GET "http://localhost:8000/balance"

# Using base shell to see the output (not shutdown immediately)
$SHELL