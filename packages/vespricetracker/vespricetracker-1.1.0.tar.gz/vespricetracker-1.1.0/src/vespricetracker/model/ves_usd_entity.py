from decimal import Decimal


class VESUSDEntity:
    def __init__(
        self,
        entity_id: int,
        partition: str,
        bcv_price: Decimal,
        binance_price: Decimal,
        misalignment: Decimal,
    ) -> None:
        self.entity_id = entity_id
        self.partition = partition
        self.bcv_price = bcv_price
        self.binance_price = binance_price
        self.misalignment = misalignment

    def to_dict(self) -> dict:
        return {
            "id": self.entity_id,
            "partition": self.partition,
            "bcv_price": self.bcv_price,
            "binance_price": self.binance_price,
            "misalignment": self.misalignment,
        }
