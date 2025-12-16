import random
import numpy as np
from typing import Tuple

class Card:
    def __init__(self, color: str, value: str):
        self.color = color
        self.value = value
    def __repr__(self):
        return f"{self.color}{self.value}"

class Deck:
    def __init__(self):
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
        self.cards = [Card(c, v) for c in colors for v in values] * 2
        for _ in range(4):
            self.cards.append(Card('Wild', 'Wild'))
            self.cards.append(Card('Wild', 'Draw Four'))
        random.shuffle(self.cards)
    def draw(self, count: int = 1) -> list:
        drawn_cards = []
        for _ in range(count):
            if not self.cards:
                # Assuming discard_pile is managed externally, this call is problematic within the class
                # For this environment, we need to pass the discard pile to the shuffle function
                # The environment manages the discard pile, so the method signature needs adjustment
                # For now, let's assume the environment handles reshuffling before calling draw if empty
                break # Stop drawing if deck runs out
            drawn_cards.append(self.cards.pop())
        return drawn_cards
    def shuffle_discard(self, discard_pile: list) -> None:
        if not self.cards:
            top_card = discard_pile.pop()
            self.cards = discard_pile
            random.shuffle(self.cards)
            discard_pile.clear()
            discard_pile.append(top_card)

class UnoEnvironment:
    def __init__(self, num_players: int = 2):
        self.num_players = num_players
        self.deck = Deck()
        self.players = [[] for _ in range(num_players)]
        self.discard_pile = []
        self.current_player = 0
        self.game_direction = 1 # 1 for clockwise, -1 for anti-clockwise
        self.game_over = False
        self._deal_initial_cards()
        self._place_starting_card()
        self.current_color = self.discard_pile[-1].color if self.discard_pile[-1].color != 'Wild' else None

    def _deal_initial_cards(self) -> None:
        for i in range(self.num_players):
            self.players[i].extend(self.deck.draw(7))

    def _place_starting_card(self) -> None:
        card = self.deck.draw()[0]
        while card.color == "Wild":
            self.deck.cards.insert(0, card)
            card = self.deck.draw()[0]
        self.discard_pile.append(card)

    def get_legal_actions(self, player_id: str):
        """
        Returns indices of playable cards in hand, or ['draw'] if none
        :param player_id:
        :return:
        """
        hand = self.players[player_id]
        top_card = self.discard_pile[-1]
        legal_actions = []
        for i, card in enumerate(hand):
            condition_1 = (card.color == 'Wild')
            condition_2 = (card.color == top_card.color)
            condition_3 = (card.value == top_card.value)
            condition_4 = (self.current_color and card.color == self.current_color)
            if condition_1 or condition_2 or condition_3 or condition_4:
                legal_actions.append(i)
        if not legal_actions:
            legal_actions.append('draw')
        return legal_actions

    def _apply_special_card_effect(self, card: Card) -> None:
        if card.value == 'Skip':
            self.current_player = (self.current_player + self.game_direction) % self.num_players
        elif card.value == 'Reverse':
            self.game_direction *= -1
        elif card.value == 'Draw Two':
            next_player = (self.current_player + self.game_direction) % self.num_players
            self.players[next_player].extend(self.deck.draw(2))
        elif card.value == 'Draw Four':
            # Wild Draw Four requires color to be called, handled in step logic
            next_player = (self.current_player + self.game_direction) % self.num_players
            self.players[next_player].extend(self.deck.draw(4))

    def step(self, player_id: str, action: str, call_color: str = None, penalty_drawing: float = 0.2,
             reward_playing: float = 0.5, major_reward_winning: float = 10):
        """

        :param player_id:
        :param action:
        :param call_color:
        :param penalty_drawing: Small penalty for drawing
        :param reward_playing: Reward for playing a card
        :param major_reward_winning: Major reward for winning
        :return:
        """
        reward = 0

        if action == 'draw':
            drawn_cards = self.deck.draw(1)
            self.players[player_id].extend(drawn_cards)
            reward -= penalty_drawing
        else:
            card_index = action
            played_card = self.players[player_id].pop(card_index)
            self.discard_pile.append(played_card)

            if played_card.color == 'Wild':
                self.current_color = call_color if call_color else random.choice(['Red', 'Green', 'Blue', 'Yellow'])
            else:
                self.current_color = played_card.color
            self._apply_special_card_effect(played_card)
            reward += reward_playing

        if len(self.players[player_id])==0:
            self.game_over = True
            reward += major_reward_winning

        self.current_player = (self.current_player + self.game_direction) % self.num_players
        next_state = self.get_state(player_id)
        return next_state, reward, self.game_over

    def get_state(self, player_id):
        """
        Needs to be a consistent, fixed size representation for RL - this is a simplistic implementation
        :param player_id:
        :return:
        """
        state = {
            'player_hand_size': len(self.players[player_id]),
            'top_card': self.discard_pile[-1],
            'current_color': self.current_color,
            'opponent_hand_sizes': [len(h) for i, h in enumerate(self.players) if i != player_id],
        }
        # print(f"State for {player_id}:")
        # print(state)
        return state

def simple_opponent_play(env, player_id):
    """
    Simple rule-based AI Opponent
    :param env:
    :param player_id:
    :return:
    """
    legal_actions = env.get_legal_actions(player_id)
    if 'draw' in legal_actions and len(legal_actions)==1:
        return 'draw', None
    else:
        for action in legal_actions:
            if action != 'draw':
                card = env.players[player_id][action]
                call_color = None
                if card.color == 'Wild':
                    colors = [c.color for c in env.players[player_id] if c.color != 'Wild']
                    if colors:
                        call_color = max(set(colors), key=colors.count)
                    else:
                        call_color = random.choice(['Red', 'Green', 'Blue', 'Yellow'])
                return action, call_color
    return 'draw', None

class QLearningAgent:
    """
    Q-Learning Agent stub (the runner will use this interface, but RL logic is complex)
    """
    def __init__(self):
        pass

    def choose_action(self, state, legal_actions):
        return random.choice(legal_actions) if 'draw' in legal_actions else legal_actions[0]

    def learn(self, state, action, reward, next_state):
        pass


