import aiohttp
from cfg.base import cfg


class Service:

    @staticmethod
    async def history(chat_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{cfg.url}/vulnerabilities/{chat_id}") as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        return {"error": f"Failed to fetch data, status code {response.status}"}
        except Exception as e:
            print(f"Error occurred while fetching vulnerabilities: {e}")
            return {"error": str(e)}

    @staticmethod
    async def exp_or_poc(name):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{cfg.url}/data/{name}") as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        return {"error": f"Failed to fetch data, status code {response.status}"}
        except Exception as e:
            print(f"Error occurred while fetching vulnerabilities: {e}")
            return {"error": str(e)}

    @staticmethod
    async def scan(ip_or_domain, chat_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{cfg.url}/scan", json={
                                    "url": ip_or_domain,
                                    "user_id": chat_id}) as response:
                    print(response.status)
                    if response.status == 200:
                        result = await response.json()
                        print(result)
                        return result
                    elif response.status == 400:
                        return {"error": "Bad request. Please check the input and try again."}
                    else:
                        return {"error": f"Failed to fetch data, status code {response.status}"}
        except Exception as e:
            print(f"Error occurred while fetching vulnerabilities: {e}")
            return {"error": str(e)}

