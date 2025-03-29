
# AioShowBusiness File Upload

This script demonstrates how to upload a file using the ClientShowBusinessTg client.

## Usage

```python
import asyncio
from ClientShowBusinessTg import ClientShowBusinessTg

client = ClientShowBusinessTg()

asyncio.run(client.upload_archive(file_path="file.zip", user_id=9999999, token="token"))
```

## Requirements
- 2 requests per second rate limit
- Maximum file size: **20MB**
- Supported formats: **.ZIP** / **.RAR**

## Installation
Ensure you have the necessary dependencies installed:
```
pip install ClientShowBusinessTg
```

## Notes
- Replace `file.zip` with your desired file.
- Update `user_id` and `token` with valid values for authentication.
