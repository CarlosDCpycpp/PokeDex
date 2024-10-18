from __future__ import annotations
import os
from typing import (
    overload,
    Any,
    Type
)
import webbrowser  # NOQA
from typing import (
    Generator
)

from ._utils import (
    raise_if,
    check_type,
    # decorators:
    index_based,
    index_based_int,
    pkmn_type,  # NOQA
    # errors:
    PokemonNotFound,
    InvalidPokemonVariant
)

try:
    import pandas as _pd
except ModuleNotFoundError:
    raise ModuleNotFoundError('Pandas package needed for this package\'s execution.\n'
                              'Install at: https://pypi.org/project/pandas/ \n'
                              'or with the \"pip install pandas\" command on the terminal')


__all__: list[str] = ['Pokemon']


# the actual code

class Pokemon:
    __package_directory = os.path.dirname(__file__)
    __data_path = os.path.join(__package_directory, 'data', 'Pokedex_Cleaned.csv')  # NOQA

    __data: _pd.DataFrame = _pd.read_csv(
        __data_path,
        encoding='utf-8',
        encoding_errors='ignore'
    )

    __numbers, __names = __data['#'], __data['Name']
    __type1, __type2 = __data['Primary Type'], __data['Secondary Type']
    __bst = __data['Total']
    __hp, __atk, __def = __data['HP'], __data['Attack'], __data['Defense']
    __sp_atk, __sp_def, __spd = __data['Sp.Atk'], __data['Sp.Def'], __data['Speed']
    __variants = __data['Variant']

    __max_number: int = int(__numbers.iloc[-1])
    __pkmn_number_length: int = len(str(__max_number))  # NOQA

    __possible_variants = set([(variant if variant is not None else '') for variant in __variants])

    def __init__(self, num: int = None, name: str = None, variant: str = None):

        # checks
        variable_table: list[list[Any | Type | str]] = [
            [num, int, 'num'],
            [name, str, 'name'],
            [variant, str, 'variant']
        ]
        for row in variable_table:
            check_type(row[0], row[1], row[2])
        assert not (num is None and name is None), 'Parameters \"num\" and \"name\" must not be both \"None\"'
        raise_if(
            InvalidPokemonVariant,
            variant is not None and variant not in Pokemon.__possible_variants,
            f'Invalid pokemon variant: {variant}.'
        )

        self.__name = name
        self.__number = num

        self.__variant = variant

        # get index
        index_options = []
        index_flag: bool = False

        if self.__name is not None:
            for index, pkmn_name in enumerate(Pokemon.__names):  # NOQA
                if pkmn_name.lower() == self.__name.lower():
                    index_options.append(index)
                    index_flag = True

        elif self.__number is not None:
            raise_if(
                PokemonNotFound,
                not (0 < self.__number <= Pokemon.__max_number),
                f'Pokemon number must be above 0 and less than or equal to {Pokemon.__max_number}.'
            )

            for index, pkmn_num in enumerate(Pokemon.__numbers):  # NOQA
                if pkmn_num == self.__number:
                    index_options.append(index)
                    index_flag = True

        else:  # this should be unreachable
            raise PokemonNotFound

        raise_if(PokemonNotFound, not index_flag)

        # handle variants
        if variant is None:
            raise_if(PokemonNotFound, not index_options)
            if index_options:
                self._index = index_options[0]
        else:
            for index in index_options:
                if Pokemon.__variants[index].lower() == variant.lower():
                    self._index = index
                    break
            else:
                raise PokemonNotFound

    @property
    def more_info(self) -> str:
        return f'https://www.pokemon.com/us/pokedex/{self.name.lower()}'

    def see_more_info(self) -> None:
        webbrowser.open(self.more_info)

    @property
    def picture(self) -> str:
        index = str(self.number)
        if not len(index) in [3, 4]:
            index = ('0' * (3 - len(index))) + index
        return f'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{index}.png'

    def open_picture(self) -> None:
        webbrowser.open(self.picture)

    @property
    @index_based
    def name(self) -> str:
        return Pokemon.__names

    @property
    @index_based
    def number(self) -> int:
        return Pokemon.__numbers

    @property
    def __number_str(self) -> str:
        return f'#{'0' * (4 - len(str(self.number))) + str(self.number)}'

    @property
    def variant(self):
        return self.__variant.title() if self.__variant is not None else 'Base Form'

    @property
    @pkmn_type
    def type1(self) -> str:
        return Pokemon.__type1

    @property
    @pkmn_type
    def type2(self) -> str:
        return Pokemon.__type2

    @property
    def types(self) -> tuple[str | None, str | None]:
        return self.type1,  self.type2

    def get_type(self, type_index: int = None) -> str | tuple[str, str]:
        raise_if(
            IndexError,
            type_index in [0, 1, 2, None],
            f'Invalid index: {type_index}.'
        )
        types = {1: self.type1, 2: self.type2}

        if isinstance(type_index, int):
            return types[type_index if type_index != 0 else 1]
        elif type_index is None:
            return self.type1, self.type2

    @property
    @index_based_int
    def bst(self) -> int:
        return Pokemon.__bst

    @property
    @index_based_int
    def hp(self) -> int:
        return Pokemon.__hp

    @property
    @index_based_int
    def attack(self) -> int:
        return Pokemon.__atk

    @property
    @index_based_int
    def defense(self) -> int:
        return Pokemon.__def

    @property
    @index_based_int
    def sp_attack(self) -> int:
        return Pokemon.__sp_atk

    @property
    @index_based_int
    def sp_defense(self) -> int:
        return Pokemon.__sp_def

    @property
    @index_based_int
    def speed(self) -> int:
        return Pokemon.__spd

    @property
    def stats(self) -> list[int]:
        return [
            self.hp,
            self.attack,
            self.defense,
            self.sp_attack,
            self.sp_defense,
            self.speed
        ]

    @property
    def __stat_strs(self) -> dict:
        return {('hp', 'health points'): f'Hp: {self.hp}',
                ('atk', 'attack'): f'Attack: {self.attack}',
                ('def', 'defense'): f'Defense: {self.defense}',
                ('sp_a', 'special_attack'): f'Special Attack: {self.sp_attack}',
                ('sp_d', 'special_defense'): f'Special Defense: {self.sp_defense}',
                ('spd', 'speed'): f'Speed: {self.speed}'}

    @property
    def __stat_info(self) -> dict[str, int]:
        return {'hp': self.hp, 'atk': self.attack, 'def': self.defense,
                'sp_a': self.sp_attack, 'sp_d': self.sp_defense, 'spd': self.speed}

    def __str__(self) -> str:
        return f'{self.__number_str} {self.name} {self.variant}'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash((self.number, self.name, self.variant))

    def __iter__(self) -> Generator[int]:
        for stat in self.stats:
            yield stat

    def __eq__(self, other: Pokemon) -> bool:
        if (
            self.number == other.number and
            self.name == other.name and
            self.variant == other.variant
        ):
            return True
        return False

    def __ne__(self, other):
        return ~(self == other)

    def __getitem__(self, item: str | int) -> str | int:
        if isinstance(item, int):
            return self.get_type(item)
        elif isinstance(item, str):
            result = self.__stat_info.get(item.lower().replace(' ', '_').strip('_'), None)
            raise_if(
                IndexError,
                result is not None,
                f'Invalid stat {item}.'
            )
        else:
            raise ValueError(f'Invalid item type {type(item)}')
        return result

    def __format__(self, format_spec: str) -> str:
        key_word, *rest = format_spec.lower().strip().split(' ')

        output = ''
        match key_word:
            case 'stats':
                for _, stat_str in self.__stat_strs.items():
                    output += f'{stat_str}; '
                output = output[:-2]

            case 'stat':
                for keys, stat_string in self.__stat_strs.items():
                    for stat in rest:
                        for key in keys:
                            if key == stat:
                                output += f'{stat_string}; '
                output = output[:-2]

            case 'number' | 'index':
                output = self.__number_str

            case 'bst':
                output = str(self.bst)

            case 'type':
                if not rest:
                    output = f'{self.type1} {self.type2}'
                else:
                    for type_index in rest:
                        if index := int(type_index) in [1, 2]:
                            output += self.get_type(index)

            case '':
                raise ValueError(f'Empty string passed as a specifier.')
            case _:
                raise ValueError(f'Unknown specifier: {format_spec}.')

        return output

    @staticmethod
    @overload
    def get(name: str) -> Pokemon:
        return Pokemon(name=name)

    @staticmethod
    @overload
    def get(num: int) -> Pokemon:
        return Pokemon(num=num)

    @staticmethod
    def get(__variant: str) -> list[Pokemon] | Pokemon:
        variant_pkmn_indexes = []  # NOQA
        variant = __variant if __variant.lower().strip() not in ['', 'base form', 'base'] else 'nan'
        for index, variant_ in enumerate(Pokemon.__variants):
            if variant == variant_.lower().strip():
                variant_pkmn_indexes.append(index)
        result = [Pokemon(index) for index in variant_pkmn_indexes]
        if result:
            return result if len(result) != 1 else result[0]
        raise InvalidPokemonVariant
