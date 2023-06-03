__author__ = 'Steklyashka'

from googletrans import Translator as Tr

#pip3 install googletrans==3.1.0a0


class Translator(Tr):

	def translate(self, text, dest='en', src='auto', **kwargs):
		"""Возращает экземпляр класса Translated с переводом."""

		if type(text) is list:
			self._separator = ' //. '  #Разделитель
			self.dest = dest
			self.src = src
			self.kwargs = kwargs
			
			origin = text
			translate = super().translate

			connected_texts = self._join_text(origin)
			translated_text = []
			#print(connected_texts)

			for connected_text in connected_texts:
				translated_text.append(
					self._text_translation(connected_text)
				)
			
			#Берём за основу первый элемент списка
			Translated = translated_text[0]
			#Изменяем текст на переведённое
			Translated.text = sum([i.text for i in translated_text], [])

		else:
			Translated = translate(text, dest, src, **kwargs)
			
		return Translated
	
	def _text_translation(self, text: str) -> list[str]:
		"""Переводит текст и разделяет его."""
		
		#Находим длину первоначального текста
		len_text = len(self._split_text(text))

		#Переводим текст получая 
		translated = super().translate(text, self.dest, self.src, **self.kwargs)
		#Разделяем переаедённый текст
		translated.text = list(map(lambda s: s.strip(), self._split_text(translated.text)))
		
		#Сверяем длину переведённого и не переведённого текста.
		if len(translated.text) != len_text:
			translated.text = sum(
				self._text_translation( text[ :len(text)//2 ] ).text,
				self._text_translation( text[ len(text)//2: ] ).text
			)
		
		return translated
	
	def _join_text(self, text: list) -> tuple[str]:
		"""Соединяет текст раздилителем и проверяет его длинну
		(у google translate ошраничение на 5000 символов за 1 перевод)."""
		connected_text = self._separator.join(text) #Соединяем текст раздилителем.
		max_characters = 5000

		if len(connected_text) < max_characters:
			return [connected_text]
		
		else:
			text1 = self._join_text( text[ :len(text)//2 ] )
			text2 = self._join_text( text[ len(text)//2: ] )
			
			#Если в списке список:
			if type(text1[0]) is list: text1[0]
			if type(text2[0]) is list: text2[0]

			return sum([text1, text2], [])
	
	def _split_text(self, text: str) -> str:
		"""Разделят текст по раздилителю."""
		return text.split(self._separator.strip())


if __name__ == '__main__':

	data = [
  	"Chest of Drawers",
  	"Egg Plant",
  	"Eye Vine",
	]

	from time import time
	start = time()

	list_values = list(data)
	translation = Translator().translate(list_values, dest='ru')
	print(f"{translation}")

	print("execution time:", time() - start)