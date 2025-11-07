# 🎯 src/api/app.py - Endpoints profissionais
@app.route('/api/v1/sensors/current', methods=['GET'])
def get_current_sensors():
    """Retorna dados atuais dos sensores"""
    return jsonify({
        'temperature': get_temperature(),
        'humidity': get_humidity(),
        'soil_moisture': get_soil_moisture(),
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/v1/control/irrigation', methods=['POST'])
def control_irrigation():
    """Controla sistema de irrigação"""
    data = request.get_json()
    duration = data.get('duration', 30)
    start_watering(duration)
    return jsonify({'status': 'watering_started', 'duration': duration})
