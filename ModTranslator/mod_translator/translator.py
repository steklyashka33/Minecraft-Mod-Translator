__author__ = 'Steklyashka'

from typing import Optional, Tuple, Union, Callable, Dict
from googletrans.constants import DEFAULT_CLIENT_SERVICE_URLS, DEFAULT_RAISE_EXCEPTION, DEFAULT_USER_AGENT
from googletrans.models import Translated
from googletrans import Translator as google_Translator
import sys

import httpcore
from httpx import Timeout

sys.setrecursionlimit(100)

#pip3 install googletrans==3.1.0a0


class Translator(google_Translator):
	"""Google Translate ajax API implementation class

    You have to create an instance of Translator to use this API

    :param service_urls: google translate url list. URLs will be used randomly.
                         For example ``['translate.google.com', 'translate.google.co.kr']``
                         To preferably use the non webapp api, service url should be translate.googleapis.com
    :type service_urls: a sequence of strings

    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`

    :param proxies: proxies configuration.
                    Dictionary mapping protocol or protocol and host to the URL of the proxy
                    For example ``{'http': 'foo.bar:3128', 'http://host.name': 'foo.bar:4012'}``
    :type proxies: dictionary

    :param timeout: Definition of timeout for httpx library.
                    Will be used for every request.
    :type timeout: number or a double of numbers
    :param raise_exception: if `True` then raise exception if smth will go wrong
    :type raise_exception: boolean
    """
    
	def __init__(self,
	      		 service_urls = DEFAULT_CLIENT_SERVICE_URLS, user_agent: str = DEFAULT_USER_AGENT,
		  		 raise_exception = DEFAULT_RAISE_EXCEPTION,
          		 proxies: Union[Dict[str, httpcore.SyncHTTPTransport], None] = None,
          		 timeout: Union[Timeout, None] = None,
          		 http2: bool = True):
		super().__init__(service_urls, user_agent, raise_exception, proxies, timeout, http2)  # type: ignore

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
		connected_text = self._join_text(texts)
		connected_text_lenght = len(connected_text)
		self.max_characters = 5000 # google translate limit of 5000 characters

		if connected_text_lenght < self.max_characters:
			return [texts]
		else:
			text1 = self._check_string_limit( texts[ :texts_lenght//2 ] )
			text2 = self._check_string_limit( texts[ texts_lenght//2: ] )
			return text1 + text2
	
	def _join_text(self, texts: list) -> str:
		"""Соединяет тексты раздилителем."""
		return self._separator.join(texts)
	
	def _split_text(self, text: str) -> list[str]:
		"""Разделят текст по раздилителю."""
		if not text:
			return []
		split_text = text.split(self._separator.strip())
		strip_function = lambda s: s.strip()
		strip_text = list(map(strip_function, split_text)) #обрезаем текст от пробелов
		return strip_text


if __name__ == '__main__':

	data = [
  	"Chest of Drawers",
  	"Egg Plant",
  	"Eye Vine",
	]

	translation = Translator().translate(data, dest='ru')
	print(f"{translation}")