from typing import NoReturn, Any, Callable, TypeVar


Wrapper = TypeVar('Wrapper', bound=Callable[..., Any])
Check = NoReturn | None


def raise_if(error: type[Exception], condition: bool, message: str = None) -> Check:
    if condition:
        if message is not None:
            raise error(message)
        else:
            raise error


def check_type(variable, type_: type, variable_name: str = None) -> Check:
    raise_if(
        ValueError,
        not (isinstance(variable, type_) or variable is None),
        f'Variable \"{variable_name}\" must either be a \"{type_}\" or a \"{type(None)}\".'
    )


# decorators

def index_based(func) -> Wrapper:
    def wrapper(self):
        return func(self=self)[self._index]
    return wrapper


def index_based_int(func) -> Wrapper:
    def wrapper(self):
        return int(func(self=self)[self._index])
    return wrapper


def pkmn_type(func) -> Wrapper:  # NOQA
    def wrapper(self):
        result = func(self=self)[self._index]
        return result if not isinstance(result, float) else None
    return wrapper


# errors

class PokemonNotFound(Exception):
    pass


class InvalidPokemonVariant(Exception):
    pass
