"""
'inp' contains the class representing INP files.

Classes:
	Inp: Representation of INP files.
"""


from typing import *
import collections
import re

from .block import Block
from .cells import Cells
from .surfaces import Surfaces
from .data import Data
from .._utils import parser
from .._utils import errors
from .._utils import types

class Inp:
	"""
	'Inp' represents INP files.

	Attributes:
		message: INP message.
		title: INP title.
		cells: INP cell card block.
		surfaces: INP surface card block.
		data: INP data card block.
		other: INP other block.
	"""


	def __init__(self) -> Self:
		"""
		'__init__' initializes 'Inp'.
		"""

		self.message: str = None
		self.title: str = None
		self.cells: Type[Cells] = Cells()
		self.surfaces: Type[surfaces] = Surfaces()
		self.data: Type[Data] = Data()
		self.other: str = None


	def set_message(self, message: str) -> None:
		"""
		'set_message' sets INP messages.

		'set_message' checks messages have the required "message:"
		keyword. It sets INP messages to None when given None.

		Parameters:
			message: INP message.

		Raises:
			MCNPSyntaxError: Missing keyword in INP message.
		"""

		if message is not None and not message[:9]:
			raise errors.MCNPSyntaxError(errors.MCNPSyntaxCodes.KEYWORD_INP_MESSAGE)

		self.message = message


	def set_title(self, title: str) -> None:
		"""
		'set_title' sets INP titles.

		'set_title' checks given titles pass the 80 character limit.
		It sets INP titles to None when given None.

		Parmeters:
			title: INP title.

		Raises:
			MCNPSemanticError: Invalid INP title.
		"""

		if message is not None and not len(title) < 80:
			raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_INP_TITLE)

		self.title = title


	@classmethod
	def from_mcnp(cls, source: str) -> Self:
		"""
		'from_mcnp' generates input objects from INP.

		Parameters:
			source (str): INP to parse.

		Returns:
			inp (Input): Input object.
		"""
		
		inp = cls()

		source = parser.Preprocessor.process_inp(source)
		lines = parser.Parser(soruce, '\n', EOFError)

		# Processing Message Block
		if lines.peekl()[:9] == "message:":
			inp.set_message(lines.popl())

		# Processing Title
		inp.title = lines.popl()

		# Processing Cell Cards
		index = list(lines.deque).index('')
		cell_lines = '\n'.join(lines.popl() for _ in range(0, index))
		inp.cells = Cells.from_mcnp(cell_lines)

		lines.popl()

		# Processing Surface Cards
		index = list(lines.deque).index('')
		surface_lines = '\n'.join(lines.popl() for _ in range(0, index))
		inp.surfaces = Surfaces.from_mcnp(surface_lines)
		
		lines.popl()

		# Processing Datum Cards
		index = list(lines.deque).index('')
		datum_lines = '\n'.join(lines.popl() for _ in range(0, index))
		inp.data = Data.from_mcnp(datum_lines)

		inp.other = ''
		while lines:
			inp.other += lines.popl()

		return inp


	@classmethod
	def from_mcnp_file(cls, filename: str) -> Self:
		"""
		'from_file' generates input objects from filenames.

		Parameters:
			filename (str): Name of file to parse.

		Returns:
			inp (Input): Input object.
		"""

		source = ''
		with open(filename, 'r') as file:
			source = ''.join(file.readlines())

		return cls.from_mcnp(source)


	def to_mcnp(self) -> str:
		"""
		'to_mcnp' generates INP from input objects.

		Returns:
			source (str): INP for input object.
		"""

		# Appending Message Block
		source = self.message + '\n' if self.message else ''

		# Appending Title Block
		if not self.title: raise ValueError
		if len(self.title) > 80: raise ValueError
		source += self.title + '\n'

		# Appending Blocks
		source += Cells.to_mcnp(self.cells) + '\n'
		source += Surfaces.to_mcnp(self.surfaces) + '\n'
		source += Data.to_mcnp(self.data) + '\n'

		return source


	def to_mcnp_file(self, filename: str) -> int:
		"""
		'to_mcnp_file' generates INP files from input objects.

		Parameters (str):
			filename (str): Output filename.
		"""

		with open(filename, 'w') as file:
			return file.write(self.to_mcnp())

		return 0


	def to_arguments(self) -> dict:
		"""
		'to_arguments' generates dictionaries from input objects.

		Returns:
			arguments (list): Dictionary of input object data.

		Returns:
			chars_written (int): Number of chars written to file.
		"""
		
		return {'message': self.message, 'title': self.title, 'cells': self.cells.to_arguments(), 'surfaces': self.surfaces.to_arguments(), 'data': self.data.to_arguments(), 'other': self.other}

