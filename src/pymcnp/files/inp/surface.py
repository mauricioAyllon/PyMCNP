"""
``surface`` contains the class representing INP surface cards.

``surface`` packages the ``Surface`` class, providing an object-oriented,
importable interface for INP surface cards.
"""


import numpy as np

import math
from typing import Callable
from enum import StrEnum

from . import card
from . import _cadquery
from ..utils import _parser
from ..utils import errors
from ..utils import types


class Surface(card.Card):
    """
    ``Surface`` represents INP cell cards.

    ``Surface`` implements INP cell cards as a Python class. Its attributes
    store INP surface card input parameters, and its methods provide entry
    points and endpoints for working with MCNP cells. It represents the INP
    surface card syntax element, and it inherits from the ``Card`` super class.

    Attributes:
        number: Surface card number.
        mnemonic: Surface card type identifier.
        transform: Surface card transformation number.
        periodic: Surface card periodic number.
        parameters: Surface parameter list based on mnemonic.
    """

    class SurfaceMnemonic(StrEnum):
        """
        ``SurfaceMnemonic`` represents INP surface card mnemonics

        ``SurfaceMnemonic`` implements INP surface card mnemonics as a Python
        inner class. It enumerates MCNP mnemonics and provides methods for
        casting strings to ``SurfaceMnemonic`` instances. It represents the INP
        surface card mnemonics syntax element, so ``Surface`` depends on
        ``SurfaceMnemonic`` as an enum.
        """

        PLANEGENERAL = "p"
        PLANENORMALX = "px"
        PLANENORMALY = "py"
        PLANENORMALZ = "pz"
        SPHEREORIGIN = "so"
        SPHEREGENERAL = "s"
        SPHERENORMALX = "sx"
        SPHERENORMALY = "sy"
        SPHERENORMALZ = "sz"
        CYLINDERPARALLELX = "c/x"
        CYLINDERPARALLELY = "c/y"
        CYLINDERPARALLELZ = "c/z"
        CYLINDERONX = "cx"
        CYLINDERONY = "cy"
        CYLINDERONZ = "cz"
        CONEPARALLELX = "k/x"
        CONEPARALLELY = "k/y"
        CONEPARALLELZ = "k/z"
        CONEONX = "kx"
        CONEONY = "ky"
        CONEONZ = "kx"
        QUADRATICSPECIAL = "sq"
        QUADRATICGENERAL = "gq"
        TORUSPARALLELX = "tx"
        TORUSPARALLELY = "ty"
        TORUSPARALLELZ = "tz"
        SURFACEX = "x"
        SURFACEY = "y"
        SURFACEZ = "z"
        BOX = "box"
        PARALLELEPIPED = "rpp"
        SPHERE = "sph"
        CYLINDERCIRCULAR = "rcc"
        HEXAGONALPRISM = "rhp"
        CYLINDERELLIPTICAL = "rec"
        CONETRUNCATED = "trc"
        ELLIPSOID = "ell"
        WEDGE = "wed"
        POLYHEDRON = "arb"

        @staticmethod
        def from_mcnp(source: str):
            """
            ``from_mcnp`` generates ``SurfaceMnemonic`` objects from INP.

            ``from_mcnp`` constructs instances of ``SurfaceMnemonic`` from INP
            source strings, so it operates as a class constructor method
            and INP parser helper function.

            Parameters:
                source: INP for surface card mnemonic.

            Returns:
                ``SurfaceMnemonic`` object.

            Raises:
                MCNPSemanticError: INVALID_SURFACE_MNEMONIC.
            """

            source = _parser.Preprocessor.process_inp(source)

            # Processing Mnemonic
            if source not in [enum.value for enum in Surface.SurfaceMnemonic]:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_MNEMONIC)

            return Surface.SurfaceMnemonic(source)

        def to_mcnp(self) -> str:
            """
            ``to_mcnp`` generates INP from ``SurfaceMnemonic`` objects.

            ``to_mcnp`` creates INP source string from ``SurfaceMnemonic``
            objects, so it provides an MCNP endpoint.

            Returns:
                INP string for ``SurfaceMnemonic`` object.
            """

            return self.value

    def __init__(
        self,
        number: int,
        mnemonic: SurfaceMnemonic,
        transform_periodic: int,
        parameters: tuple[float],
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Surface``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.
        """

        super().__init__(number)

        if mnemonic is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_MNEMONIC)

        if parameters is None or not parameters:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        try:
            match mnemonic:
                case Surface.SurfaceMnemonic.PLANEGENERAL:
                    if len(parameters) == 4:
                        obj = PlaneGeneralEquation(
                            number,
                            transform_periodic,
                            *parameters,
                            is_whiteboundary=is_whiteboundary,
                            is_reflecting=is_reflecting,
                        )
                    else:
                        obj = PlaneGeneralPoint(
                            number,
                            transform_periodic,
                            *parameters,
                            is_whiteboundary=is_whiteboundary,
                            is_reflecting=is_reflecting,
                        )
                case Surface.SurfaceMnemonic.PLANENORMALX:
                    obj = PlaneNormalX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.PLANENORMALY:
                    obj = PlaneNormalY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.PLANENORMALZ:
                    obj = PlaneNormalZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SPHEREORIGIN:
                    obj = SphereOrigin(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SPHEREGENERAL:
                    obj = SphereGeneral(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SPHERENORMALX:
                    obj = SphereNormalX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SPHERENORMALY:
                    obj = SphereNormalY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SPHERENORMALZ:
                    obj = SphereNormalZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERPARALLELX:
                    obj = CylinderParallelX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERPARALLELY:
                    obj = CylinderParallelY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERPARALLELZ:
                    obj = CylinderParallelZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERONX:
                    obj = CylinderOnX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERONY:
                    obj = CylinderOnY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERONZ:
                    obj = CylinderOnZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONEPARALLELX:
                    obj = ConeParallelX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONEPARALLELY:
                    obj = ConeParallelY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONEPARALLELZ:
                    obj = ConeParallelZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONEONX:
                    obj = ConeOnX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONEONY:
                    obj = ConeOnY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONEONZ:
                    obj = ConeOnZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.QUADRATICSPECIAL:
                    obj = QuadraticSpecial(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.QUADRATICGENERAL:
                    obj = QuadraticGeneral(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.TORUSPARALLELX:
                    obj = TorusParallelX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.TORUSPARALLELY:
                    obj = TorusParallelY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.TORUSPARALLELZ:
                    obj = TorusParallelZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SURFACEX:
                    obj = SurfaceX(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SURFACEY:
                    obj = SurfaceY(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SURFACEZ:
                    obj = SurfaceZ(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.BOX:
                    obj = Box(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.PARALLELEPIPED:
                    obj = Parallelepiped(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.SPHERE:
                    obj = Sphere(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERCIRCULAR:
                    obj = CylinderCircular(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.HEXAGONALPRISM:
                    obj = HexagonalPrism(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CYLINDERELLIPTICAL:
                    obj = CylinderElliptical(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.CONETRUNCATED:
                    obj = ConeTruncated(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.ELLIPSOID:
                    obj = Ellipsoid(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.WEDGE:
                    obj = Wedge(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case Surface.SurfaceMnemonic.POLYHEDRON:
                    obj = Polyhedron(
                        number, transform_periodic, *parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
                    )
                case _:
                    assert False, "Impossible"

            self.__dict__ = obj.__dict__
            self.__class__ = obj.__class__

        except TypeError:
            raise errors.MCNPSyntaxError(errors.MCNPSyntaxCodes.TOOFEW_SURFACE_ENTRIES)

    @staticmethod
    def from_mcnp(source: str, line: int = None):
        """
        ``from_mcnp`` generates ``Surface`` objects from INP.

        ``from_mcnp`` constructs instances of ``Surface`` from INP source
        strings, so it operates as a class constructor method and INP parser
        helper function.

        Parameters:
            source: INP for surface.
            line: Line number.

        Returns:
            ``Surface`` object.

        Raises:
            MCNPSyntaxError: TOOFEW_SURFACE, TOOLONG_SURFACE.
        """

        # Processing Inline Comment
        comment = None
        if "$" in source:
            source, comment = source.split("$")

        source = _parser.Preprocessor.process_inp(source)
        tokens = _parser.Parser(source.split(" "), errors.MCNPSyntaxError(errors.MCNPSyntaxCodes.TOOFEW_SURFACE))

        # Processing Reflecting Prefix
        if tokens.peekl()[0] == "+":
            is_whiteboundary = True
            is_reflecting = False
            tokens.pushl(tokens.popl()[1:])
        elif tokens.peekl()[0] == "*":
            is_whiteboundary = False
            is_reflecting = True
            tokens.pushl(tokens.popl()[1:])
        else:
            is_whiteboundary = False
            is_reflecting = False

        # Processing Number, Transform/Periodic, Mnemonic, Parameters
        number = types.cast_fortran_integer(tokens.popl())
        if types.cast_fortran_integer(tokens.peekl()) is not None:
            transform_periodic = types.cast_fortran_integer(tokens.popl())
        else:
            transform_periodic = None
        mnemonic = Surface.SurfaceMnemonic.from_mcnp(tokens.popl())
        parameters = tuple([types.cast_fortran_real(tokens.popl()) for _ in range(0, len(tokens))])

        print(parameters)

        surface = Surface(
            number, mnemonic, transform_periodic, parameters, is_whiteboundary=is_whiteboundary, is_reflecting=is_reflecting
        )
        surface.line = line
        surface.comment = comment

        return surface

    def to_mcnp(self) -> str:
        """
        ``to_mcnp`` generates INP from ``Surface`` objects.

        ``to_mcnp`` creates INP source string from ``Surface`` objects,
        so it provides an MCNP endpoint.

        Returns:
            INP string for ``Surface`` object.
        """

        # parameters_str = " ".join([str(param) for _ in,
        source = (
            f"{self.number}{' ' + {self.transform} + ' ' if self.transform is not None else ' '}"
            f"{self.mnemonic} {' '.join(str(parameter) if parameter is not None else '' for parameter in self.parameters)}"
        )

        return _parser.Postprocessor.add_continuation_lines(source)

    def to_arguments(self) -> dict:
        """
        ``to_arguments`` makes dictionaries from ``Surface`` objects.

        ``to_arguments`` creates Python dictionaries from ``Surface`` objects,
        so it provides an MCNP endpoint. The dictionary keys follow the MCNP
        manual.

        Returns:
            Dictionary for ``Surface`` object.
        """

        return {
            "j": self.number,
            "+": self.is_reflecting,
            "*": self.is_whiteboundary,
            "n": self.transform,
            "A": self.mnemonic,
            "list": self.parameters,
        }


class PlaneGeneralPoint(Surface):
    """
    ``PlaneGeneralPoint`` represents INP general planes surface cards.

    ``PlaneGeneralPoint`` inherits attributes from ``Surface``. It
    represents the INP general planes surface card syntax element.

    Attributes:
        x1: Point-defined general plane point #1 x component.
        y1: Point-defined general plane point #1 y component.
        z1: Point-defined general plane point #1 z component.
        x2: Point-defined general plane point #2 x component.
        y2: Point-defined general plane point #2 y component.
        z2: Point-defined general plane point #2 z component.
        x3: Point-defined general plane point #3 x component.
        y3: Point-defined general plane point #3 y component.
        z3: Point-defined general plane point #3 z component.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``PlaneGeneral``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x1: Point-defined general plane point #1 x component.
            y1: Point-defined general plane point #1 y component.
            z1: Point-defined general plane point #1 z component.
            x2: Point-defined general plane point #2 x component.
            y2: Point-defined general plane point #2 y component.
            z2: Point-defined general plane point #2 z component.
            x3: Point-defined general plane point #3 x component.
            y3: Point-defined general plane point #3 y component.
            z3: Point-defined general plane point #3 z component.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.PLANEGENERAL
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if x2 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y2 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z2 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if x3 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y3 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z3 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x1: final[float] = x1
        self.y1: final[float] = y1
        self.z1: final[float] = z1
        self.x2: final[float] = x2
        self.y2: final[float] = y2
        self.z2: final[float] = z2
        self.x3: final[float] = x3
        self.y3: final[float] = y3
        self.z3: final[float] = z3

        self.parameters: final[tuple[float]] = (x1, y1, z1, x2, y2, z2, x3, y3, z3)


class PlaneGeneralEquation(Surface):
    """
    ``PlaneGeneralEquation`` represents INP general planes surface cards.

    ``PlaneGeneralEquation`` inherits attributes from ``Surface``. It
    represents the INP general planes surface card syntax element.

    Attributes:
        a: Equation-defined general plane A coefficent.
        b: Equation-defined general plane B coefficent.
        c: Equation-defined general plane C coefficent.
        d: Equation-defined general plane D coefficent.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        a: float,
        b: float,
        c: float,
        d: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``PlaneGeneral``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            a: Equation-defined general plane A coefficent.
            b: Equation-defined general plane B coefficent.
            c: Equation-defined general plane C coefficent.
            d: Equation-defined general plane D coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.PLANEGENERAL
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if a is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if b is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if c is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if d is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.a: final[float] = a
        self.b: final[float] = b
        self.c: final[float] = c
        self.d: final[float] = d

        self.parameters: final[tuple[float]] = (a, b, c, d)


class PlaneNormalX(Surface):
    """
    ``PlaneNormalX`` represents INP normal-to-the-x-axis surface cards.

    ``PlaneNormalX`` inherits attributes from ``Surface``. It represents the
    INP normal-to-the-x-axis surface card syntax element.

    Attributes:
        d: Normal-to-the-x-axis plane D coefficent.
    """

    def __init__(
        self, number: int, transform_periodic: int, d: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``PlaneNormalX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            d: Normal-to-the-x-axis plane D coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.PLANENORMALX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if d is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.d: final[float] = d

        self.parameters: final[tuple[float]] = (d,)


class PlaneNormalY(Surface):
    """
    ``PlaneNormalY`` represents INP normal-to-the-y-axis surface cards.

    ``PlaneNormalY`` inherits attributes from ``Surface``. It represents the
    INP normal-to-the-y-axis surface card syntax element.

    Attributes:
        d: Normal-to-the-y-axis plane D coefficent.
    """

    def __init__(
        self, number: int, transform_periodic: int, d: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``PlaneNormalY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            d: Normal-to-the-y-axis plane D coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.PLANENORMALY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if d is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.d: final[float] = d

        self.parameters: final[tuple[float]] = (d,)


class PlaneNormalZ(Surface):
    """
    ``PlaneNormalZ`` represents INP normal-to-the-z-axis surface cards.

    ``PlaneNormalZ`` inherits attributes from ``Surface``. It represents the
    INP normal-to-the-z-axis surface card syntax element.

    Attributes:
        d: Normal-to-the-z-axis plane D coefficent.
    """

    def __init__(
        self, number: int, transform_periodic: int, d: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``PlaneNormalZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            d: Normal-to-the-z-axis plane D coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.PLANENORMALZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if d is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.d: final[float] = d

        self.parameters: final[tuple[float]] = (d,)


class SphereOrigin(Surface):
    """
    ``SphereOrigin`` represents INP origin-centered sphere surface cards.

    ``SphereOrigin`` inherits attributes from ``Surface``. It represents the
    INP origin-centered sphere surface card syntax element.

    Attributes:
        r: Origin-centered sphere radius.
    """

    def __init__(
        self, number: int, transform_periodic: int, r: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``SphereOrigin``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            r: Origin-centered sphere radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SPHEREORIGIN
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (r,)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_sphere(self.r)

        return cadquery + "\n"


class SphereGeneral(Surface):
    """
    ``SphereGeneral`` represents INP general sphere surface cards.

    ``SphereGeneral`` inherits attributes from ``Surface``. It represents the
    INP general sphere surface card syntax element.

    Attributes:
        x: General sphere center x component.
        y: General sphere center y component.
        z: General sphere center z component.
        r: General sphere radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SphereGeneral``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: General sphere center x component.
            y: General sphere center y component.
            z: General sphere center z component.
            r: General sphere radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SPHEREGENERAL
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (x, y, z, r)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_sphere(self.r)
        cadquery += _cadquery.add_translation(self.x, self.y, self.z)

        return cadquery + "\n"


class SphereNormalX(Surface):
    """
    ``SphereNormalX`` represents INP on-x-axis sphere surface cards.

    ``SphereNormalX`` inherits attributes from ``Surface``. It represents the
    INP on-x-axis sphere surface card syntax element.

    Attributes:
        x: On-x-axis sphere center x component.
        r: On-x-axis sphere radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SphereNormalX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: On-x-axis sphere center x component.
            r: On-x-axis sphere radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SPHERENORMALX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (x, r)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_sphere(self.r)
        cadquery += _cadquery.add_translation(self.x, 0, 0)

        return cadquery


class SphereNormalY(Surface):
    """
    ``SphereNormalY`` represents INP on-y-axis sphere surface cards.

    ``SphereNormalY`` inherits attributes from ``Surface``. It represents the
    INP on-y-axis sphere surface card syntax element.

    Attributes:
        y: On-y-axis sphere center y component.
        r: On-y-axis sphere radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        y: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SphereNormalY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            y: On-y-axis sphere center y component.
            r: On-y-axis sphere radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SPHERENORMALY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.y: final[float] = y
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (y, r)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_sphere(self.r)
        cadquery += _cadquery.add_translation(0, self.y, 0)

        return cadquery


class SphereNormalZ(Surface):
    """
    ``SphereNormalZ`` represents INP on-z-axis sphere surface cards.

    ``SphereNormalZ`` inherits attributes from ``Surface``. It represents the
    INP on-z-axis sphere surface card syntax element.

    Attributes:
        z: On-z-axis sphere center z component.
        r: On-z-axis sphere radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        z: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SphereNormalZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            z: On-z-axis sphere center z component.
            r: On-z-axis sphere radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SPHERENORMALZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.z: final[float] = z
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (z, r)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_sphere(self.r)
        cadquery += _cadquery.add_translation(0, 0, self.z)

        return cadquery


class CylinderParallelX(Surface):
    """
    ``CylinderParallelX`` represents INP parallel-to-x-axis cylinder surface
    cards.

    ``CylinderParallelX`` inherits attributes from ``Surface``. It represents
    the INP parallel-to-x-axis cylinder surface card syntax element.

    Attributes:
        y: Parallel-to-x-axis cylinder center y component.
        z: Parallel-to-x-axis cylinder center z component.
        r: Parallel-to-x-axis cylinder radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        y: float,
        z: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``CylinderParallelX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            y: Parallel-to-x-axis cylinder center y component.
            z: Parallel-to-x-axis cylinder center z component.
            r: Parallel-to-x-axis cylinder radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERPARALLELX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.y: final[float] = y
        self.z: final[float] = z
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (y, z, r)


class CylinderParallelY(Surface):
    """
    ``CylinderParallelY`` represents INP parallel-to-y-axis cylinder surface
    cards.

    ``CylinderParallelY`` inherits attributes from ``Surface``. It represents
    the INP parallel-to-y-axis cylinder surface card syntax element.

    Attributes:
        x: Parallel-to-y-axis cylinder center x component.
        z: Parallel-to-y-axis cylinder center z component.
        r: Parallel-to-y-axis cylinder radius.
    """

    def __init__(self):
        """
        ``__init__`` initializes ``CylinderParallelY``.
        """

        super().__init__()
        self.mnemonic = Surface.SurfaceMnemonic.CYLINDERPARALLELY

        self.x: float = None
        self.z: float = None
        self.r: float = None

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        z: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``CylinderParallelY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-y-axis cylinder center x component.
            z: Parallel-to-y-axis cylinder center z component.
            r: Parallel-to-y-axis cylinder radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERPARALLELY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.z: final[float] = z
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (x, z, r)


class CylinderParallelZ(Surface):
    """
    ``CylinderParallelZ`` represents INP parallel-to-z-axis cylinder surface
    cards.

    ``CylinderParallelZ`` inherits attributes from ``Surface``. It represents
    the INP parallel-to-z-axis cylinder surface card syntax element.

    Attributes:
        x: Parallel-to-z-axis cylinder center x component.
        y: Parallel-to-z-axis cylinder center y component.
        r: Parallel-to-z-axis cylinder radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``CylinderParallelZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-z-axis cylinder center x component.
            y: Parallel-to-z-axis cylinder center y component.
            r: Parallel-to-z-axis cylinder radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERPARALLELZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (x, y, r)


class CylinderOnX(Surface):
    """
    ``CylinderOnX`` represents INP on-x-axis cylinder surface cards.

    ``CylinderOnX`` inherits attributes from ``Surface``. It represents the
    INP on-x-axis surface card syntax element.

    Attributes:
        r: On-x-axis cylinder radius.
    """

    def __init__(
        self, number: int, transform_periodic: int, r: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``CylinderOnX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            r: On-x-axis cylinder radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERONX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (r,)


class CylinderOnY(Surface):
    """
    ``CylinderOnY`` represents INP on-y-axis cylinder surface cards.

    ``CylinderOnY`` inherits attributes from ``Surface``. It represents the
    INP on-x-axis surface card syntax element.

    Attributes:
        r: On-y-axis cylinder radius.
    """

    def __init__(
        self, number: int, transform_periodic: int, r: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``CylinderOnY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            r: On-y-axis cylinder radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERONY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (r,)


class CylinderOnZ(Surface):
    """
    ``CylinderOnZ`` represents INP on-z-axis cylinder surface cards.

    ``CylinderOnZ`` inherits attributes from ``Surface``. It represents the
    INP on-x-axis surface card syntax element.

    Attributes:
        r: On-z-axis cylinder radius.
    """

    def __init__(
        self, number: int, transform_periodic: int, r: float, is_whiteboundary: bool = False, is_reflecting: bool = False
    ):
        """
        ``__init__`` initializes ``CylinderOnZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            r: On-z-axis cylinder radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERONZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (r,)


class ConeParallelX(Surface):
    """
    ``ConeParallelX`` represents INP parallel-to-x-axis cone surface cards.

    ``ConeParallelX`` inherits attributes from ``Surface``. It represents the
    INP parallel-to-x-axis cone surface card syntax element.

    Attributes:
        x: Parallel-to-x-axis cone center x component.
        y: Parallel-to-x-axis cone center y component.
        z: Parallel-to-x-axis cone center z component.
        t_squared: Parallel-to-x-axis cone t^2 coefficent.
        plusminus_1: Parallel-to-x-axis cone sheet selector.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        t_squared: float,
        plusminus_1: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeParallelX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-x-axis cone center x component.
            y: Parallel-to-x-axis cone center y component.
            z: Parallel-to-x-axis cone center z component.
            t_squared: Parallel-to-x-axis cone t^2 coefficent.
            plusminus_1: Parallel-to-x-axis cone sheet selector.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONEPARALLELX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.t_squared: final[float] = t_squared
        self.plusminus_1: final[float] = plusminus_1

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if t_squared is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if plusminus_1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.parameters: final[tuple[float]] = (x, y, z, t_squared, plusminus_1)


class ConeParallelY(Surface):
    """
    ``ConeParallelY`` represents INP parallel-to-y-axis cone surface cards.

    ``ConeParallelY`` inherits attributes from ``Surface``. It represents the
    INP parallel-to-y-axis cone surface card syntax element.

    Attributes:
        x: Parallel-to-y-axis cone center x component.
        y: Parallel-to-y-axis cone center y component.
        z: Parallel-to-y-axis cone center z component.
        t_squared: Parallel-to-y-axis cone t^2 coefficent.
        plusminus_1: Parallel-to-y-axis cone sheet selector.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        t_squared: float,
        plusminus_1: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeParallelY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-y-axis cone center x component.
            y: Parallel-to-y-axis cone center y component.
            z: Parallel-to-y-axis cone center z component.
            t_squared: Parallel-to-y-axis cone t^2 coefficent.
            plusminus_1: Parallel-to-y-axis cone sheet selector.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONEPARALLELY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if t_squared is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if plusminus_1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.t_squared: final[float] = t_squared
        self.plusminus_1: final[float] = plusminus_1

        self.parameters: final[tuple[float]] = (x, y, z, t_squared, plusminus_1)


class ConeParallelZ(Surface):
    """
    ``ConeParallelZ`` represents INP parallel-to-z-axis cone surface cards.

    ``ConeParallelZ`` inherits attributes from ``Surface``. It represents the
    INP parallel-to-z-axis cone surface card syntax element.

    Attributes:
        x: Parallel-to-z-axis cone center x component.
        y: Parallel-to-z-axis cone center y component.
        z: Parallel-to-z-axis cone center z component.
        t_squared: Parallel-to-z-axis cone t^2 coefficent.
        plusminus_1: Parallel-to-z-axis cone sheet selector.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        t_squared: float,
        plusminus_1: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeParallelZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-z-axis cone center x component.
            y: Parallel-to-z-axis cone center y component.
            z: Parallel-to-z-axis cone center z component.
            t_squared: Parallel-to-z-axis cone t^2 coefficent.
            plusminus_1: Parallel-to-z-axis cone sheet selector.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONEPARALLELZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if t_squared is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if plusminus_1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.t_squared: final[float] = t_squared
        self.plusminus_1: final[float] = plusminus_1

        self.parameters: final[tuple[float]] = (x, y, z, t_squared, plusminus_1)


class ConeOnX(Surface):
    """
    ``ConeOnX`` represents INP on-x-axis cone surface cards.

    ``ConeOnX`` inherits attributes from ``Surface``. It represents the
    INP on-x-axis cone surface card syntax element.

    Attributes:
        x: On-x-axis cone center x component.
        t_squared: On-x-axis cone t^2 coefficent.
        plusminus_1: On-x-axis cone sheet selector.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        t_squared: float,
        plusminus_1: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeOnX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: On-x-axis cone center x component.
            t_squared: On-x-axis cone t^2 coefficent.
            plusminus_1: On-x-axis cone sheet selector.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONEONX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if t_squared is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if plusminus_1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.t_squared: final[float] = t_squared
        self.plusminus_1: final[float] = plusminus_1

        self.parameters: final[tuple[float]] = (x, t_squared, plusminus_1)


class ConeOnY(Surface):
    """
    ``ConeOnY`` represents INP on-y-axis cone surface cards.

    ``ConeOnY`` inherits attributes from ``Surface``. It represents the
    INP on-y-axis cone surface card syntax element.

    Attributes:
        y: On-y-axis cone center y component.
        t_squared: On-y-axis cone t^2 coefficent.
        plusminus_1: On-y-axis cone sheet selector.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        y: float,
        t_squared: float,
        plusminus_1: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeOnY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            y: On-y-axis cone center y component.
            t_squared: On-y-axis cone t^2 coefficent.
            plusminus_1: On-y-axis cone sheet selector.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONEONY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if t_squared is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if plusminus_1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.y: final[float] = y
        self.t_squared: final[float] = t_squared
        self.plusminus_1: final[float] = plusminus_1

        self.parameters: final[tuple[float]] = (y, t_squared, plusminus_1)


class ConeOnZ(Surface):
    """
    ``ConeOnZ`` represents INP on-z-axis cone surface cards.

    ``ConeOnZ`` inherits attributes from ``Surface``. It represents the
    INP on-z-axis cone surface card syntax element.

    Attributes:
        z: On-z-axis cone center z component.
        t_squared: On-z-axis cone t^2 coefficent.
        plusminus_1: On-z-axis cone sheet selector.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        z: float,
        t_squared: float,
        plusminus_1: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeOnZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            z: On-z-axis cone center z component.
            t_squared: On-z-axis cone t^2 coefficent.
            plusminus_1: On-z-axis cone sheet selector.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONEONZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if t_squared is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if plusminus_1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.z: final[float] = z
        self.t_squared: final[float] = t_squared
        self.plusminus_1: final[float] = plusminus_1

        self.parameters: final[tuple[float]] = (z, t_squared, plusminus_1)


class QuadraticSpecial(Surface):
    """
    ``QuadraticSpecial`` represents INP oblique special quadratic surface cards.

    ``QuadraticSpecial`` inherits attributes from ``Surface``. It represents the
    INP oblique special quadratic surface card syntax element.

    Attributes:
        a: Oblique special quadratic A coefficent.
        b: Oblique special quadratic B coefficent.
        c: Oblique special quadratic C coefficent.
        d: Oblique special quadratic D coefficent.
        e: Oblique special quadratic E coefficent.
        f: Oblique special quadratic F coefficent.
        g: Oblique special quadratic G coefficent.
        x: Oblique special quadratic center x component.
        y: Oblique special quadratic center y component.
        z: Oblique special quadratic center z component.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        a: float,
        b: float,
        c: float,
        d: float,
        e: float,
        f: float,
        g: float,
        x: float,
        y: float,
        z: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``QuadraticSpecial``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            a: Oblique special quadratic A coefficent.
            b: Oblique special quadratic B coefficent.
            c: Oblique special quadratic C coefficent.
            d: Oblique special quadratic D coefficent.
            e: Oblique special quadratic E coefficent.
            f: Oblique special quadratic F coefficent.
            g: Oblique special quadratic G coefficent.
            x: Oblique special quadratic center x component.
            y: Oblique special quadratic center y component.
            z: Oblique special quadratic center z component.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.QUADRATICSPECIAL
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if a is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if b is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if c is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if d is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if e is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if f is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if g is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.a: final[float] = a
        self.b: final[float] = b
        self.c: final[float] = c
        self.d: final[float] = d
        self.e: final[float] = e
        self.f: final[float] = f
        self.g: final[float] = g
        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z

        self.parameters: final[tuple[float]] = (a, b, c, d, e, f, g, x, y, z)


class QuadraticGeneral(Surface):
    """
    ``QuadraticGeneral`` represents INP parrallel-to-axis general quadratic
    surface cards.

    ``QuadraticGeneral`` inherits attributes from ``Surface``. It represents
    the INP parrallel-to-axis general quadratic surface card syntax element.

    Attributes:
        a: Oblique special quadratic A coefficent.
        b: Oblique special quadratic B coefficent.
        c: Oblique special quadratic C coefficent.
        d: Oblique special quadratic D coefficent.
        e: Oblique special quadratic E coefficent.
        f: Oblique special quadratic F coefficent.
        g: Oblique special quadratic G coefficent.
        h: Oblique special quadratic H coefficent.
        j: Oblique special quadratic J coefficent.
        k: Oblique special quadratic K coefficent.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        a: float,
        b: float,
        c: float,
        d: float,
        e: float,
        f: float,
        g: float,
        h: float,
        j: float,
        k: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``QuadraticGeneral``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            a: Oblique special quadratic A coefficent.
            b: Oblique special quadratic B coefficent.
            c: Oblique special quadratic C coefficent.
            d: Oblique special quadratic D coefficent.
            e: Oblique special quadratic E coefficent.
            f: Oblique special quadratic F coefficent.
            g: Oblique special quadratic G coefficent.
            h: Oblique special quadratic H coefficent.
            j: Oblique special quadratic J coefficent.
            k: Oblique special quadratic K coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.QUADRATICGENERAL
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if a is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if b is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if c is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if d is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if e is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if f is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if g is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if h is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if j is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if k is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.a: final[float] = a
        self.b: final[float] = b
        self.c: final[float] = c
        self.d: final[float] = d
        self.e: final[float] = e
        self.f: final[float] = f
        self.g: final[float] = g
        self.h: final[float] = h
        self.j: final[float] = j
        self.k: final[float] = k

        self.parameters: final[tuple[float]] = (a, b, c, d, e, f, g, h, j, k)


class TorusParallelX(Surface):
    """
    ``TorusParallelX`` represents INP parallel-to-x-axis tori surface cards.

    ``TorusParallelX`` inherits attributes from ``Surface``. It represents the
    INP parallel-to-x-axis tori surface card syntax element.

    Attributes:
        x: Parallel-to-x-axis tori center x component.
        y: Parallel-to-x-axis tori center y component.
        z: Parallel-to-x-axis tori center z component.
        a: Parallel-to-x-axis tori A coefficent.
        b: Parallel-to-x-axis tori B coefficent.
        c: Parallel-to-x-axis tori C coefficent.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``TorusParallelX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-x-axis tori center x component.
            y: Parallel-to-x-axis tori center y component.
            z: Parallel-to-x-axis tori center z component.
            a: Parallel-to-x-axis tori A coefficent.
            b: Parallel-to-x-axis tori B coefficent.
            c: Parallel-to-x-axis tori C coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.TORUSPARALLELX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if b is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if c is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.a: final[float] = a
        self.b: final[float] = b
        self.c: final[float] = c

        self.parameters: final[tuple[float]] = (x, y, z, a, b, c)


class TorusParallelY(Surface):
    """
    ``TorusParallelY`` represents INP parallel-to-y-axis tori surface cards.

    ``TorusParallelY`` inherits attributes from ``Surface``. It represents the
    INP parallel-to-y-axis tori surface card syntax element.

    Attributes:
        x: Parallel-to-y-axis tori center x component.
        y: Parallel-to-y-axis tori center y component.
        z: Parallel-to-y-axis tori center z component.
        a: Parallel-to-y-axis tori A coefficent.
        b: Parallel-to-y-axis tori B coefficent.
        c: Parallel-to-y-axis tori C coefficent.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``TorusParallelY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-y-axis tori center x component.
            y: Parallel-to-y-axis tori center y component.
            z: Parallel-to-y-axis tori center z component.
            a: Parallel-to-y-axis tori A coefficent.
            b: Parallel-to-y-axis tori B coefficent.
            c: Parallel-to-y-axis tori C coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.TORUSPARALLELY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if b is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if c is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.a: final[float] = a
        self.b: final[float] = b
        self.c: final[float] = c

        self.parameters: final[tuple[float]] = (x, y, z, a, b, c)


class TorusParallelZ(Surface):
    """
    ``TorusParallelZ`` represents INP parallel-to-z-axis tori surface cards.

    ``TorusParallelZ`` inherits attributes from ``Surface``. It represents the
    INP parallel-to-z-axis tori surface card syntax element.

    Attributes:
        x: Parallel-to-z-axis tori center x component.
        y: Parallel-to-z-axis tori center y component.
        z: Parallel-to-z-axis tori center z component.
        a: Parallel-to-z-axis tori A coefficent.
        b: Parallel-to-z-axis tori B coefficent.
        c: Parallel-to-z-axis tori C coefficent.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``TorusParallelZ``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x: Parallel-to-z-axis tori center x component.
            y: Parallel-to-z-axis tori center y component.
            z: Parallel-to-z-axis tori center z component.
            a: Parallel-to-z-axis tori A coefficent.
            b: Parallel-to-z-axis tori B coefficent.
            c: Parallel-to-z-axis tori C coefficent.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.TORUSPARALLELZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if b is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if c is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x: final[float] = x
        self.y: final[float] = y
        self.z: final[float] = z
        self.a: final[float] = a
        self.b: final[float] = b
        self.c: final[float] = c

        self.parameters: final[tuple[float]] = (x, y, z, a, b, c)


class SurfaceX(Surface):
    """
    ``SurfaceX`` represents INP x-axisymmetric point-defined surface cards.

    ``SurfaceX`` inherits attributes from ``Surface``. It represents the
    INP x-axisymmetric point-defined surface card syntax element.

    Attributes:
        x1: X-axisymmetric point-defined surface point #1 x component.
        r1: X-axisymmetric point-defined surface point #1 radius.
        x2: X-axisymmetric point-defined surface point #2 x component.
        r2: X-axisymmetric point-defined surface point #2 radius.
        x3: X-axisymmetric point-defined surface point #3 x component.
        r3: X-axisymmetric point-defined surface point #3 radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        x1: float,
        r1: float,
        x2: float = None,
        r2: float = None,
        x3: float = None,
        r3: float = None,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SurfaceX``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            x1: X-axisymmetric point-defined surface point #1 x component.
            r1: X-axisymmetric point-defined surface point #1 radius.
            x2: X-axisymmetric point-defined surface point #2 x component.
            r2: X-axisymmetric point-defined surface point #2 radius.
            x3: X-axisymmetric point-defined surface point #3 x component.
            r3: X-axisymmetric point-defined surface point #3 radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SURFACEX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if x1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if x2 is not None and r2 is not None:
            if x2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if r2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if x3 is not None and r3 is not None:
                if x3 is None:
                    raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

                if r3 is None:
                    raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.x1: final[float] = x1
        self.r1: final[float] = r1
        self.x2: final[float] = x2 if x2 is not None else None
        self.r2: final[float] = r2 if r2 is not None else None
        self.x3: final[float] = x3 if x3 is not None else None
        self.r3: final[float] = r3 if r3 is not None else None

        self.parameters = (x1, r1, x2, r2, x3, r3)


class SurfaceY(Surface):
    """
    ``SurfaceY`` represents INP y-axisymmetric point-defined surface cards.

    ``SurfaceY`` inherits attributes from ``Surface``. It represents the
    INP y-axisymmetric point-defined surface card syntax element.

    Attributes:
        y1: Y-axisymmetric point-defined surface point #1 y component.
        r1: Y-axisymmetric point-defined surface point #1 radius.
        y2: Y-axisymmetric point-defined surface point #2 y component.
        r2: Y-axisymmetric point-defined surface point #2 radius.
        y3: Y-axisymmetric point-defined surface point #3 y component.
        r3: Y-axisymmetric point-defined surface point #3 radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        y1: float,
        r1: float,
        y2: float = None,
        r2: float = None,
        y3: float = None,
        r3: float = None,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SurfaceY``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            y1: Y-axisymmetric point-defined surface point #1 y component.
            r1: Y-axisymmetric point-defined surface point #1 radius.
            y2: Y-axisymmetric point-defined surface point #2 y component.
            r2: Y-axisymmetric point-defined surface point #2 radius.
            y3: Y-axisymmetric point-defined surface point #3 y component.
            r3: Y-axisymmetric point-defined surface point #3 radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SURFACEY
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if y1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if y2 is not None and r2 is not None:
            if y2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if r2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if y3 is not None and r3 is not None:
                if y3 is None:
                    raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

                if r3 is None:
                    raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.y1: final[float] = y1
        self.r1: final[float] = r1
        self.y2: final[float] = y2 if y2 is not None else None
        self.r2: final[float] = r2 if r2 is not None else None
        self.y3: final[float] = y3 if y3 is not None else None
        self.r3: final[float] = r3 if r3 is not None else None

        self.parameters: final[tuple[float]] = (y1, r1, y2, r2, y3, r3)


class SurfaceZ(Surface):
    """
    ``SurfaceZ`` represents INP z-axisymmetric point-defined surface cards.

    ``SurfaceZ`` inherits attributes from ``Surface``. It represents the
    INP z-axisymmetric point-defined surface card syntax element.

    Attributes:
        z1: Z-axisymmetric point-defined surface point #1 z component.
        r1: Z-axisymmetric point-defined surface point #1 radius.
        z2: Z-axisymmetric point-defined surface point #2 z component.
        r2: Z-axisymmetric point-defined surface point #2 radius.
        z3: Z-axisymmetric point-defined surface point #3 z component.
        r3: Z-axisymmetric point-defined surface point #3 radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        z1: float,
        r1: float,
        z2: float = None,
        r2: float = None,
        z3: float = None,
        r3: float = None,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``SurfaceZ``.

        Parameters:
            z1: Z-axisymmetric point-defined surface point #1 z component.
            r1: Z-axisymmetric point-defined surface point #1 radius.
            z2: Z-axisymmetric point-defined surface point #2 z component.
            r2: Z-axisymmetric point-defined surface point #2 radius.
            z3: Z-axisymmetric point-defined surface point #3 z component.
            r3: Z-axisymmetric point-defined surface point #3 radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SURFACEZ
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if z1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if z2 is not None and r2 is not None:
            if z2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if r2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if z3 is not None and r3 is not None:
                if z3 is None:
                    raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

                if r3 is None:
                    raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.z1: final[float] = z1
        self.r1: final[float] = r1
        self.z2: final[float] = z2 if z2 is not None else None
        self.r2: final[float] = r2 if r2 is not None else None
        self.z3: final[float] = z3 if z3 is not None else None
        self.r3: final[float] = r3 if r3 is not None else None

        self.parameters: final[tuple[float]] = (z1, r1, z2, r2, z3, r3)


class Box(Surface):
    """
    ``Box`` represents INP arbitrarily oriented orthogonal box macrobody
    surface cards.

    ``Box`` inherits attributes from ``Surface``. It represents the
    INP arbitrarily oriented orthogonal box macrobody surface card syntax
    element.

    Attributes:
        vx: Box macrobody position vector x component.
        vy: Box macrobody position vector y component.
        vz: Box macrobody position vector z component.
        a1x: Box macrobody vector #1 x component.
        a1y: Box macrobody vector #1 y component.
        a1z: Box macrobody vector #1 z component.
        a2x: Box macrobody vector #2 x component.
        a2y: Box macrobody vector #2 y component.
        a2z: Box macrobody vector #2 z component.
        a3x: Box macrobody vector #3 x component.
        a3y: Box macrobody vector #3 y component.
        a3z: Box macrobody vector #3 z component.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        a1x: float,
        a1y: float,
        a1z: float,
        a2x: float,
        a2y: float,
        a2z: float,
        a3x: float = None,
        a3y: float = None,
        a3z: float = None,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Box``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Box macrobody position vector x component.
            vy: Box macrobody position vector y component.
            vz: Box macrobody position vector z component.
            a1x: Box macrobody vector #1 x component.
            a1y: Box macrobody vector #1 y component.
            a1z: Box macrobody vector #1 z component.
            a2x: Box macrobody vector #2 x component.
            a2y: Box macrobody vector #2 y component.
            a2z: Box macrobody vector #2 z component.
            a3x: Box macrobody vector #3 x component.
            a3y: Box macrobody vector #3 y component.
            a3z: Box macrobody vector #3 z component.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.BOX
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a1x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a1y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a1z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a2x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a2y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a2z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if a3x is not None or a3y is not None or a3z is not None:
            if a3x is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if a3y is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if a3z is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.a1x: final[float] = a1x
        self.a1y: final[float] = a1y
        self.a1z: final[float] = a1z
        self.a2x: final[float] = a2x
        self.a2y: final[float] = a2y
        self.a2z: final[float] = a2z
        self.a3x: final[float] = a3x if a3x is not None else None
        self.a3y: final[float] = a3y if a3y is not None else None
        self.a3z: final[float] = a3z if a3z is not None else None

        self.parameters: final[tuple[float]] = (vx, vy, vz, a1x, a1y, a1z, a2x, a2y, a2z, a3x, a3y, a3z)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        v = _cadquery.CqVector(self.vx, self.vy, self.vz)
        a1 = _cadquery.CqVector(self.a1x, self.a1y, self.a1z)
        a2 = _cadquery.CqVector(self.a2x, self.a2y, self.a2z)
        a3 = _cadquery.CqVector(self.a3x, self.a3y, self.a3z)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_box(a1, a2, a3)
        cadquery += _cadquery.add_translation(v)

        return cadquery + "\n"


class Parallelepiped(Surface):
    """
    ``Parallelepiped`` represents INP rectangular parallelepiped macrobody
    surface cards.

    ``Parallelepiped`` inherits attributes from ``Surface``. It represents the
    INP rectangular parallelepiped macrobody surface card syntax element.

    Attributes:
        xmin: Parallelepiped x termini minimum.
        xmax: Parallelepiped x termini maximum.
        ymin: Parallelepiped y termini minimum.
        ymax: Parallelepiped y termini maximum.
        zmin: Parallelepiped z termini minimum.
        zmax: Parallelepiped z termini maximum.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        zmin: float,
        zmax: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Parallelepiped``.

        Parameters:
            xmin: Parallelepiped x termini minimum.
            xmax: Parallelepiped x termini maximum.
            ymin: Parallelepiped y termini minimum.
            ymax: Parallelepiped y termini maximum.
            zmin: Parallelepiped z termini minimum.
            zmax: Parallelepiped z termini maximum.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.PARALLELEPIPED
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if xmin is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if xmax is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if ymin is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if ymax is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if zmin is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if zmax is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.xmin: final[float] = xmin
        self.xmax: final[float] = xmax
        self.ymin: final[float] = ymin
        self.ymax: final[float] = ymax
        self.zmin: final[float] = zmin
        self.zmax: final[float] = zmax

        self.parameters: final[tuple[float]] = (xmin, xmax, ymin, ymax, zmin, zmax)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        xlen, ylen, zlen = (
            math.fabs(self.xmax - self.xmin),
            math.fabs(self.ymax - self.ymin),
            math.fabs(self.zmax - self.zmin),
        )

        x = _cadquery.CqVector(xlen, 0, 0)
        y = _cadquery.CqVector(0, ylen, 0)
        z = _cadquery.CqVector(0, 0, zlen)
        v = _cadquery.CqVector(self.xmin + xlen / 2, self.ymin + ylen / 2, self.zmin + zlen / 2)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_box(x, y, z)
        cadquery += _cadquery.add_translation(v)

        return cadquery + "\n"


class Sphere(Surface):
    """
    ``Sphere`` represents INP sphere macrobody surface cards.

    ``Sphere`` inherits attributes from ``Surface``. It represents the
    INP sphere macrobody surface card syntax element.

    Attributes:
        vx: Sphere macrobody position vector x component.
        vy: Sphere macrobody position vector y component.
        vz: Sphere macrobody position vector z component.
        r: Sphere macrobody radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Sphere``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Sphere macrobody position vector x component.
            vy: Sphere macrobody position vector y component.
            vz: Sphere macrobody position vector z component.
            r: Sphere macrobody radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.SPHERE
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (vx, vy, vz, r)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_sphere(self.r)
        cadquery += _cadquery.add_translation(self.vx, self.vy, self.vz)

        return cadquery


class CylinderCircular(Surface):
    """
    ``CylinderCircular`` represents INP right circular cylinder macrobody
    surface cards.

    ``CylinderCircular`` inherits attributes from ``Surface``. It represents
    the INP right circular cylinder surface card syntax element.

    Attributes:
        vx: Circular cylinder macrobody position vector x component.
        vy: Circular cylinder macrobody position vector y component.
        vz: Circular cylinder macrobody position vector z component.
        hx: Circular cylinder macrobody height vector x component.
        hy: Circular cylinder macrobody height vector y component.
        hz: Circular cylinder macrobody height vector z component.
        r: Circular cylinder macrobody radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        hx: float,
        hy: float,
        hz: float,
        r: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``CylinderCircular``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Circular cylinder macrobody position vector x component.
            vy: Circular cylinder macrobody position vector y component.
            vz: Circular cylinder macrobody position vector z component.
            hx: Circular cylinder macrobody height vector x component.
            hy: Circular cylinder macrobody height vector y component.
            hz: Circular cylinder macrobody height vector z component.
            r: Circular cylinder macrobody radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERCIRCULAR
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.hx: final[float] = hx
        self.hy: final[float] = hy
        self.hz: final[float] = hz
        self.r: final[float] = r

        self.parameters: final[tuple[float]] = (vx, vy, vz, hx, hy, hz, r)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        h = _cadquery.CqVector(self.hx, self.hy, self.hz)
        v = _cadquery.CqVector(self.vx, self.vy, self.vz / 2)
        k = _cadquery.CqVector(0, 0, 1)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_cylinder_circle(h.norm(), self.r)

        if self.hx != 0 or self.hy != 0 or self.hz / self.hz != 1:
            cadquery += _cadquery.add_rotation(_cadquery.CqVector.cross(k, h), _cadquery.CqVector.angle(k, h))

        cadquery += _cadquery.add_translation(v)

        return cadquery


class HexagonalPrism(Surface):
    """
    ``HexagonalPrism`` represents INP right hexagonal prism macrobody surface
    cards.

    ``HexagonalPrism`` inherits attributes from ``Surface``. It represents the
    INP right hexagonal prism macrobody surface card syntax element.

    Attributes:
        vx: Hexagonal prism position vector x component.
        vy: Hexagonal prism position vector y component.
        vz: Hexagonal prism position vector z component.
        hx: Hexagonal prism height vector x component.
        hy: Hexagonal prism height vector y component.
        hz: Hexagonal prism height vector z component.
        r1: Hexagonal prism facet #1 vector x component.
        r2: Hexagonal prism facet #1 vector y component.
        r3: Hexagonal prism facet #1 vector z component.
        s1: Hexagonal prism facet #2 vector x component.
        s2: Hexagonal prism facet #2 vector y component.
        s3: Hexagonal prism facet #2 vector z component.
        t1: Hexagonal prism facet #3 vector x component.
        t2: Hexagonal prism facet #3 vector y component.
        t3: Hexagonal prism facet #3 vector z component.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        hx: float,
        hy: float,
        hz: float,
        r1: float,
        r2: float,
        r3: float,
        s1: float = None,
        s2: float = None,
        s3: float = None,
        t1: float = None,
        t2: float = None,
        t3: float = None,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``HexagonalPrism``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Hexagonal prism position vector x component.
            vy: Hexagonal prism position vector y component.
            vz: Hexagonal prism position vector z component.
            hx: Hexagonal prism height vector x component.
            hy: Hexagonal prism height vector y component.
            hz: Hexagonal prism height vector z component.
            r1: Hexagonal prism facet #1 vector x component.
            r2: Hexagonal prism facet #1 vector y component.
            r3: Hexagonal prism facet #1 vector z component.
            s1: Hexagonal prism facet #2 vector x component.
            s2: Hexagonal prism facet #2 vector y component.
            s3: Hexagonal prism facet #2 vector z component.
            t1: Hexagonal prism facet #3 vector x component.
            t2: Hexagonal prism facet #3 vector y component.
            t3: Hexagonal prism facet #3 vector z component.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.HEXAGONALPRISM
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r2 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r3 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if s1 is not None or s2 is not None or s3 is not None or t1 is not None or t2 is not None or t3 is not None:
            if s1 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if s2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if s3 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if t1 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if t2 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if t3 is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.hx: final[float] = hx
        self.hy: final[float] = hy
        self.hz: final[float] = hz
        self.r1: final[float] = r1
        self.r2: final[float] = r2
        self.r3: final[float] = r3
        self.s1: final[float] = s1 if s1 is not None else None
        self.s2: final[float] = s2 if s2 is not None else None
        self.s3: final[float] = s3 if s3 is not None else None
        self.t1: final[float] = t1 if t1 is not None else None
        self.t2: final[float] = t2 if t2 is not None else None
        self.t3: final[float] = t3 if t3 is not None else None

        self.parameters: final[tuple[float]] = (vx, vy, vz, hx, hy, hz, r1, r2, r3, s1, s2, s3, t1, t2, t3)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        v = _cadquery.CqVector(self.vx, self.vy, self.vz)
        h = _cadquery.CqVector(self.hx, self.hy, self.hz)
        r = _cadquery.CqVector(self.r1, self.r2, self.r3)
        k = _cadquery.CqVector(0, 0, 1)
        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_prism_polygon(h.norm(), r.apothem())

        if self.hx != 0 or self.hy != 0 or self.hz / self.hz != 1:
            cadquery += _cadquery.add_rotation(_cadquery.CqVector.cross(k, h), _cadquery.CqVector.angle(k, h))

        cadquery += _cadquery.add_translation(v)

        return cadquery


class CylinderElliptical(Surface):
    """
    ``CylinderElliptical`` represents INP right elliptical cylinder macrobody
    surface cards.

    ``CylinderElliptical`` inherits attributes from ``Surface``. It represents
    the INP right elliptical cylinder macrobody surface card syntax element.

    Attributes:
        vx: Elliptical cylinder position vector x component.
        vy: Elliptical cylinder position vector y component.
        vz: Elliptical cylinder position vector z component.
        hx: Elliptical cylinder height vector x component.
        hy: Elliptical cylinder height vector y component.
        hz: Elliptical cylinder height vector z component.
        v1x: Elliptical cylinder major axis vector x component.
        v1y: Elliptical cylinder major axis vector y component.
        v1z: Elliptical cylinder major axis vector z component.
        v2x: Elliptical cylinder minor axis vector x component.
        v2y: Elliptical cylinder minor axis vector y component.
        v2z: Elliptical cylinder minor axis vector z component.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        hx: float,
        hy: float,
        hz: float,
        v1x: float,
        v1y: float,
        v1z: float,
        v2x: float,
        v2y: float = None,
        v2z: float = None,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``CylinderElliptical``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Elliptical cylinder position vector x component.
            vy: Elliptical cylinder position vector y component.
            vz: Elliptical cylinder position vector z component.
            hx: Elliptical cylinder height vector x component.
            hy: Elliptical cylinder height vector y component.
            hz: Elliptical cylinder height vector z component.
            v1x: Elliptical cylinder major axis vector x component.
            v1y: Elliptical cylinder major axis vector y component.
            v1z: Elliptical cylinder major axis vector z component.
            v2x: Elliptical cylinder minor axis vector x component.
            v2y: Elliptical cylinder minor axis vector y component.
            v2z: Elliptical cylinder minor axis vector z component.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CYLINDERELLIPTICAL
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2y is not None or v2z is not None:
            if v2y is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

            if v2z is None:
                raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.hx: final[float] = hx
        self.hy: final[float] = hy
        self.hz: final[float] = hz
        self.v1x: final[float] = v1x
        self.v1y: final[float] = v1y
        self.v1z: final[float] = v1z
        self.v2x: final[float] = v2x

        self.v2y: final[float] = v2y
        self.v2z: final[float] = v2z

        self.parameters: final[tuple[float]] = (vx, vy, vz, hx, hy, hz, v1x, v1y, v1z, v2x, v2y, v2z)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        k = _cadquery.CqVector(0, 0, 1)
        v = _cadquery.CqVector(self.vx, self.vy, self.vz)
        h = _cadquery.CqVector(self.hx, self.hy, self.hz)
        v1 = _cadquery.CqVector(self.v1x, self.v1y, self.v1z)
        v2 = _cadquery.CqVector(self.v2x, self.v2y, self.v2z)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()."
        cadquery += _cadquery.add_cylinder_ellipse(h.norm(), v1.norm(), v2.norm())

        if self.hx != 0 or self.hy != 0 or self.hz / self.hz != 1:
            cadquery += _cadquery.add_rotation(_cadquery.CqVector.cross(k, h), _cadquery.CqVector.angle(k, h))

        cadquery += _cadquery.add_translation(v)

        return cadquery


class ConeTruncated(Surface):
    """
    ``ConeTruncated`` represents INP truncated right-angled cone macrobody
    urface cards.

    ``ConeTruncated`` inherits attributes from ``Surface``. It represents the
    INP truncated right-angled cone macrobody surface card syntax element.

    Attributes:
        vx: Truncated cone position vector x component.
        vy: Truncated cone position vector y component.
        vz: Truncated cone position vector z component.
        hx: Truncated cone height vector x component.
        hy: Truncated cone height vector y component.
        hz: Truncated cone height vector z component.
        r1: Truncated cone lower cone radius.
        r2: Truncated cone upper cone radius.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        hx: float,
        hy: float,
        hz: float,
        r1: float,
        r2: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``ConeTruncated``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Truncated cone position vector x component.
            vy: Truncated cone position vector y component.
            vz: Truncated cone position vector z component.
            hx: Truncated cone height vector x component.
            hy: Truncated cone height vector y component.
            hz: Truncated cone height vector z component.
            r1: Truncated cone lower cone radius.
            r2: Truncated cone upper cone radius.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.CONETRUNCATED
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if r2 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.hx: final[float] = hx
        self.hy: final[float] = hy
        self.hz: final[float] = hz
        self.r1: final[float] = r1
        self.r2: final[float] = r2

        self.parameters: final[tuple[float]] = (vx, vy, vz, hx, hy, hz, r1, r2)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        k = _cadquery.CqVector(0, 0, 1)
        v = _cadquery.CqVector(self.vx, self.vy, self.vz)
        h = _cadquery.CqVector(self.hx, self.hy, self.hz)
        v1 = _cadquery.CqVector(self.v1x, self.v1y, self.v1z)
        v2 = _cadquery.CqVector(self.v2x, self.v2y, self.v2z)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_cone_truncated(h.norm(), v1.norm(), v2.norm())

        if self.hx != 0 or self.hy != 0 or self.hz / self.hz != 1:
            cadquery += _cadquery.add_rotation(_cadquery.CqVector.cross(k, h), _cadquery.CqVector.angle(k, h))

        cadquery += _cadquery.add_translation(v)

        return cadquery


class Ellipsoid(Surface):
    """
    ``Ellipsoid`` represents INP ellipsoid surface cards.

    ``Ellipsoid`` inherits attributes from ``Surface``. It represents the
    INP ellipsoid surface card syntax element.

    Attributes:
        v1x: Ellipsoid focus #1 or center x component.
        v1y: Ellipsoid focus #1 or center y component.
        v1z: Ellipsoid focus #1 or center z component.
        v2x: Ellipsoid focus #2 or major axis x component.
        v2y: Ellipsoid focus #2 or major axis y component.
        v2z: Ellipsoid focus #2 or major axis z component.
        rm: Ellipsoid major/minor axis radius length.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        v1x: float,
        v1y: float,
        v1z: float,
        v2x: float,
        v2y: float,
        v2z: float,
        rm: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Ellipsoid``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            v1x: Ellipsoid focus #1 or center x component.
            v1y: Ellipsoid focus #1 or center y component.
            v1z: Ellipsoid focus #1 or center z component.
            v2x: Ellipsoid focus #2 or major axis x component.
            v2y: Ellipsoid focus #2 or major axis y component.
            v2z: Ellipsoid focus #2 or major axis z component.
            rm: Ellipsoid major/minor axis radius length.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.ELLIPSOID
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if v1x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if rm is None or (rm == 0):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.v1x: final[float] = v1x
        self.v1y: final[float] = v1y
        self.v1z: final[float] = v1z
        self.v2x: final[float] = v2x
        self.v2y: final[float] = v2y
        self.v2z: final[float] = v2z
        self.rm: final[float] = rm

        self.parameters: final[tuple[float]] = (v1x, v1y, v1z, v2x, v2y, v2z, rm)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        j = _cadquery.CqVector(0, 1, 0)
        v1 = _cadquery.CqVector(self.v1x, self.v1y, self.v1z)
        v2 = _cadquery.CqVector(self.v2x, self.v2y, self.v2z)

        if self.rm > 0:
            a = _cadquery.CqVector.cross(j, v2 - v1)
            angle = _cadquery.CqVector.angle(j, v2 - v1)
            v = _cadquery.CqVector((self.v2x - self.v1x) / 2, (self.v2y - self.v1y) / 2 - a, (self.v2z - self.v1z) / 2) + v1
        else:
            a = _cadquery.CqVector.cross(j, v2)
            angle = _cadquery.CqVector.angle(j, v2)
            v = _cadquery.CqVector(v1.x, v1.y - a.y, v1.z)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += f"surface_{self.number} = cq.Workplane()"
        cadquery += _cadquery.add_ellipsoid(a.norm(), self.rm)
        cadquery += _cadquery.add_rotation(a, angle)
        cadquery += _cadquery.add_translation(v)

        return cadquery


class Wedge(Surface):
    """
    ``Wedge`` represents INP wedge surface cards.

    ``Wedge`` inherits attributes from ``Surface``. It represents the
    INP wedge surface card syntax element.

    Attributes:
        vx: Wedge position vector x component.
        vy: Wedge position vector y component.
        vz: Wedge position vector z component.
        v1x: Wedge side vector #1 x component.
        v1y: Wedge side vector #1 y component.
        v1z: Wedge side vector #1 z component.
        v2x: Wedge side vector #2 x component.
        v2y: Wedge side vector #2 y component.
        v2z: Wedge side vector #2 z component.
        v3x: Wedge height vector x component.
        v3y: Wedge height vector y component.
        v3z: Wedge height vector z component.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        vx: float,
        vy: float,
        vz: float,
        v1x: float,
        v1y: float,
        v1z: float,
        v2x: float,
        v2y: float,
        v2z: float,
        v3x: float,
        v3y: float,
        v3z: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Wedge``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            vx: Wedge position vector x component.
            vy: Wedge position vector y component.
            vz: Wedge position vector z component.
            v1x: Wedge side vector #1 x component.
            v1y: Wedge side vector #1 y component.
            v1z: Wedge side vector #1 z component.
            v2x: Wedge side vector #2 x component.
            v2y: Wedge side vector #2 y component.
            v2z: Wedge side vector #2 z component.
            v3x: Wedge height vector x component.
            v3y: Wedge height vector y component.
            v3z: Wedge height vector z component.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.WEDGE
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if vx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if vz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v1z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v2z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v3x is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v3y is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if v3z is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.vx: final[float] = vx
        self.vy: final[float] = vy
        self.vz: final[float] = vz
        self.v1x: final[float] = v1x
        self.v1y: final[float] = v1y
        self.v1z: final[float] = v1z
        self.v2x: final[float] = v2x
        self.v2y: final[float] = v2y
        self.v2z: final[float] = v2z
        self.v3x: final[float] = v3x
        self.v3y: final[float] = v3y
        self.v3z: final[float] = v3z

        self.parameters: final[tuple[float]] = (vx, vy, vz, v1x, v1y, v1z, v2x, v2y, v2z, v3x, v3y, v3z)

    def to_cadquery(self, hasHeader: bool = False) -> str:
        """
        ``to_cadquery`` generates cadquery from INP surface card objects.

        ``to_cadquery`` provides a Cadquery endpoints for writing Cadquery
        source strings and later displaying geometries.

        Parameters:
            hasHeader: Boolean to include cadquery header.

        Returns:
            Cadquery for surface card object.
        """

        v = _caddquery.CqVectro(self.vx, self.vy, self.vz)
        v1 = _cadquery.CqVector(self.v1x, self.v1y, self.v1z)
        v2 = _cadquery.CqVector(self.v2x, self.v2y, self.v2z)
        v3 = _cadquery.CqVector(self.v3x, self.v3y, self.v3z)

        cadquery = "import cadquery as cq\n\n" if hasHeader else ""
        cadquery += add_wedge(v1, v2, v3)
        cadquery += add_translation(v)

        return cadquery


class Polyhedron(Surface):
    """
    ``Polyhedron`` represents INP arbitrary polyhedron surface cards.

    ``Polyhedron`` inherits attributes from ``Surface``. It represents the
    INP arbitrary polyhedron surface card syntax element.

    Attributes:
        ax: Polyhedron corner #1 x component.
        ay: Polyhedron corner #1 y component.
        az: Polyhedron corner #1 z component.
        bx: Polyhedron corner #2 x component.
        by: Polyhedron corner #2 y component.
        bz: Polyhedron corner #2 z component.
        cx: Polyhedron corner #3 x component.
        cy: Polyhedron corner #3 y component.
        cz: Polyhedron corner #3 z component.
        dx: Polyhedron corner #4 x component.
        dy: Polyhedron corner #4 y component.
        dz: Polyhedron corner #4 z component.
        ex: Polyhedron corner #5 x component.
        ey: Polyhedron corner #5 y component.
        ez: Polyhedron corner #5 z component.
        fx: Polyhedron corner #6 x component.
        fy: Polyhedron corner #6 y component.
        fz: Polyhedron corner #6 z component.
        gx: Polyhedron corner #7 x component.
        gy: Polyhedron corner #7 y component.
        gz: Polyhedron corner #7 z component.
        hx: Polyhedron corner #8 x component.
        hy: Polyhedron corner #8 y component.
        hz: Polyhedron corner #8 z component.
        n1: Polyhedron four-digit side specificer #1.
        n2: Polyhedron four-digit side specificer #2.
        n3: Polyhedron four-digit side specificer #3.
        n4: Polyhedron four-digit side specificer #4.
        n5: Polyhedron four-digit side specificer #5.
        n6: Polyhedron four-digit side specificer #6.
    """

    def __init__(
        self,
        number: int,
        transform_periodic: int,
        ax: float,
        ay: float,
        az: float,
        bx: float,
        by: float,
        bz: float,
        cx: float,
        cy: float,
        cz: float,
        dx: float,
        dy: float,
        dz: float,
        ex: float,
        ey: float,
        ez: float,
        fx: float,
        fy: float,
        fz: float,
        gx: float,
        gy: float,
        gz: float,
        hx: float,
        hy: float,
        hz: float,
        n1: float,
        n2: float,
        n3: float,
        n4: float,
        n5: float,
        n6: float,
        is_whiteboundary: bool = False,
        is_reflecting: bool = False,
    ):
        """
        ``__init__`` initializes ``Polyhedron``.

        ``__init__`` checks given arguments before assigning the given
        value to their cooresponding attributes. If given an unrecognized
        argument, it raises semantic errors.

        Parameters:
            ax: Polyhedron corner #1 x component.
            ay: Polyhedron corner #1 y component.
            az: Polyhedron corner #1 z component.
            bx: Polyhedron corner #2 x component.
            by: Polyhedron corner #2 y component.
            bz: Polyhedron corner #2 z component.
            cx: Polyhedron corner #3 x component.
            cy: Polyhedron corner #3 y component.
            cz: Polyhedron corner #3 z component.
            dx: Polyhedron corner #4 x component.
            dy: Polyhedron corner #4 y component.
            dz: Polyhedron corner #4 z component.
            ex: Polyhedron corner #5 x component.
            ey: Polyhedron corner #5 y component.
            ez: Polyhedron corner #5 z component.
            fx: Polyhedron corner #6 x component.
            fy: Polyhedron corner #6 y component.
            fz: Polyhedron corner #6 z component.
            gx: Polyhedron corner #7 x component.
            gy: Polyhedron corner #7 y component.
            gz: Polyhedron corner #7 z component.
            hx: Polyhedron corner #8 x component.
            hy: Polyhedron corner #8 y component.
            hz: Polyhedron corner #8 z component.
            n1: Polyhedron four-digit side specificer #1.
            n2: Polyhedron four-digit side specificer #2.
            n3: Polyhedron four-digit side specificer #3.
            n4: Polyhedron four-digit side specificer #4.
            n5: Polyhedron four-digit side specificer #5.
            n6: Polyhedron four-digit side specificer #6.

        Raises:
            MCNPSemanticError: INVALID_SURFACE_NUMBER.
            MCNPSemanticError: INVALID_SURFACE_TRANSFORMPERIODIC.
            MCNPSemanticError: INVALID_SURFACE_WHITEBOUNDARY.
            MCNPSemanticError: INVALID_SURFACE_REFLECTING.
            MCNPSemanticError: INVALID_SURFACE_PARAMETER.
        """

        if number is None or not (1 <= number <= 99_999_999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_NUMBER)

        if transform_periodic is not None and not (-99_999_999 <= transform_periodic <= 999):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_TRANSFORMPERIODIC)

        if is_whiteboundary is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_WHITEBOUNDARY)

        if is_reflecting is None or (is_reflecting and is_whiteboundary):
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_REFLECTING)

        self.number: final[int] = number
        self.mnemonic: final[SurfaceMnemonic] = Surface.SurfaceMnemonic.POLYHEDRON
        self.transform: final[int] = transform_periodic if transform_periodic > 0 else None
        self.periodic: final[int] = transform_periodic if transform_periodic < 0 else None
        self.is_reflecting: final[bool] = is_reflecting
        self.is_whiteboundary: final[bool] = is_whiteboundary

        if ax is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if ay is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if az is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if bx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if by is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if bz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if cx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if cy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if cz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if dx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if dy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if dz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if ex is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if ey is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if ez is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if fx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if fy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if fz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if gx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if gy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if gz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hx is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hy is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if hz is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if n1 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if n2 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if n3 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if n4 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if n5 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        if n6 is None:
            raise errors.MCNPSemanticError(errors.MCNPSemanticCodes.INVALID_SURFACE_PARAMETER)

        self.ax: final[float] = ax
        self.ay: final[float] = ay
        self.az: final[float] = az
        self.bx: final[float] = bx
        self.by: final[float] = by
        self.bz: final[float] = bz
        self.cx: final[float] = cx
        self.cy: final[float] = cy
        self.cz: final[float] = cz
        self.dx: final[float] = dx
        self.dy: final[float] = dy
        self.dz: final[float] = dz
        self.ex: final[float] = ex
        self.ey: final[float] = ey
        self.ez: final[float] = ez
        self.fx: final[float] = fx
        self.fy: final[float] = fy
        self.fz: final[float] = fz
        self.gx: final[float] = gx
        self.gy: final[float] = gy
        self.gz: final[float] = gz
        self.hx: final[float] = hx
        self.hy: final[float] = hy
        self.hz: final[float] = hz
        self.n1: final[float] = n1
        self.n2: final[float] = n2
        self.n3: final[float] = n3
        self.n4: final[float] = n4
        self.n5: final[float] = n5
        self.n6: final[float] = n6

        self.parameters: final[tuple[float]] = (
            ax,
            ay,
            az,
            bx,
            by,
            bz,
            cx,
            cy,
            cz,
            dx,
            dy,
            dz,
            ex,
            ey,
            ez,
            fx,
            fy,
            fz,
            gx,
            gy,
            gz,
            hx,
            hy,
            hz,
            n1,
            n2,
            n3,
            n4,
            n5,
            n6,
        )
