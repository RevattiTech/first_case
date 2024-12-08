import time
from flask import Flask, request, jsonify, Blueprint
from marshmallow import ValidationError
from src.core.hosts import scan_ports
from src.core.sploitus import  check_vulnerabilities
from src.service.service import Service
from src.sh.sh import ScanSh

route = Blueprint('main', __name__)
service = Service()

@route.route('/vulnerabilities/<int:chat_id>', methods=['GET'])
def vulnerabilities(chat_id: int):
    """
      Get the vulnerability history for a specific chat ID.

      This endpoint retrieves a list of past vulnerability scan results for a specific user identified by `chat_id`.

      ---
      tags:
        - Vulnerabilities
      parameters:
        - name: chat_id
          in: path
          type: integer
          required: true
          description: The chat ID of the user for whom the vulnerability history is being fetched.
      responses:
        200:
          description: The vulnerability history for the specified `chat_id`.
          schema:
            type: object
            properties:
              status:
                type: string
                description: The status of the request (e.g., "success").
              data:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: string
                      description: Unique identifier for the request.
                    host:
                      type: string
                      description: The host URL or IP address where the scan was performed.
                    execution_time:
                      type: string
                      description: The time it took to complete the scan.
                    status:
                      type: string
                      description: The status of the vulnerability scan (e.g., "success", "failed").
                    open_port:
                      type: string
                      description: Open ports found during the scan.
                    vulnerabilities:
                      type: array
                      items:
                        type: string
                      description: A list of vulnerabilities found during the scan.
                    user_id:
                      type: integer
                      description: The chat ID of the user.
        500:
          description: Internal server error.
          schema:
            type: object
            properties:
              error:
                type: string
                description: Error message describing the internal issue.
      """
    try:
        result = service.history(chat_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@route.route('/scan', methods=['POST'])
def scan():
    """
       Scan a target URL for open ports and vulnerabilities.

       This endpoint accepts a POST request with a URL to scan and an optional `user_id`.
       It returns the scan results, including the list of open ports, found vulnerabilities,
       and the status of the target (vulnerable or not).

       ---
       tags:
         - Scan
       parameters:
         - name: url
           in: body
           type: string
           required: true
           description: URL of the target to scan.
         - name: user_id
           in: body
           type: string
           required: false
           description: The user ID associated with the scan request.
       responses:
         200:
           description: The scan results with open ports and vulnerabilities.
           schema:
             type: object
             properties:
               url:
                 type: string
                 description: The URL of the scanned target.
               open_ports:
                 type: array
                 items:
                   type: integer
                 description: List of open ports found on the target.
               vulnerabilities:
                 type: array
                 items:
                   type: string
                 description: List of vulnerabilities found on the target.
               status:
                 type: string
                 description: The status of the scan ('vulnerable' or 'not_vulnerable').
               execution_time:
                 type: number
                 format: float
                 description: Time taken to complete the scan (in seconds).
               user_id:
                 type: string
                 description: The user ID associated with the scan request (optional).
         400:
           description: Invalid input provided.
           schema:
             type: object
             properties:
               error:
                 type: string
                 description: Error message indicating the invalid input.
               details:
                 type: object
                 description: Validation error details.
         500:
           description: Internal server error.
           schema:
             type: object
             properties:
               error:
                 type: string
                 description: Error message describing the internal issue.
       """
    try:
        request_data = request.get_json()
        schema = ScanSh()
        data = schema.load(request_data)

        url = data['url']
        user_id = data.get('user_id')

        start_time = time.time()

        open_ports = scan_ports(url)

        if not open_ports:
            return jsonify({
                "status": "no_ports_found",
                "message": "No open ports found on the target.",
                "execution_time": time.time() - start_time
            }), 200

        vulnerabilities = check_vulnerabilities(url,
                                                open_ports)

        result = {
            "url": url,
            "open_ports": open_ports,
            "vulnerabilities": vulnerabilities,
            "status": "vulnerable" if vulnerabilities else "not_vulnerable",
            "execution_time": time.time() - start_time,
            "user_id": user_id,
        }

        service.save_req(result)

        return jsonify(result), 200

    except ValidationError as err:
        return jsonify({"error": "Invalid input", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@route.route('/data/<string:name>', methods=['GET'])
def data(name):
    """
        Получить данные по заданному имени.

        ---
        parameters:
          - name: name
            in: path
            type: string
            required: true
            description: Имя для поиска данных

        responses:
          200:
            description: Данные успешно получены
            schema:
              type: object
              properties:
                href:
                  type: string
                  description: Ссылка на эксплойт
                  example: "https://github.com/blackmagic2023/AnyDesk-7.0.15---Unquoted-Service-Path-PoC"
                id:
                  type: string
                  description: Идентификатор
                  example: "38b128a3-44f4-45ec-aa3d-b76f62ad7f0e"
                language:
                  type: string
                  description: Язык эксплойта
                  example: "MARKDOWN"
                name:
                  type: string
                  description: Имя эксплойта
                  example: "poc"
                published:
                  type: string
                  description: Дата публикации
                  example: "2024-04-10T00:00:00"
                score:
                  type: string
                  description: Оценка эксплойта
                  example: "7.8"
                source:
                  type: string
                  description: Источник
                  example: "## https://sploitus.com/exploit?id=F3E7A4E0-2927-5CF0-961C-D7E7AB6CFFB3"
          404:
            description: Данные не найдены
        """
    res = service.all_data(name)
    return jsonify(res), 200
