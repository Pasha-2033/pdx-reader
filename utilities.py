from typing import TypeVar, Generic, Iterable

T = TypeVar('T')
class nenumerate(Generic[T]):
	iterable:	Iterable[T]
	index:		int
	def __init__(self, iterable: Iterable[T]):
		self.iterable = iterable
		self.index = 0
	def __iter__(self):
		return self
	def __next__(self) -> tuple[int, T]:
		if self.index < len(self.iterable):
			self.index += 1
			return (-self.index, self.iterable[-self.index])
		raise StopIteration
	
class renumerate(Generic[T]):
	iterable:	Iterable[T]
	index:		int
	def __init__(self, iterable: Iterable[T]):
		self.iterable = iterable
		self.index = len(self.iterable)
	def __iter__(self):
		return self
	def __next__(self) -> tuple[int, T]:
		if self.index > 0:
			self.index -= 1
			return (self.index, self.iterable[self.index])
		raise StopIteration