from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from a2_support import *
import math

# Replace these <strings> with your name, student number and email address.
__author__ = "Harold Shaw, 47020665"
__email__ = "s4702066@student.uq.edu.au"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackbaord changelog.
__version__ = 2.0

# Implement your classes here.
class PokemonStats(object):
    """A class that models a Pokemon's statistics."""
    def __init__(self, stats: Tuple[float, int, int, int]) -> None:
        """Constructs a Pokemon's statistics.

        Parameters:
            stats (Tuple[float, int, int, int]): A Pokemon's hit chance,
                    max health, attack and defense respectively.
        Returns:
            (None)
        """
        self._stats = stats
        self._hit_chance = self._stats[STAT_HIT_CHANCE]
        self._max_health = self._stats[STAT_MAX_HEALTH]
        self._attack = self._stats[STAT_ATTACK]
        self._defense = self._stats[STAT_DEFENSE]

    def level_up(self) -> None:
        """(None) Increases a Pokemon's statistics by 5%, rounding them down,
        with the exception of hit chance, which is set to 1."""
        self._hit_chance = 1
        self._max_health = math.floor(self._max_health * LEVEL_UP_STAT_GROWTH)
        self._attack = math.floor(self._attack * LEVEL_UP_STAT_GROWTH)
        self._defense = math.floor(self._defense * LEVEL_UP_STAT_GROWTH)
        return None

    def get_hit_chance(self) -> float:
        """(float) Returns the Pokemon's hit chance."""
        return self._hit_chance

    def get_max_health(self) -> int:
        """(int) Returns the Pokemon's max health."""
        return self._max_health

    def get_attack(self) -> int:
        """(int) Returns the Pokemon's attack."""
        return self._attack

    def get_defense(self) -> int:
        """(int) Returns the Pokemon's defense."""
        return self._defense

    def apply_modifier(self, modifier: Tuple[float, int, int, int]) \
                                -> PokemonStats:
        """Modifies the Pokemon's statistics.

        Parameters:
            modifier(Tuple[float, int, int, int]): Values by which PokemonStats
                    will be modified.

        Returns:
            (PokemonStats): A PokemonStats class with modified statistics.
        """
        hit_chance = self.get_hit_chance() + modifier[STAT_HIT_CHANCE]
        max_health = self.get_max_health() + modifier[STAT_MAX_HEALTH]
        attack = self.get_attack() + modifier[STAT_ATTACK]
        defense = self.get_defense() + modifier[STAT_DEFENSE]
        return PokemonStats((hit_chance, max_health, attack, defense))

    def __str__(self) -> str:
        """(str) Returns a string representation of the PokemonStats class."""
        return f'PokemonStats({self._stats})'

    def __repr__(self) -> str:
        """(str) Returns a string representation of the PokemonStats class."""
        return str(self)


class Pokemon(object):
    """A class representing a Pokemon."""
    def __init__(self, name: str,
                 stats: PokemonStats,
                 element_type: str,
                 moves: List[ForwardRef('Move')],
                 level: int = 1) -> None:
        """Constructs a Pokemon.

        Parameters:
            name (str): The Pokemon's name.
            stats (PokemonStats): The Pokemon's stats.
            element_type (str): The Pokemon's element type.
            moves (List[ForwardRef('Move')]): The moves the Pokemon has learnt.
            level (int = 1): The Pokemon's level.

        Returns:
            (None)
        """
        self._name = name
        self.stats = stats
        self._modified_stats = stats
        self._element_type = element_type
        self.moves = []
        for move in moves:
            self.learn_move(move)
        self._level = level
        self._health = self.get_max_health()
        self._experience = math.floor(self._level ** 3)
        self._current_stat_modifiers = []

    def get_name(self) -> str:
        """(str) Returns the Pokemon's name."""
        return self._name

    def get_health(self) -> int:
        """(int) Returns the Pokemon's health."""
        return self._health

    def get_max_health(self) -> int:
        """(int) Returns the Pokemon's max health."""
        return self.stats.get_max_health()

    def get_element_type(self) -> str:
        """(str) Returns the Pokemon's element type."""
        return self._element_type

    def get_remaining_move_uses(self, move: Move) -> int:
        """Returns the number of moves remaining for specified move. If the
        Pokemon doesn't know the move, there are 0 remaining moves for that
        move.

        Parameters:
            move (Move): A move that a Pokemon can learn.

        Returns:
            (int): The remaining uses of specified move. If not learnt, will
                    return 0.
        """
        for move_info in self.moves:
            if move_info[0] == move:
                remaining_move_uses = move_info[1]
                return remaining_move_uses
        return 0

    def get_level(self) -> int:
        """(int) Returns the Pokemon's level."""
        return self._level

    def get_experience(self) -> int:
        """(int) Returns the Pokemon's experience."""
        return self._experience

    def get_next_level_experience_requirement(self) -> int:
        """(int) Returns the experience required for the Pokemon to
        level up."""
        next_level = self.get_level() + 1
        experience_requirement = math.floor(next_level ** 3)
        return experience_requirement

    def get_move_info(self) -> List[Tuple[Move, int]]:
        """(List[Tuple[Move, int]]) Returns Pokemon's known moves and
        remaining uses."""
        sorted_moves = sorted(self.moves,
                              key = lambda info: info[0].get_name())
        return sorted_moves

    def has_fainted(self) -> bool:
        """(bool) Returns whether Pokemon has fainted."""
        return self._health == 0

    def modify_health(self, change: int) -> None:
        """Modifies the Pokemon's health by amount specified. The result must
        be between 0 and the Pokemon's max health.

        Parameters:
            change (int): The amount by which the Pokemon's health is to be
                            modified.
        Returns:
            (None)
        """
        self._health = self.get_health() + change
        modified_max_health = self.get_stats().get_max_health()

        if self.get_health() > modified_max_health:
            self._health = modified_max_health
        if self.get_health() < 0:
            self._health = 0
        return None

    def gain_experience(self, experience: int) -> None:
        """Increases the Pokemon's experience by the specified amount. If the
        resulting experience is of an appropriate value, the Pokemon levels up.

        Parameters:
            experience (int): The amount by which the Pokemon's experience is
                                to be increased.
        Returns:
            (None)
        """
        self._experience += experience
        if self._experience >= self.get_next_level_experience_requirement():
            self.level_up()
        return None

    def level_up(self) -> None:
        """Increases the Pokemon's level, which causes the Pokemon's stats to
        grow and it's health to increase by the same amount that it's max
        health is increased.

        Returns:
            (None)
        """
        self._level += 1
        initial_max_health = self.get_stats().get_max_health()
        self.stats.level_up()
        new_max_health = self.get_stats().get_max_health()

        difference = new_max_health - initial_max_health
        self._health += difference
        return None

    def experience_on_death(self) -> int:
        """(int) Returns the amount of experience to be given to the opposing,
        victorious player if Pokemon instance faints."""
        experience_on_death = math.floor(200 * self.get_level() / 7)
        return experience_on_death

    def can_learn_move(self, move: Move) -> bool:
        """Returns whether the Pokemon can learn the specified move. A Pokemon
        can't learn a move if it has already learnt 4 moves and/or it has
        already learnt the specified move.

        Parameters:
            move (Move): A Pokemon move.

        Returns:
            (bool): True iff the Pokemon can learn the specified move.
        """
        if len(self.moves) < MAXIMUM_MOVE_SLOTS:
            for move_info in self.moves:
                if move_info[0] == move:
                    return False
            return True
        return False

    def learn_move(self, move: Move) -> None:
        """The Pokemon learns the specified move.

        Parameters:
            move (Move): A Pokemon move.

        Returns:
            (None)
        """
        info = move, move.get_max_uses()
        self.moves.append((info))
        self.moves
        return None

    def forget_move(self, move: Move) -> None:
        """If the Pokemon has learnt the supplied move, it forgets the move.

        Parameters:
            move (Move): A Pokemon move.

        Returns:
            (None)
        """
        for move_info in self.moves:
            if move_info[0] == move:
                move_index = self.moves.index(move_info)
                self.moves.pop(move_index)
        return None

    def has_moves_left(self) -> bool:
        """(bool) Returns true iff the Pokemon has any moves left."""
        return len(self.moves) != 0

    def reduce_move_count(self, move: Move) -> None:
        """Decreases the move count of the specified move, assuming the Pokemon
        has learnt the move.

        Parameters:
            move (Move): A Pokemon move.

        Returns:
            (None)
        """
        count = 0
        for move_info in self.moves:
            if move_info[0] == move:
                move_index = count
                self.moves[move_index] = (move, move_info[1] - 1)
                if (move_info[1] - 1) == 0:
                    self.forget_move(move)
            else:
                count += 1
        return None

    def add_stat_modifier(self,
                          modifier: Tuple[float, int, int, int],
                          rounds: int) -> None:
        """Modifies the stats of the Pokemon by the specified amounts for the
        number of rounds specified.

        Parameters:
            modifier (Tuple[float, int, int, int]): The values by which the
                                Pokemon's stats will be modified.
            rounds (int): The number of rounds for which the Pokemon's stats
                            will be modified for.

        Returns:
            (None)
        """
        self._current_stat_modifiers.append((modifier, rounds))
        self.get_stats()
        return None

    def get_stats(self) -> PokemonStats:
        """(PokemonStats) Returns the Pokemon's stats, with all stats
        modifications applied."""
        self._modified_stats = self.stats
        for mod_info in self._current_stat_modifiers:
            mod = mod_info[0]
            self._modified_stats = self._modified_stats.apply_modifier(mod)

        if self._modified_stats.get_max_health() < self._health:
            self._health = self._modified_stats.get_max_health()
        return self._modified_stats

    def post_round_actions(self) -> None:
        """(None) Updates stat modifiers by decreasing the number of rounds
        remaining for which they are in effect."""
        for mod_info in self._current_stat_modifiers:
            index_of_mod_info = self._current_stat_modifiers.index(mod_info)
            new_mod_info = (mod_info[0], mod_info[1] - 1)
            self._current_stat_modifiers[index_of_mod_info] = new_mod_info
            if (mod_info[1] - 1) == 0:
                self._current_stat_modifiers.pop(index_of_mod_info)
        self.get_stats()
        self.modify_health(0)
        return None

    def rest(self) -> None:
        """(None) Returns Pokemon to it's max health, removes it's stat
        modifiers and sets all move uses to their maximums."""
        self._health = self.get_max_health()
        self._current_stat_modifiers = []
        count = 0
        for move_info in self.moves:
                index_of_move = count
                self.moves[index_of_move] = (move_info[0],
                                             move_info[0].get_max_uses())
                count += 1
        return None

    def __str__(self) -> str:
        """(str) Returns a succinct representation of the Pokemon, specifically
        it's name and it's level."""
        return f'{self._name} (lv{self._level})'

    def __repr__(self) -> str:
        """(str) Returns a string representation of the Pokemon."""
        return str(self)


class Trainer(object):
    """A class that represents a Pokemon Trainer."""
    def __init__(self, name: str) -> None:
        """Constructs a Pokemon Trainer.

        Parameters:
            name (str): The name of the Trainer.

        Returns:
            (None)
        """
        self._name = name
        self._inventory = {}
        self._pokemon_roster = []
        self.current_pokemon = None

    def get_name(self) -> str:
        """(str) Returns the Trainer's name."""
        return self._name

    def get_inventory(self) -> Dict[Item, int]:
        """(Dict[Item, int]) Returns the Trainer's inventory."""
        return self._inventory

    def get_current_pokemon(self) -> Pokemon:
        """(Pokemon) Returns the Trainer's current Pokemon."""
        if self.current_pokemon is None:
            raise NoPokemonException()
        return self.current_pokemon

    def get_all_pokemon(self) -> List[Pokemon]:
        """(List[Pokemon]) Returns all the Trainer's Pokemon."""
        return self._pokemon_roster

    def rest_all_pokemon(self) -> None:
        """(None) Rests all the Trainer's Pokemon."""
        for pokemon in self._pokemon_roster:
            pokemon.rest()
        return None

    def all_pokemon_fainted(self) -> bool:
        """(bool) Returns true iff all the Trainer's Pokemon have fainted."""
        for pokemon in self._pokemon_roster:
            if not pokemon.has_fainted():
                return False
        return True

    def can_add_pokemon(self, pokemon: Pokemon) -> bool:
        """Determines whether specified Pokemon can be added to the
        Trainer's Pokemon roster.

        Parameters:
            pokemon (Pokemon): A Pokemon.

        Returns:
            (bool): True iff the specified Pokemon can be added to the
                        Trainer's roster.
        """
        if len(self._pokemon_roster) < MAXIMUM_POKEMON_ROSTER:
            for rostered_pokemon in self._pokemon_roster:
                if rostered_pokemon == pokemon:
                    return False
            return True
        return False

    def add_pokemon(self, pokemon: Pokemon) -> None:
        """Adds the specified Pokemon to the Trainer's roster.

        Parameters:
            pokemon (Pokemon): A Pokemon.

        Returns:
            (None)
        """
        if len(self._pokemon_roster) == 0:
            self.current_pokemon = pokemon
        self._pokemon_roster.append(pokemon)
        return None

    def can_switch_pokemon(self, index: int) -> bool:
        """Determines whether current Pokemon can be switched for Pokemon
        at index.

        Parameters:
            index (int): The index of a Pokemon in the Trainer's roster.

        Returns:
            (bool): True iff the Pokemon can be switched.
        """
        test_pokemon = self._pokemon_roster[index]
        if len(self._pokemon_roster) == 0 or \
           len(self._pokemon_roster) <= index:
            return False
        elif test_pokemon == self.current_pokemon:
            return False
        elif test_pokemon.has_fainted():
            return False
        else:
            return True

    def switch_pokemon(self, index: int) -> None:
        """Switches the current Pokemon to the Pokemon at index on the
        Trainer's roster.

        Parameters:
            index (int): The index of a Pokemon in the Trainer's roster.

        Returns:
            (None)
        """
        self.current_pokemon = self._pokemon_roster[index]
        return None

    def add_item(self, item: Item, uses: int) -> None:
        """Adds specified item to the Trainer's inventory, incrementing it's
        uses by the specified number of uses.

        Parameters:
            item (Item): An item to be added to the Trainer's inventory.
            uses (int): The number of uses by which the specified Item's uses
                            will be incremented.

        Returns:
            (None)
        """
        self._inventory[item] = uses
        return None

    def has_item(self, item: Item) -> bool:
        """Determines whether the Trainer has the specified Item in their
        inventory.

        Parameters:
            item (Item): An Item potentionally in the Trainer's inventory.

        Returns:
            (bool): True iff the Trainer has the specified Item in their
            inventory.
        """
        for stored_item in self._inventory:
            if stored_item == item:
                return True
            return False

    def use_item(self, item: Item) -> None:
        """Decrements the number of uses the specified Item has in the
        Trainer's inventory. If the Item's uses become 0, it is removed from
        the Trainer's inventory.

        Parameters:
            item (Item): An Item.

        Returns:
            (None)
        """
        item.decrement_item_count(self)
        return None

    def __str__(self) -> str:
        """Returns a string representation of the Trainer."""
        return f'Trainer(\'{self._name}\')'

    def __repr__(self) -> str:
        """Returns a string representation of the Trainer."""
        return str(self)


class Battle(object):
    """A class that represents a Battle between two Trainers or a Trainer
    and another Trainer whose sole Pokemon is a 'wild' Pokemon."""
    def __init__(self,
                 player: Trainer,
                 enemy: Trainer,
                 is_trainer_battle: bool) -> None:
        """Constructs a Battle between two trainers.

        Parameters:
            player (Trainer): A Pokemon Trainer competing in the Battle.
            enemy (Trainer): A Pokemon Trainer competing in the Battle.
            is_trainer_battle (bool): True iff the Battle is between two
                        trainers, neither of whom have a sole, wild pokemon
                                    rostered.
        Returns:
            (None)
        """
        self._player = player
        self._enemy = enemy
        self._is_trainer_battle = is_trainer_battle
        self.is_battle_over = False
        self.turn = None
        self._action_queue = {}

    def get_turn(self) -> Optional[bool]:
        """(Optional[bool]) Returns whether it is player's or enemy's
        turn, if either."""
        return self.turn

    def get_trainer(self, is_player: bool) -> Trainer:
        """Determines specified Trainer as either the player or the enemy.

        Parameters:
            is_player (bool): True iff the Trainer is the player.

        Returns:
            (Trainer): Either the player or the enemy.
        """
        if is_player == True:
            return self._player
        return self._enemy

    def attempt_end_early(self) -> None:
        """(None) Ends Battle if it is not a Trainer battle."""
        if not self.is_trainer_battle():
            self.is_battle_over = True
        return None

    def is_trainer_battle(self) -> bool:
        """(bool) True iff the Battle is a Trainer Battle."""
        return self._is_trainer_battle

    def is_action_queue_full(self) -> bool:
        """(bool) Returns true iff both Trainers in Battle have an Action
        queued."""
        if len(self._action_queue) != 2:
            return False
        players_queued = list(self._action_queue)
        if (players_queued[0] and not players_queued[1]) or \
           (not players_queued[0] and players_queued[1]):
           return True
        return False

    def is_action_queue_empty(self) -> bool:
        """(bool) Returns true iff both Trainers in Battle have no Actions
        queued."""
        return len(self._action_queue) == 0

    def trainer_has_action_queued(self, is_player: bool) -> bool:
        """Determines whether specified Trainer has an Action queued.

        Parameters:
            is_player (bool): True iff the Trainer is the player.

        Returns:
            (bool): True iff the specified Trainer has an Action queued.
        """
        if self.is_action_queue_full():
            return True
        if self.is_action_queue_empty():
            return False
        player_queued = list(self._action_queue)[0]
        if is_player == player_queued:
            return True
        return False

    def is_ready(self) -> bool:
        """(bool) Returns true iff the next Action is ready to be
        completed."""
        if self.turn is None and self.is_action_queue_full():
                return True
        elif self.turn and self.trainer_has_action_queued(True):
                return True
        elif not self.turn and self.trainer_has_action_queued(False):
                return True
        else:
            return False

    def queue_action(self, action: Action, is_player: bool) -> None:
        """Adds the specified Action to the specified Trainer's queue,
        if it is valid to do so.

        Parameters:
            action (Action): An Action to be performed.
            is_player (bool): True iff the Trainer is the player.

        Returns:
            (None)
        """
        if not self.is_ready() and \
        not self.trainer_has_action_queued(is_player) and \
        action.is_valid(self, is_player):
            self._action_queue[is_player] = action
        return None

    def enact_turn(self) -> Optional[ActionSummary]:
        """(Optional[ActionSummary]) Attempts next queued Action and if
        valid, returns an ActionSummary of its effects."""
        if self.is_action_queue_full():
            action_player = self._action_queue[True]
            action_enemy = self._action_queue[False]
            priority_player = action_player.get_priority()
            priority_enemy = action_enemy.get_priority()

        if self.is_action_queue_full() and \
           (priority_enemy > priority_player and \
           (self.turn or self.turn is None)):
            self.turn = False
            action = self._action_queue.pop(True)
            return action.apply(self, True)
        if self.is_action_queue_full() and \
           (priority_player > priority_enemy and \
           (not self.turn or self.turn is None)):
            self.turn = True
            action = self._action_queue.pop(False)
            return action.apply(self, False)

        player_pokemon = self.get_trainer(self.turn).get_current_pokemon()
        enemy_pokemon = self.get_trainer(not self.turn).get_current_pokemon()
        player_pokemon.post_round_actions()
        enemy_pokemon.post_round_actions()
        self.turn = None
        is_player = list(self._action_queue)[0]
        first_action = self._action_queue.pop(is_player)
        return first_action.apply(self, is_player)

    def is_over(self) -> bool:
        """(bool) True iff the Battle is over."""
        player_fainted = self.get_trainer(True).all_pokemon_fainted()
        enemy_fainted = self.get_trainer(False).all_pokemon_fainted()

        if player_fainted or enemy_fainted:
            self.is_battle_over = True
        return self.is_battle_over


class ActionSummary(object):
    """A class that contains messages regarding actions."""
    def __init__(self, message: Optional[str] = None) -> None:
        """Constructs an ActionSummary with an optional message.

        Parameters:
            message (Optional[str] = None): A message pertaining to an action
                                                and its effect(s).

        Returns:
            (None)
        """
        self._message = message
        self._messages = []
        if self._message is not None:
            self._messages.append(self._message)


    def get_messages(self) -> List[str]:
        """(List[str]): Returns messages of an ActionSummary."""
        return self._messages

    def add_message(self, message: str) -> None:
        """Adds a message to an ActionSummary.

        Parameters:
            message (str): A message pertaining to an action and its effect(s).

        Returns:
            (None)
        """
        self._messages.append(message)
        return None

    def combine(self, summary: ActionSummary) -> None:
        """Combines two ActionSummary classes.

        Parameters:
            summary (ActionSummary): An instance of the ActionSummary class.

        Returns:
            (None)
        """
        if isinstance(summary._message, str):
            self.add_message(summary._message)
        return None


class Action(object):
    """An abstract class that represents any action that uses a turn in the
    game."""
    def get_priority(self) -> int:
        """(int) Returns the Action's priority."""
        return DEFAULT_ACTION_PRIORITY

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        """Determines whether Action is valid for specified Battle and player.

        Parameters:
            battle (Battle): A Battle between two Trainers.
            is_player (bool): True iff the Trainer is the player.

        Returns:
            (bool): True iff the Action is valid.
        """
        return not battle.is_over() and \
        (battle.get_turn() is None or battle.get_turn() == is_player)

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        """Applies the Action to the specified Battle by the specified Trainer.

        Parameters:
            battle (Battle): A Battle between two Trainers.
            is_player (bool): True iff the Trainer is the player.

        Returns:
            (ActionSummary): The effect(s) of the applied Action.
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """(str) Returns a string representation of the Action."""
        return f'Action()'

    def __repr__(self) -> str:
        """(str) Returns a string representation of the Action."""
        return str(self)


class Flee(Action):
    """A class representing the Flee Action, where a Trainer attempts to
    leave a Battle."""
    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        if super().is_valid(battle, is_player):
            trainer = battle.get_trainer(is_player)
            return not trainer.get_current_pokemon().has_fainted()
        return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        if battle.is_trainer_battle():
            return ActionSummary(FLEE_INVALID)
        battle.attempt_end_early()
        return ActionSummary(FLEE_SUCCESS)

    def __str__(self) -> str:
        return f'Flee()'


class SwitchPokemon(Action):
    """A class representing the Action of a Trainer switching Pokemon."""
    def __init__(self, next_pokemon_index: int) -> None:
        """Constructs an instance of a Trainer's desire to SwitchPokemon.

        Parameters:
            next_pokemon_index (int): The index at which the Pokemon to be
            switched is located.

        Returns:
            (None)
        """
        self._next_pokemon_index = next_pokemon_index

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        if super().is_valid(battle, is_player):
            trainer = battle.get_trainer(is_player)
            return trainer.can_switch_pokemon(self._next_pokemon_index)
        return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        trainer = battle.get_trainer(is_player)
        pokemon = trainer.get_current_pokemon()
        current_pokemon_name = pokemon.get_name()
        trainer.switch_pokemon(self._next_pokemon_index)
        next_pokemon_name = trainer.get_current_pokemon().get_name()

        summary = ActionSummary()
        if ((battle.get_turn() == is_player or \
           battle.get_turn() is None) and not \
           pokemon.has_fainted()):
            SWITCH_POKEMON_RETURN = '{}, return!'
            message = SWITCH_POKEMON_RETURN.format(current_pokemon_name)
            summary.add_message(message)
        SWITCHED_POKEMON = '{} switched to {}.'
        summary.add_message(SWITCHED_POKEMON.format(trainer.get_name(),
                            next_pokemon_name))
        return summary

    def __str__(self) -> str:
        return f'SwitchPokemon({self._next_pokemon_index})'


class Item(Action):
    """An abstract class which represents an Item to be used as an Action."""
    def __init__(self, name: str) -> None:
        """Constructs an Item.

        Parameters:
            name (str): The name of the Item.

        Returns:
            (None)
        """
        self.name = name

    def get_name(self) -> str:
        """(str) Returns the name of the Item."""
        return self.name

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        trainer = battle.get_trainer(is_player)
        current_pokemon = trainer.get_current_pokemon()
        if super().is_valid(battle, is_player) and \
             (not current_pokemon.has_fainted() and \
             trainer.has_item(self)):
                return True
        return False

    def decrement_item_count(self, trainer: Trainer) -> None:
        """Decrements the number of Items the specified Trainer has in their
        inventory.

        Parameters:
            trainer (Trainer): The Trainer who has this instance of Item in
                                their inventory.
        Returns:
            (None)
        """
        if not trainer.has_item(self):
            return None
        else:
            trainer._inventory[self] -= 1
        if trainer._inventory[self] <= 0:
            trainer._inventory.pop(self)
        return None


class Pokeball(Item):
    """An Item a Trainer can use to catch another Trainer's 'wild' Pokemon."""
    def __init__(self, name, catch_chance) -> None:
        """Constructs a Pokeball.

        Parameters:
            name: The name of the Pokeball.
            catch_chance: The chance that the Trainer has of catching a
                            'wild' Pokemon.
        Returns:
            (None)
        """
        super().__init__(name)
        self._catch_chance = catch_chance

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        trainer_player = battle.get_trainer(is_player)
        trainer_enemy = battle.get_trainer(not is_player)
        wild_pokemon = trainer_enemy.get_current_pokemon()
        wild_pokemon_name = wild_pokemon.get_name()

        if battle.is_trainer_battle():
            return ActionSummary(POKEBALL_INVALID_BATTLE_TYPE)
        if not trainer_player.can_add_pokemon(wild_pokemon):
            return ActionSummary(POKEBALL_FULL_TEAM.format(wild_pokemon_name))
        if did_succeed(self._catch_chance):
            trainer_player.add_pokemon(wild_pokemon)
            battle.is_battle_over = True
            message = POKEBALL_SUCCESSFUL_CATCH.format(wild_pokemon_name)
            return ActionSummary(message)
        else:
            message = POKEBALL_UNSUCCESSFUL_CATCH.format(wild_pokemon_name)
            return ActionSummary(message)

    def __str__(self) -> str:
        return f'Pokeball(\'{self.name}\')'


class Food(Item):
    """An Item representing Food which restores the health of the Pokemon
    whose Trainer uses it."""
    def __init__(self, name: str, health_restored: int) -> None:
        """Constructs Food.

        Parameters:
            name (str): The name of the Food.
            health_restored (int): The number of points by which the Pokemon's
                                    health will be restored.
        Returns:
            (None)
        """
        super().__init__(name)
        self._health_restored = health_restored

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        trainer = battle.get_trainer(is_player)
        current_pokemon = trainer.get_current_pokemon()
        current_pokemon.modify_health(self._health_restored)
        FOOD_CONSUMED = '{} ate {}.'
        return ActionSummary(FOOD_CONSUMED.format(current_pokemon.get_name(),
                                                  self.name))

    def __str__(self) -> str:
        return f'Food(\'{self.name}\')'


class Move(Action):
    """An abstract class representing Moves a Pokemon can learn."""
    def __init__(self,
                 name: str,
                 element_type: str,
                 max_uses: int,
                 speed: int) -> None:
        """Constructs a Move.

        Parameters:
            name (str): The name of the Move.
            element_type (str): The element type of the Move.
            max_uses (int): The maximum number of times the Move can be used
                                before resting.
            speed (int): The speed of the Move.

        Returns:
            (None)
        """
        self.name = name
        self.element_type = element_type
        self.max_uses = max_uses
        self.speed = speed

    def get_name(self) -> str:
        """(str) Returns the name of the Move."""
        return self.name

    def get_element_type(self) -> str:
        """(str) Returns the element type of the Move."""
        return self.element_type

    def get_max_uses(self) -> int:
        """(int) Returns the max uses of the Move."""
        return self.max_uses

    def get_priority(self) -> int:
        return SPEED_BASED_ACTION_PRIORITY + self.speed

    def is_valid(self, battle: Battle, is_player: bool) -> bool:
        trainer = battle.get_trainer(is_player)
        current_pokemon = trainer.get_current_pokemon()

        if not super().is_valid(battle, is_player) or \
           current_pokemon.has_fainted():
            return False
        result = False
        for move_info in current_pokemon.moves:
            if move_info[0] == self:
                result = True
        if not result:
            return False
        if current_pokemon.get_remaining_move_uses(move_info[0]) > 0:
            return True
        return False

    def apply(self, battle: Battle, is_player: bool) -> ActionSummary:
        POKEMON_GAINED_EXP = '{} gained {} exp.'

        player = battle.get_trainer(is_player)
        pokemon_name = player.get_current_pokemon().get_name()
        enemy = battle.get_trainer(not is_player)
        combined_summary = self.apply_ally_effects(player)
        combined_summary.combine(self.apply_enemy_effects(player, enemy))
        player.get_current_pokemon().reduce_move_count(self)
        if len(combined_summary.get_messages()) == 2:
            combined_summary.add_message(POKEMON_GAINED_EXP.format(pokemon_name, 5))
        return combined_summary

    def apply_ally_effects(self, trainer: Trainer) -> ActionSummary:
        """Applies effect(s) of the Move to the Trainer making the Move, if
        appropriate.

        Parameters:
            trainer (Trainer): The Trainer making the Move.

        Returns:
            (ActionSummary): The effect(s) of the applied Move.
        """
        return ActionSummary()

    def apply_enemy_effects(self,
                            trainer: Trainer,
                            enemy: Trainer) -> ActionSummary:
        """Applies effect(s) of the Move to the Trainer on which the Move is
        being made, if appropriate.

        Parameters:
            trainer (Trainer): The Trainer making the Move.
            enemy (Trainer): The Trainer on which the Move is being made.

        Returns:
            (ActionSummary): The effect(s) of the applied Move.
        """
        return ActionSummary()


class Attack(Move):
    """A class representing Moves that cause damage to an enemy Pokemon."""
    def __init__(self,
                 name: str,
                 element_type: str,
                 max_uses: int,
                 speed: int,
                 base_damage: int,
                 hit_chance: float) -> None:
        """Constructs an Attack Move.

        Parameters:
            name (str): The name of the Attack.
            element_type (str): The element type of the Attack.
            max_uses (int): The maximum number of times this Attack can be
                                used.
            speed (int): The speed of the Attack.
            base_damage (int): The base damage of the Attack.
            hit_chance (float): The base hit chance of the Attack.

        Returns:
            (None)
        """
        super().__init__(name, element_type, max_uses, speed)
        self._base_damage = base_damage
        self._hit_chance = hit_chance

    def did_hit(self, pokemon: Pokemon) -> bool:
        """Determines whether the Attack hits.

        Parameters:
            pokemon (Pokemon): The attacking Pokemon.

        Returns:
            (bool): True iff the Attack hits.
        """
        total_hit_chance = pokemon.get_stats().get_hit_chance() * \
                           self._hit_chance
        if did_succeed(total_hit_chance):
            return True
        return False

    def calculate_damage(self,
                         pokemon: Pokemon,
                         enemy_pokemon: Pokemon) -> int:
        """Calculates the damage caused to the enemy Pokemon's health
        by the attacking Pokemon's Attack.

        Parameters:
            pokemon (Pokemon): The attacking Pokemon.
            enemy_pokemon (Pokemon): The Pokemon receiving the Attack.

        Returns:
            (int): The number of health points by which the enemy Pokemon's
                    health will be reduced.
        """
        if not self.did_hit(pokemon):
            return 0
        move_element_type = super().get_element_type()
        element_type = ElementType.of(move_element_type)
        enemy_element_type = enemy_pokemon.get_element_type()
        effectiveness = element_type.get_effectiveness(enemy_element_type)
        attack = pokemon.get_stats().get_attack()
        defense = enemy_pokemon.get_stats().get_defense()
        total_damage = math.floor(self._base_damage * \
                       effectiveness * attack / (defense + 1))
        return total_damage

    def apply_ally_effects(self, trainer: Trainer) -> ActionSummary:
        current_pokemon = trainer.get_current_pokemon()
        current_pokemon_name = current_pokemon.get_name()
        if self.did_hit(current_pokemon):
            ATTACK_USED = '{} used {}.'
            return ActionSummary(ATTACK_USED.format(current_pokemon_name,
                                 self.get_name()))
        else:
            ATTACK_MISSED = '{} missed!'
            return ActionSummary(ATTACK_MISSED.format(current_pokemon_name))

    def apply_enemy_effects(self,
                            trainer: Trainer,
                            enemy: Trainer) -> ActionSummary:
        pokemon = trainer.get_current_pokemon()
        pokemon_name = pokemon.get_name()
        enemy_pokemon = enemy.get_current_pokemon()
        enemy_pokemon_name = enemy_pokemon.get_name()
        experience = enemy_pokemon.experience_on_death()
        damage = self.calculate_damage(pokemon, enemy_pokemon)
        enemy_pokemon.modify_health(-damage)

        summary = ActionSummary()
        if enemy_pokemon.has_fainted():
            POKEMON_FAINTED = '{} has fainted.'
            summary = ActionSummary(POKEMON_FAINTED.format(enemy_pokemon_name))
            summary.combine(ActionSummary())
        return summary

    def __str__(self) -> str:
        result = (
                    f'Attack(\'{self.name}\', '
                    f'\'{self.element_type}\', '
                    f'{self.max_uses})'
        )
        return result


class StatusModifier(Move):
    """An abstract class representing buffs and debuffs."""
    def __init__(self,
                 name: str,
                 element_type: str,
                 max_uses: int,
                 speed: int,
                 modification: Tuple[float, int, int, int],
                 rounds: int) -> None:
        """Constructs a Status Modifier.

        Parameters:
            name (str): The name of the Status Modifier.
            element_type (str): The element type of the Status Modifier.
            max_uses (int): The maximum number of times this Status
                                Modifier can be used.
            speed (int): The speed of the Status Modifier.
            modification (Tuple[float, int, int, int]): The values by which
                            a Pokemon's Stats are changed.
            rounds (int): The number of rounds for which the Status Modifier
                            is in effect.
        Returns:
        (None)
        """
        super().__init__(name, element_type, max_uses, speed)
        self._modification = modification
        self._rounds = rounds


class Buff(StatusModifier):
    """A class representing a Status Modifier when the Pokemon Stats are
    increased."""
    def apply_ally_effects(self, trainer: Trainer) -> ActionSummary:
        trainer.get_current_pokemon().add_stat_modifier(modification)
        pokemon_name = trainer.get_current_pokemon().get_name()
        POKEMON_BUFFED = '{} was buffed for {} turns.'
        message = POKEMON_BUFFED.format(pokemon_name, rounds)
        return ActionSummary(message)

    def __str__(self) -> str:
        result = (
                    f'Buff(\'{self.name}\', '
                    f'\'{self.element_type}\', '
                    f'{self.max_uses})'
        )
        return result


class Debuff(StatusModifier):
    """A class representing a Status Modifier when the PokemonStats are
    decreased."""
    def apply_enemy_effects(self,
                            trainer: Trainer,
                            enemy: Trainer) -> ActionSummary:
        enemy.get_current_pokemon().add_stat_modifier(modification)
        pokemon_name = enemy.get_current_pokemon().get_name()
        POKEMON_DEBUFFED = '{} was debuffed for {} turns.'
        message = POKEMON_DEBUFFED.format(pokemon_name, rounds)
        return ActionSummary(message)

    def __str__(self) -> str:
        result = (
                    f'Debuff(\'{self.name}\', '
                    f'\'{self.element_type}\', '
                    f'{self.max_uses})'
        )
        return result


# Below are the classes and functions which pertain only to masters students.
class Strategy(object):
    """An abstract class providing behaviour to determine a next action given a battle state."""

    def get_next_action(self, battle: Battle, is_player: bool) -> Action:
        """Determines next action given battle state.

        Parameters:
            battle (Battle): A Pokemon Battle.
            is_player (bool): True iff the Trainer is the player

        Returns:
            (Action): The consequent action to be performed based on strategy.
        """
        raise NotImplementedError()


class ScaredyCat(Strategy):
    """An Strategy in which the trainer trys to flee a Battle."""
    pass


class TeamRocket(Strategy):
    """A Strategy used exclusively by members of Team Rocket."""
    pass


def create_encounter(trainer: Trainer, wild_pokemon: Pokemon) -> Battle:
    """Creates an instance of a non-trainer Battle (between a Trainer and
    a wild pokemon)."""
    pass


if __name__ == "__main__":
    print(WRONG_FILE_MESSAGE)
