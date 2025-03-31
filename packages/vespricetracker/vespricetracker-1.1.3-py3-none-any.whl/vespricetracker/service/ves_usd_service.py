from __future__ import annotations

from boto3.dynamodb.conditions import Key

from vespricetracker.model.ves_usd_entity import VESUSDEntity


class VESUSDService:
    def __init__(self, table) -> None:  # noqa: ANN001
        self.table = table

    def create(self, ves_usd_entity: VESUSDEntity) -> None:
        self.table.put_item(Item=ves_usd_entity.to_dict())

    def get_latest(self) -> VESUSDEntity | None:
        response = self.table.query(
            KeyConditionExpression=Key("partition").eq("usd")
            & Key("id").gt(0),
            ScanIndexForward=False,  # Sort descending (newest first)
            Limit=1,
        )
        item = response["Items"][0] if response["Items"] else None

        if item:
            return VESUSDEntity(
                entity_id=item.get("id"),
                partition=item.get("partition"),
                bcv_price=item.get("bcv_price"),
                binance_price=item.get("binance_price"),
                misalignment=item.get("misalignment"),
            )

        return None
