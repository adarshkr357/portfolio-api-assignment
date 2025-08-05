import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from tools.resume_parser import parse_resume
from tools.translator import translate_text
from tools.currency import convert_currency

app = Flask(__name__)
CORS(app)

# Config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

# Resume Parser Section
@app.route('/api/parse-resume', methods=['POST'])
def resume_api():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if file and is_allowed_file(file.filename):
        filename = file.filename.replace(" ", "_")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            website_data = parse_resume(filepath)
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            os.remove(filepath)

        return jsonify({'success': True, 'data': website_data}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid file type'}), 400

# Translation Section
@app.route('/api/translate', methods=['POST'])
def translate_api():
    data = request.get_json()
    text = data.get('text')
    target = data.get('target_language', 'hi')
    source = data.get('source_language', 'auto')

    if not text:
        return jsonify({'success': False, 'message': 'No text provided'}), 400

    try:
        translated = translate_text(text, target, source)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    return jsonify({'success': True, 'translated': translated}), 200

# Currency Conversion Section
@app.route('/api/currency/convert', methods=['POST'])
def currency_api():
    try:
        data = request.get_json()

        amount = float(data.get('amount', 1))
        from_currency = data.get('from_currency', 'USD').upper()
        to_currency = data.get('to_currency', 'INR').upper()

        if not from_currency or not to_currency:
            return jsonify({'success': False, 'message': 'Currency codes missing'}), 400

        result = convert_currency(amount, from_currency, to_currency)

        return jsonify({
            'success': True,
            'converted_amount': result['converted_amount'],
            'exchange_rate': result['exchange_rate']
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
