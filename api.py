from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

pokemon_dataframe = pd.read_csv('Pokemon.csv')

# Use this instead if want to allow users to update CSV/persist data across server restarts
# pokemon_dataframe = pd.read_csv('PokemonPersist.csv')

@app.route('/pokemon', methods=['GET'])
def get_pokemon():
    all_pokemon_data = pokemon_dataframe.to_dict('records')
    return jsonify(all_pokemon_data)

@app.route('/pokemon/<int:id>/attack-strength', methods=['GET'])
def get_strength(id):
    pokemon = pokemon_dataframe[pokemon_dataframe['#'] == id]
    if pokemon.empty:
        return jsonify({"message": "Pokemon ID Not Found"}), 404   
    return jsonify({'attackStrength': int(pokemon['Attack'].values[0])})

@app.route('/pokemon', methods=['POST'])
def create_pokemon():
    data = request.get_json()
    required_fields = ['Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing fields"}), 400

    global pokemon_dataframe
    new_id = pokemon_dataframe['#'].max() + 1
    new_pokemon = pd.DataFrame([dict(data, **{'#': new_id})], columns=['#'] + required_fields)
    pokemon_dataframe = pd.concat([pokemon_dataframe, new_pokemon], ignore_index=True)

    # Persist this new data across server restarts
    pokemon_dataframe.to_csv('PokemonPersist.csv', index=False)

    return jsonify(new_pokemon.to_dict('records')[0]), 201


@app.route('/pokemon/type/<type>', methods=['GET'])
def get_pokemon_by_type(type):
    pokemon_of_type = pokemon_dataframe[(pokemon_dataframe['Type 1'] == type) | (pokemon_dataframe['Type 2'] == type)]
    if pokemon_of_type.empty:
        return jsonify({"message": "No Pokemon of this type were found"}), 404
    return jsonify(pokemon_of_type.to_dict('records'))


if __name__ == "__main__":
    app.run(debug=True)