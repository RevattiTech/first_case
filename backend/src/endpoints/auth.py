import base64
import hashlib
import hmac
import json
from flask import Blueprint, request, redirect, jsonify, render_template_string
from cfg.base import cfg
from src.service.service import Service

auth = Blueprint('auth', __name__)
service = Service()

def check_telegram_auth(data, bot_token):
    check_hash = data.pop('hash', None)
    if not check_hash:
        return False

    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])

    secret_key = hashlib.sha256(bot_token.encode()).digest()

    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <script type="text/javascript">
        const hash = window.location.hash.substring(1);  // Считываем фрагмент (#tgAuthResult=...)
        if (hash) {
            const params = new URLSearchParams(hash);
            const tgAuthResult = params.get("tgAuthResult");
            if (tgAuthResult) {
                window.location.href = `/api/v1/s?tgAuthResult=${encodeURIComponent(tgAuthResult)}`;
            }
        }
    </script>
</head>
<body>
    <p>Processing...</p>
</body>
</html>
"""


@auth.route('/auth', methods=['GET'])
def process_fragment():
    return render_template_string(HTML_TEMPLATE)


@auth.route('/login', methods=['GET'])
def logins():
    bot_id = cfg.BOT_TOKEN.split(':')[0]
    telegram_auth_url = (
        f"https://oauth.telegram.org/auth"
        f"?bot_id={bot_id}"
        f"&origin=https://703b-85-92-121-226.ngrok-free.app/api/v1/auth"
        f"&request_access=write"
    )
    return redirect(telegram_auth_url)


def get_jwt_header(jwt_token):
    parts = jwt_token.split('.')

    header = parts[0]

    padding = '=' * (4 - len(header) % 4)
    decoded_header = base64.urlsafe_b64decode(header + padding)

    try:
        header_data = json.loads(decoded_header)
        return header_data
    except json.JSONDecodeError as e:
        print(f"Error decoding the header: {e}")
        return None


@auth.route('/s', methods=['GET'])
def login():
    tg_auth_result = request.args.get('tgAuthResult')
    print(tg_auth_result)
    if not tg_auth_result:
        return jsonify({"error": "Missing 'tgAuthResult' in request data"}), 400

    auth_data = get_jwt_header(tg_auth_result)

    service.login_user(auth_data)

    return jsonify({"status": "success", "user": auth_data}), 200

