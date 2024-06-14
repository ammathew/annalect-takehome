## API Documentation

#### Curl a Post request example

curl -XPOST -H "Content-Type: application/json" -d '{ "Attack": 85,
    "Defense": 60,
    "Generation": 3,
    "HP": 60,
    "Legendary": false,
    "Name": "NewMon",
    "Sp. Atk": 85,
    "Sp. Def": 60,
    "Speed": 55,
    "Total": 405,
    "Type 1": "Fire",
    "Type 2": "Fighting"
  }' 'http://localhost:5000/pokemon'
