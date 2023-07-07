__author__ = 'Steklyashka'

from typing import Optional, Tuple, Union, Callable
from googletrans.models import Translated
from googletrans import Translator as google_Translator
import sys

sys.setrecursionlimit(100)

#pip3 install googletrans==3.1.0a0


class Translator(google_Translator):

	def translate(self,
	       text: Union[str, list[str]],
		   dest='en',
		   src='auto',
		   **kwargs) -> Union[str, list[str]]:
		"""Возращает экземпляр класса Translated с переводом."""

		if type(text) is list:
			self._separator = ' //. '  #Разделитель
			self.dest = dest
			self.src = src
			self.kwargs = kwargs
			
			list_texts = self._check_string_limit(text)
			if list_texts == -1: # Пойманая ошибка
				return text
			translated_texts = [self._text_translation(texts) for texts in list_texts]
			
			#Соединяем переведённые тексты
			return sum(translated_texts, [])

		else:
			return super().translate(text, dest, src, **kwargs).text
	
	def _text_translation(self, texts: list[str]) -> list[str]:
		"""Переводит текст."""

		#Соединяем тексты раздилителем
		connected_text = self._join_text(texts)
		#Находим длину первоначального текста
		len_text = len(texts)

		#Переводим текст
		translated = super().translate(connected_text, self.dest, self.src, **self.kwargs)
		#Разделяем переведённый текст разделителем
		result = self._split_text(translated.text)
		
		#Сверяем длину переведённого и не переведённого текста.
		if len(result) != len_text:
			translation1 = self._text_translation( texts[ :len_text//2 ] )
			translation2 = self._text_translation( texts[ len_text//2: ] )
			return translation1 + translation2
		else:
			return result
	
	def _check_string_limit(self, texts: list[str]) -> list[ list[str] ]:
		"""Проверяет на превышение лимита и возращает списки, которые не превышают лимит."""

		texts_lenght = len(texts)
		try:
			connected_text = self._join_text(texts)
		except TypeError: # texts имеет элементы не типа str
			return -1
		connected_text_lenght = len(connected_text)
		self.max_characters = 5000 # google translate limit of 5000 characters

		if connected_text_lenght < self.max_characters:
			return [connected_text]
		else:
			text1 = self._check_string_limit( texts[ :texts_lenght//2 ] )
			text2 = self._check_string_limit( texts[ texts_lenght//2: ] )
			return text1 + text2
	
	def _join_text(self, texts: list) -> str:
		"""Соединяет тексты раздилителем."""
		return self._separator.join(texts)
	
	def _split_text(self, text: str) -> list[str]:
		"""Разделят текст по раздилителю."""
		split_text = text.split(self._separator.strip())
		strip_function = lambda s: s.strip()
		return list(map(strip_function, split_text)) #обрезаем текст от пробелов


if __name__ == '__main__':

	data = [
  	"Chest of Drawers",
  	"Egg Plant",
  	"Eye Vine",
	]

	translation = Translator().translate(data, dest='ru')
	print(f"{translation}")