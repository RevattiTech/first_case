import asyncio
import json
import socket
from pyppeteer import launch

from src.service.service import Service

service = Service()


async def parse_page_poc():
    # Запускаем браузер с DevTools
    browser = await launch(headless=False, devtools=True)
    page = await browser.newPage()

    # Включаем протокол DevTools
    client = await page.target.createCDPSession()
    await client.send("Network.enable")  # Включаем сетевые события

    # Переменная для хранения данных целевого запроса
    target_request_data = None

    # Обработчик события ответа
    async def capture_response(event):
        try:
            url = event.get("response", {}).get("url", "N/A")
            status = event.get("response", {}).get("status", "N/A")

            # Фильтруем только нужный URL
            if url == "https://sploitus.com/search" and status == 200:
                # Получаем тело ответа
                response_body_data = await client.send("Network.getResponseBody", {"requestId": event["requestId"]})
                response_body = response_body_data.get("body", "{}")  # Дефолтное значение - пустой JSON

                target_request_data = {
                    "url": url,
                    "status": status,
                    "headers": event.get("response", {}).get("headers", {}),
                    "mimeType": event.get("response", {}).get("mimeType", "N/A"),
                    "body": json.loads(response_body)
                }


                data = json.loads(response_body)
                service.save_poc_or_ext(data, "poc")

        except Exception as e:
            print(f"Ошибка обработки целевого ответа: {e}")

    # Подписываемся только на событие ответа
    client.on("Network.responseReceived", lambda event: asyncio.create_task(capture_response(event)))

    # Загружаем страницу
    await page.goto('https://sploitus.com/?query=POC#exploits')

    await page.waitForSelector('body')
    await asyncio.sleep(5)


    await browser.close()

    # Возвращаем данные о целевом запросе
    return target_request_data


async def parse_page_exploit():
    # Запускаем браузер с DevTools
    browser = await launch(headless=False, devtools=True)
    page = await browser.newPage()

    # Включаем протокол DevTools
    client = await page.target.createCDPSession()
    await client.send("Network.enable")  # Включаем сетевые события

    # Переменная для хранения данных целевого запроса
    target_request_data = None

    # Обработчик события ответа
    async def capture_response(event):
        try:
            url = event.get("response", {}).get("url", "N/A")
            status = event.get("response", {}).get("status", "N/A")

            # Фильтруем только нужный URL
            if url == "https://sploitus.com/search" and status == 200:
                # Получаем тело ответа
                response_body_data = await client.send("Network.getResponseBody", {"requestId": event["requestId"]})
                response_body = response_body_data.get("body", "{}")  # Дефолтное значение - пустой JSON

                target_request_data = {
                    "url": url,
                    "status": status,
                    "headers": event.get("response", {}).get("headers", {}),
                    "mimeType": event.get("response", {}).get("mimeType", "N/A"),
                    "body": json.loads(response_body)
                }

                data = json.loads(response_body)
                service.save_poc_or_ext(data, "exploit")

        except Exception as e:
            print(f"Ошибка обработки целевого ответа: {e}")

    # Подписываемся только на событие ответа
    client.on("Network.responseReceived", lambda event: asyncio.create_task(capture_response(event)))

    # Загружаем страницу
    await page.goto('https://sploitus.com/?query=exploit#exploits')

    await page.waitForSelector('body')
    await asyncio.sleep(5)

    await browser.close()

    # Возвращаем данные о целевом запросе
    return target_request_data

def scan_ports(host, port_range=(1, 65535)):
    open_ports = []
    try:
        for port in range(port_range[0], port_range[1] + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
    except Exception as e:
        print(f"Ошибка сканирования портов: {e}")
    return open_ports


def check_vulnerabilities(host, ports):
    vulnerabilities = []

    for port in ports:
        if port == 22:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "SSH Weak Key Exchange",
                "exploit": "PoC1",
                "description": "The SSH server is using a weak key exchange algorithm, making it susceptible to attacks.",
                "recommendation": "Update your SSH configuration to use stronger key exchange algorithms such as ECDH."
            })

        elif port == 80:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "HTTP Header Injection",
                "exploit": "PoC2",
                "description": "The HTTP server is vulnerable to header injection attacks.",
                "recommendation": "Validate and sanitize all user input in HTTP headers."
            })

        elif port == 443:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "SSL/TLS Insecure Cipher Suite",
                "exploit": "PoC3",
                "description": "The server supports insecure SSL/TLS cipher suites, which could allow data interception.",
                "recommendation": "Disable weak cipher suites in the SSL/TLS configuration."
            })

        elif port == 21:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "Anonymous FTP Access",
                "exploit": "PoC4",
                "description": "The FTP server allows anonymous access, potentially exposing sensitive data.",
                "recommendation": "Disable anonymous access and enforce user authentication for FTP connections."
            })

        elif port == 3306:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "MySQL Default Configuration",
                "exploit": "PoC5",
                "description": "The MySQL server might be running with default configurations, making it susceptible to SQL injection.",
                "recommendation": "Harden the MySQL configuration and implement proper user access controls."
            })

        elif port == 3389:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "RDP Brute Force Vulnerability",
                "exploit": "PoC6",
                "description": "The RDP server is exposed to brute force attacks.",
                "recommendation": "Enable network-level authentication (NLA) and use strong, complex passwords."
            })

        elif port == 6379:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "Redis Unauthorized Access",
                "exploit": "PoC7",
                "description": "The Redis instance is open to unauthorized access.",
                "recommendation": "Restrict access to the Redis server and secure it with authentication."
            })

        else:
            vulnerabilities.append({
                "port": port,
                "vulnerability": "Unknown",
                "description": f"No known vulnerabilities detected for port {port}.",
                "recommendation": "Monitor traffic and ensure the service running on this port is up-to-date."
            })

    return vulnerabilities
