import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from outline_vpn.outline_vpn import OutlineVPN

app = Flask(__name__)
CORS(app)

# Настройка доступа к API Outline
client = OutlineVPN(api_url="https://51.38.154.86:50316/-VoYdL-pnwhyKgTzUf9dFg",
                    cert_sha256="BBE0630ED9A12C15221C7C6D54597E863F1A63367F2D0867041410C532BBC681")

def delete_key_after_delay(key_id, delay):
    """Удаляет ключ через определённое время (в секундах)."""
    threading.Timer(delay, delete_key, [key_id]).start()

def delete_key(key_id):
    """Удаляет ключ по ID."""
    try:
        client.delete_key(key_id)
        print(f'Key {key_id} deleted successfully')
    except Exception as e:
        print(f'Error deleting key {key_id}: {e}')

@app.route('/create_key', methods=['POST'])
def create_key():
    try:
        data = request.get_json()
        duration = int(data.get('duration', 60))  # Время по умолчанию - 1 минута (60 секунд)
        
        new_key = client.create_key()
        key_id = new_key.key_id
        access_url = new_key.access_url

        # Запланировать удаление ключа через выбранное время
        delete_key_after_delay(key_id, duration)

        return jsonify({'key_id': key_id, 'access_url': access_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
