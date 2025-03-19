import csv
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_sum():
    data = request.get_json()

    if not data or 'file' not in data or 'product' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data['product']

    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = f"/Niv_PV_dir/{file_name}"

    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            total_sum = 0
            for row in csv_reader:
                if len(row) != len(header):
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
                row_data = dict(zip(header, row))
                if row_data['product'] == product:
                    total_sum += int(row_data['amount'])

            return jsonify({"file": file_name, "sum": total_sum}), 200
    except Exception:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)