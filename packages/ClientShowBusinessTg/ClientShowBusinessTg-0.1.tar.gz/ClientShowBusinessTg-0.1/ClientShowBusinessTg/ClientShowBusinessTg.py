import httpx

class ClientShowBusinessTg:

    def __init__(self):

        self.url = "http://showbusiness.top/upload_archive"

    async def upload_archive(self, file_path: str, user_id: int, token: str):

        """2 requests per second, the maximum file size is 20MB, .ZIP/.RAR"""

        try:

            async with httpx.AsyncClient(timeout=30) as client:

                with open(file_path, "rb") as f:

                    files = {"file": (file_path, f, "application/zip")}
                    params = {"user_id": user_id, "token": token}

                    response = await client.post(self.url, files=files, params=params)

            return response.status_code

        except Exception as e:

            print(f"Error: {e}")