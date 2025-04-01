from bridgepy.card import Card
from bridgepy.game import Game
from bridgepy.player import PlayerId
from dataclasses import dataclass
import numpy as np
from typing import Literal, Type, TypeVar

from bridgebot.dataencoder import BidEncoder, CardEncoder


ObservationType = TypeVar("ObservationType", bound = "Observation")

@dataclass
class Observation:
    player_turn: int
    player_hand: np.ndarray[tuple[Literal[52]], np.dtype[np.int8]]
    bid_history: np.ndarray[tuple[Literal[210]], np.dtype[np.int8]]
    game_bid_ready: int
    partner_card: int
    partner: int
    trick_history: np.ndarray[tuple[Literal[104]], np.dtype[np.int8]]

    @classmethod
    def build(cls: Type[ObservationType], game: Game, player_id: PlayerId | None) -> ObservationType:
        player_turn = Observation.__encode_player_turn(game, player_id)
        player_hand = Observation.__encode_player_hand(game, player_id)
        bid_history = Observation.__encode_bid_history(game)
        game_bid_ready = Observation.__encode_game_bid_ready(game)
        partner_card = Observation.__encode_partner_card(game)
        partner = Observation.__encode_partner(game)
        trick_history = Observation.__encode_trick_history(game)

        return cls(
            player_turn = player_turn,
            player_hand = player_hand,
            bid_history = bid_history,
            game_bid_ready = game_bid_ready,
            partner_card = partner_card,
            partner = partner,
            trick_history = trick_history,
        )
    
    @staticmethod
    def __encode_player_turn(game: Game, player_id: PlayerId | None) -> int:
        """
        0-na, 1-player 1, 2-player 2, 3-player 3, 4-player 4
        """
        if player_id is None:
            return 0
        return Observation.__encode_player_id(game, player_id)
    
    @staticmethod
    def __encode_player_hand(game: Game, player_id: PlayerId | None) -> np.ndarray[tuple[Literal[52]], np.dtype[np.int8]]:
        """
        one-hot encoding list of size 52 where 0-card not on hand, 1-card on hand
        """
        if player_id is None:
            player_hand: list[Card] = []
        else:
            player_hand: list[Card] = game._Game__find_player_hand(player_id).cards
        one_hot_player_hand = np.zeros(52, dtype=np.int8)
        for card in player_hand:
            one_hot_player_hand[CardEncoder.encode(card)] = 1
        return one_hot_player_hand
    
    @staticmethod
    def __encode_bid_history(game: Game) -> np.ndarray[tuple[Literal[210]], np.dtype[np.int8]]:
        """
        a list of 105 bids, each bid is labeled as [player, bid] where
        player is 0-na, 1-player 1, 2-player 2, 3- player 3, 4-player 4 and
        bid is 0-na, 1-pass, 2-1C, 3-1D, 4-1H, 5-1S, 6-1NT, 7-2C, 8-2D, 9-2H, 10-2S, 11-2NT, ..., 36-7NT
        """
        bid_history = np.zeros(210, np.int8)
        actual_bid_history = np.array([(
            Observation.__encode_player_id(game, player_bid.player_id),
            BidEncoder.encode(player_bid.bid) + 1,
        ) for player_bid in game.bids]).flatten()
        bid_history[:len(actual_bid_history)] = actual_bid_history
        return bid_history
    
    @staticmethod
    def __encode_game_bid_ready(game: Game) -> int:
        """
        0-game bid not ready, 1-game bid ready
        """
        return 1 if game.game_bid_ready() else 0
    
    @staticmethod
    def __encode_partner_card(game: Game) -> int:
        """
        0-partner not chosen, 1-2C, 2-2D, 3-2H, 4-2S, 5-3C, 6-3D, 7-3H, 8-3S,..., 52-AS
        """
        if game.partner is None:
            return 0
        return CardEncoder.encode(game.partner) + 1

    @staticmethod
    def __encode_partner(game: Game) -> int:
        """
        0-partner not revealed, 1-player 1, 2-player 2, 3-player 3, 4-player 4
        """
        if game.partner_player_id is None:
            return 0
        return Observation.__encode_player_id(game, game.partner_player_id)
    
    @staticmethod
    def __encode_trick_history(game: Game) -> np.ndarray[tuple[Literal[104]], np.dtype[np.int8]]:
        """
        a list of 52 tricks, each trick is labeled as [player, trick] where
        player is 0-na, 1-player 1, 2-player 2, 3-player 3, 4-player 4 and
        trick is 0-na, 1-2C, 2-2D, 3-2H, 4-2S, 5-3C, 6-3D, 7-3H, 8-3S,..., 52-AS
        """
        trick_history = np.zeros(104, np.int8)
        actual_trick_history = np.array([(
            Observation.__encode_player_id(game, player_trick.player_id),
            CardEncoder.encode(player_trick.trick) + 1,
        ) for game_trick in game.tricks for player_trick in game_trick.player_tricks]).flatten()
        trick_history[:len(actual_trick_history)] = actual_trick_history
        return trick_history
    
    @staticmethod
    def __encode_player_id(game: Game, player_id: PlayerId) -> int:
        """
        1-player 1, 2-player 2, 3-player 3, 4-player 4
        """
        return game.player_ids.index(player_id) + 1
