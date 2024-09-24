from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    mask_status = db.Column(db.Boolean, nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/entry', methods=['POST'])
def add_entry():
    try:
        temperature = request.form['temperature']
        mask_status = request.form['mask_status'].lower() == 'true'
        image = request.files['image']

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Save the image file
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

        # Create a new Entry instance and save it to the database
        new_entry = Entry(temperature=float(temperature), mask_status=mask_status, image_path=image_path)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({'message': 'Entry added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/entries', methods=['GET'])
def get_entries():
    entries = Entry.query.all()
    results = []
    for entry in entries:
        results.append({
            'id': entry.id,
            'timestamp': entry.timestamp,
            'temperature': entry.temperature,
            'mask_status': entry.mask_status,
            'image_path': entry.image_path
        })
    return jsonify(results)

@app.route('/api/real_time_data', methods=['GET'])
def get_real_time_data():
    latest_entry = Entry.query.order_by(Entry.timestamp.desc()).first()
    if latest_entry:
        return jsonify({
            'current_reading': {
                'temperature': latest_entry.temperature,
                'mask_status': latest_entry.mask_status,
                'timestamp': latest_entry.timestamp,
                'image_path': latest_entry.image_path  # Include the image path
            }
        })
    return jsonify({'error': 'No data available'}), 404

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)