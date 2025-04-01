from abc import ABC, abstractmethod
from bridgepy.bid import Bid
from bridgepy.card import Card, Rank, Suit, _rank_order, _suit_order
from typing import Generic, TypeVar


T = TypeVar("T")

class DataEncoder(ABC, Generic[T]):

    @staticmethod
    @abstractmethod
    def encode(data: T) -> int:
        pass

    @staticmethod
    @abstractmethod
    def decode(value: int) -> T:
        pass

class BidEncoder(DataEncoder[Bid | None]):
    """
    0-pass, 1-1C, 2-1D, 3-1H, 4-1S, 5-1NT, 6-2C, 7-2D, 8-2H, 9-2S, 10-2NT, ..., 35-7NT
    """

    @staticmethod
    def encode(data: Bid | None) -> int:
        if data is None:
            value: int = 0
        else:
            value: int = (data.level - 1) * 5 + _suit_order[data.suit] + 1 if data.suit is not None else data.level * 5
        return value

    @staticmethod
    def decode(value: int) -> Bid | None:
        if value == 0:
            return None
        bid_index: int = value - 1
        level: int = bid_index // 5 + 1
        suit_index: int = bid_index % 5
        suit: Suit | None = list(Suit)[suit_index] if suit_index < 4 else None
        return Bid(level, suit)

class CardEncoder(DataEncoder[Card]):
    """
    0-1C, 1-1D, 2-1H, 3-1S, 4-2C, 5-2D, 6-2H, 7-2S,..., 51-AS
    """

    @staticmethod
    def encode(data: Card) -> int:
        value: int = _rank_order[data.rank] * 4 + _suit_order[data.suit]
        return value

    @staticmethod
    def decode(value: int) -> Card:
        rank: Rank = list(Rank)[value // 4]
        suit: Suit = list(Suit)[value % 4]
        return Card(rank, suit)
