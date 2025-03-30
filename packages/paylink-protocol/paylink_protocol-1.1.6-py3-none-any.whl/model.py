from dataclasses import dataclass
from enum import Enum

class PurchaseType(Enum):
    HOLDING = 0
    PURCHASE_WITH_ETH = 1
    PURCHASE_WITH_TOKENS = 2

@dataclass
class PurchaseItem:
    txHash: str
    blockNumber: int
    appId: int
    userId: int
    userWalletAddress: str
    purchaseType: PurchaseType
    purchaseTokenAddress: str
    purchaseAmount: int
    expirationTimestamp: int

    def __str__(self):
        return (
            f"txHash: {self.txHash}\n"
            f"blockNumber: {self.blockNumber}\n"
            f"appId: {self.appId}\n"
            f"userId: {self.userId}\n"
            f"userWalletAddress: {self.userWalletAddress}\n"
            f"purchaseType: {self.purchaseType.name}\n"
            f"purchaseTokenAddress: {self.purchaseTokenAddress}\n"
            f"purchaseAmount: {self.purchaseAmount}\n"
            f"expirationTimestamp: {self.expirationTimestamp}"
        )
