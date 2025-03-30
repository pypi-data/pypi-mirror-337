import asyncio
import time
from web3 import Web3, AsyncWeb3, WebSocketProvider
from eth_abi.abi import decode
from hexbytes import HexBytes
from typing import Callable, Awaitable, Dict, Any, List

from model import *
from resources import *
from util import *

class PurchaseManager:
    def __init__(self, appId: int, encryptionKey: int, websocketUrl: str = defaultWebsocket, rpcUrl: str = defaultRpc, debug: bool = False):
        self.appId = appId
        self.encryptionKey = encryptionKey
        self.websocketUrl = websocketUrl
        self.rpcUrl = rpcUrl
        self.debug = debug
        self.contract_address = Web3.to_checksum_address(routerAddress)
        self.topic_hash = purchaseTopicHash
        self.running = False

    def createPayLink(self, userId : int):
        return payLinkUrl.format(data=encodePayLinkData(self.appId, encryptUserId(userId)))
    
    def isPurchaseValid(self, purchase: PurchaseItem) -> bool:
        current_time = int(time.time())
        return current_time < purchase.expirationTimestamp
    
    async def getAllPurchases(self, ignoreExpiredPurchases: bool = False) -> List[PurchaseItem]:
        return await self.__getPurchases__([
            self.topic_hash,
            "0x" + hex(self.appId).lower().replace("0x", "").rjust(64, "0"),
            None,
            None
            ], ignoreExpiredPurchases)
    
    async def getPurchasesByUserId(self, userId: str, ignoreExpiredPurchases: bool = False) -> List[PurchaseItem]:
        userId = encryptUserId(userId, self.encryptionKey)
        return await self.__getPurchases__([
            self.topic_hash,
            "0x" + hex(self.appId).lower().replace("0x", "").rjust(64, "0"),
            "0x" + hex(userId).lower().replace("0x", "").rjust(64, "0"),
            None
            ], ignoreExpiredPurchases)
    
    async def getPurchasesByUserWalletAddress(self, userWalletAddress: str, ignoreExpiredPurchases: bool = False) -> List[PurchaseItem]:
        return await self.__getPurchases__([
            self.topic_hash,
            "0x" + hex(self.appId).lower().replace("0x", "").rjust(64, "0"),
            None,
            "0x" + userWalletAddress.lower().replace("0x", "").rjust(64, "0")
            ], ignoreExpiredPurchases)
    
    async def __getPurchases__(self, topics: list, ignoreExpiredPurchases: bool) -> List[PurchaseItem]:
        if self.debug:
            print(f"Fetching logs for topics {topics} ...")

        filter_params = {
            "address": self.contract_address,
            "topics": topics,
            "fromBlock": "earliest",
            "toBlock": "latest"
        }

        purchases = []
        logs = Web3(Web3.HTTPProvider(self.rpcUrl)).eth.get_logs(filter_params)
        for payload in logs:
            item = self.__decodePurchase__(payload)
            if ignoreExpiredPurchases:
                purchases.append(item)
            elif self.isPurchaseValid(item):
                purchases.append(item)

        return purchases

    async def listenForPurchases(self, callback: Callable[[PurchaseItem], Awaitable[None]]):
        self.running = True
        while self.running:
            try:
                async with AsyncWeb3(WebSocketProvider(self.websocketUrl)) as web3:
                    filter_params = {
                        "address": self.contract_address,
                        "topics": [self.topic_hash],
                    }
                    subscription_id = await web3.eth.subscribe("logs", filter_params)
                    if self.debug:
                        print(f"Subscribing to purchase events: {subscription_id}")

                    async for payload in web3.socket.process_subscriptions():
                        if "result" not in payload:
                            continue
                        item = self.__decodePurchase__(payload["result"])
                        await callback(item)

            except Exception as e:
                if self.debug:
                    print(f"[ERROR] WebSocket error: {e}")
                    print("Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    def __decodePurchase__(self, result: Dict[str, Any]) -> PurchaseItem:
        txHash = "0x" + result["transactionHash"].hex()
        blockNumber = result["blockNumber"]

        topics = result["topics"]
        appId = int.from_bytes(topics[1], "big")
        userId = decryptUserId(int.from_bytes(topics[2], "big"), self.encryptionKey)
        userWalletAddress = decode(["address"], topics[3])[0]

        data = HexBytes(result["data"])
        decodedData = decode(["uint256", "address", "uint256", "uint256"], data)
        purchaseType = decodedData[0]
        purchaseTokenAddress = decodedData[1]
        purchaseAmount = decodedData[2]
        expirationTimestamp = decodedData[3]

        return PurchaseItem(
            txHash=txHash,
            blockNumber=blockNumber,
            appId=appId,
            userId=userId,
            userWalletAddress=userWalletAddress,
            purchaseType=PurchaseType(purchaseType),
            purchaseTokenAddress=purchaseTokenAddress,
            purchaseAmount=purchaseAmount,
            expirationTimestamp=expirationTimestamp
        )
