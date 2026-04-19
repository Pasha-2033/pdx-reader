from typing import TypeVar, Generic, Iterable, Iterator
from operator import length_hint

T = TypeVar('T')
class iter_base(Generic[T]):
	iterable:	Iterable[T]
	index:	int
	def __init__(self, iterable: Iterable[T], index: int):
		self.iterable = iterable
		self.index = index
	def __iter__(self) -> Iterator[T]:
		return self

	
class reverse_begin(iter_base[T]):
	def __init__(self, iterable: Iterable[T], offset: int = 0):
		super().__init__(iterable, len(iterable) - offset)
	def __next__(self) -> tuple[int, T, Iterator[T]]:
		if self.index > 0:
			self.index -= 1
			return self.index, self.iterable[self.index], self
		raise StopIteration
	def set_index(self, new_index: int) -> None:
		self.index = min(len(self.iterable), new_index)

class forward_begin(iter_base[T]):
	def __init__(self, iterable: Iterable[T], offset: int = 0):
		super().__init__(iterable, offset - 1)
	def __next__(self) -> tuple[int, T, Iterator[T]]:
		if self.index < len(self.iterable) - 1:
			self.index += 1
			return self.index, self.iterable[self.index], self
		raise StopIteration
	def set_index(self, new_index: int) -> None:
		self.index = max(0, new_index)
	