from abc import ABC, abstractmethod

import typing as t
import inspect

import logging
import traceback



Key = t.TypeVar("Key")
Value = t.TypeVar("Value")
Result = t.TypeVar("Result")



class Extractor(ABC, t.Generic[Result]):
	@abstractmethod
	def __call__(self, mapping: t.Mapping[Key, Value]) -> Result:
		raise RuntimeError(self.__call__)



class Returner(Extractor[Result]):
	def __init__(self, value: Result) -> None:
		self.__value = value

	
	def __call__(self, _: t.Mapping[Key, Value]) -> Result:
		return self.__value



class KeyExtractor(Extractor[Value | None], t.Generic[Key, Value]):
	def __init__(self, key: Key, default: Value | None = None) -> None:
		self.__key = key
		self.__default = default


	def __call__(self, mapping: t.Mapping[Key, Value]) -> Value | None:
		return mapping.get(self.__key, self.__default)



class HardKeyExtractor(Extractor[Value], t.Generic[Key, Value]):
	def __init__(self, key: Key) -> None:
		self.__key = key


	def __call__(self, mapping: t.Mapping[Key, Value]) -> Value:
		return mapping[self.__key]



class FuncExtractor(Extractor[Result]):
	def __init__(self, func: t.Callable[..., Result]) -> None:
		self.__func = func


	def __call__(self, mapping: t.Mapping[str, Value]) -> Result:
		requiredParams = self.__getRequiredParams(mapping)
		return self.__func(**requiredParams)

	
	def __getRequiredParams(
		self, mapping: t.Mapping[str, Value]
	) -> t.Dict[str, Value]:
		signature = inspect.signature(self.__func)
		requiredArgNames = signature.parameters.keys()
		return {name: mapping[name] for name in requiredArgNames}



class PlainFuncExtractor(Extractor[Result], t.Generic[Key, Value, Result]):
	def __init__(self, func: t.Callable[[t.Mapping[Key, Value]], Result]) -> None:
		self.__func = func

	
	def __call__(self, mapping: t.Mapping[Key, Value]) -> Result:
		return self.__func(mapping)



# decorators


class SafeExtractor(Extractor[Result]):
	def __init__(
		self,
		main: Extractor,
		default: Result,
		toExcept: t.Tuple[t.Type[BaseException]] = (Exception,)
	) -> None:
		self.__innerExtractor = main
		self.__default = default
		self.__toExcept = toExcept
		self.journal: t.List[BaseException] = []


	def __call__(self, mapping: t.Mapping[Key, Value]) -> Result:
		try:
			return self.__innerExtractor(mapping)
		except self.__toExcept as err:
			logging.debug(traceback.format_exc())
			logging.error(err)
			self.journal.append(err)
			return self.__default



class MassExtractor(
	Extractor[t.Mapping[Key, Result]], t.Dict[Key, Extractor[Result]]
):
	def __init__(
		self,
		extractors: t.Mapping[Key, Extractor[Result]] = {},
		mappingFactory: t.Callable[
			[t.Iterable[t.Tuple[Key, Result]]], t.Mapping[Key, Result]
		] = dict,
		**kwargs: Extractor[Result]
	) -> None:
		super().__init__(extractors, **kwargs)
		self.__mappingFactory = mappingFactory


	def __call__(
		self, mapping: t.Mapping[Key, Value]
	) -> t.Mapping[Key, Result]:
		return self.__mappingFactory(
			(key, extractor(mapping)) for key, extractor in self.items()
		)



ChainableExtractor = Extractor[t.Mapping[Key, Value]] | Extractor[Result]


class ExtractorChain(
	Extractor[t.Mapping[Key, Value]|Result],
	t.List[ChainableExtractor[Key, Value, Result]]
):
	def __init__(
		self,
		*args: ChainableExtractor[Key, Value, Result],
		extractors: t.Iterable[ChainableExtractor[Key, Value, Result]] = []
	) -> None:
		super().__init__(extractors)
		self.extend(args)

	
	def __call__(
		self, mapping: t.Mapping[Key, Value]
	) -> t.Mapping[Key, Value] | Result:
		extracted = mapping
		for extractor in self:
			if not isinstance(extracted, t.Mapping):
				raise TypeError(self.__call__, extracted)
			extracted = extractor(extracted)
		return extracted