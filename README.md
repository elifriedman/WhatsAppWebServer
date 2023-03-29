# WhatsAppWebServer
A simple flask webserver for controlling whatsapp web


`pip install -r requirements.txt`

```
python -m whatsapper.server
```

```python
from whatsapper.client import WhatsappAPI

api = WhatsappAPI("localhost:5000")
api.open_browser()
api.number("580010001")
api.write("hey there")
api.send()
```
