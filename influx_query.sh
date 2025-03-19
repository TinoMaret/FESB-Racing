#!/bin/bash

# InfluxDB details
INFLUX_URL="http://localhost:8086"  # Replace with your InfluxDB URL
TOKEN="zR7YNtfJkM5Yq2u8Jt0QgUvZFoSnqSjSthyFaPcb7j-BDNF7fuLUc_OM_n1-qbveuZg8G6UoyYD5NoGQuj0zIQ=="  # Your InfluxDB API token
ORG="Racing"  # Your organization name
BUCKET="racing"  # Your bucket name
QUERY='from(bucket: "'$BUCKET'") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "can_data") |> filter(fn: (r) => r["_field"] == "data")'

# File path to save the output (Desktop)
OUTPUT_FILE="$HOME/Desktop/influx_query_output.json"  # Save the output to a file on your Desktop

# Sending request to InfluxDB API and saving the response to a file
curl -X POST "$INFLUX_URL/api/v2/query?org=$ORG" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/vnd.flux" \
  -d "$QUERY" > "$OUTPUT_FILE"

# Notify user
echo "Query executed and saved to $OUTPUT_FILE"
