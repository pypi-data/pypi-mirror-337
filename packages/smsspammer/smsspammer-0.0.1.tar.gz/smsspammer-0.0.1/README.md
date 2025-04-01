# SMS Spammer

> [!WARNING]
> このライブラリは研究目的で作成されました。  
> このライブラリを使用したことによって生じた損害を nennneko5787 は負いません。

> [!NOTE]
> Sorry, This library support Japanese phone numbers only.

## 使い方

本ライブラリの関数はは非同期関数内でのみ動作します。

```python
import asyncio

from smsspammer import SMSSpammer

sms = SMSSpammer()


async def main():
    print(await sms.spam("090-1234-5678"))  # Send SMS
    print(await sms.call("090-1234-5678"))  # Call


asyncio.run(main())

```
