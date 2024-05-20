from typing import AsyncContextManager, Callable, TypeAlias, TypeVar

_T = TypeVar("_T")

AsyncContextManagerFactory: TypeAlias = Callable[[], AsyncContextManager[_T]]
