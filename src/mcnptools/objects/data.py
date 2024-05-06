"""Classes for parsing elements in the data section of an MCNP input file.

The base class is called `Data`

Currently we support specialized version of the base class for:
- Source (sdef)
- SourceInformation (SI)
- Nps
- Print
- Random
- Mode
- Ptrac
- Tally
- TallyModifier
- Cut
- Energy

"""

import re
from typing import Dict, List, Optional

from rich import print

from ..input_line import InputLine


def parse_number(value: str, requested_type=float):
    value = value.strip()
    if value == "j":
        return None
    else:
        return requested_type(value)


def to_number(value) -> str:
    if value is None:
        return "j"

    return str(value)


def is_numeric(value):
    """Quick test if a string can be converted to float.

    This is better than value.isnumeric(), since it can handle 1e6 or -1.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


class Data:
    """The base class for all data related entries."""

    all_data = []
    multi_arg_keys = {}

    def __init__(
        self,
        name: str,
        parameters: Dict,
        args: List,
        comment: Optional[str] = None,
    ) -> None:
        self.name = name
        self.parameters = parameters
        self.args = args
        self.comment = comment

    @classmethod
    def get_all_data(cls):
        return cls.all_data

    def to_mcnp(self):
        out = f"{self.name} "
        for k, v in self.parameters.items():
            out += f"{k}={v} "
        for v in self.args:
            out += f"{v} "
        out = out.strip()
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        """Most lines in the data part will be parsed in the general class.

        For some we have specialized subclasses.
        """

        components = line.text.split()
        comment = line.comment
        name = components[0].lower()

        if len(line.text) == 1 and line.text[0].lower() == "c":
            # this might be a bug in the input files, since comments should be "c "?
            # this should be resolved in a better way eventually
            return
        elif name == "ptrac":
            return Ptrac.from_mcnp(line)
        elif name == "sdef":
            return Source.from_mcnp(line)
        elif name == "nps":
            return Nps.from_mcnp(line)
        elif name == "mode":
            return Mode.from_mcnp(line)
        elif name == "rand":
            return Random.from_mcnp(line)
        elif name == "print":
            return Print.from_mcnp(line)
        elif name.startswith("cut"):
            return Cut.from_mcnp(line)
        elif name[0] == "s" and name[1] in "ibp":
            return SourceInformation.from_mcnp(line)
        elif name.startswith("fm") and not name.startswith("fmesh"):
            return TallyModifier.from_mcnp(line)
        elif name.startswith("f") or name.startswith("*f"):
            return Tally.from_mcnp(line)
        elif name[0] == "e":
            return TallyModifier.from_mcnp(line)
        elif name.startswith("c") or name.startswith("*c"):
            return TallyModifier.from_mcnp(line)

        parameters, args = cls.parse_key_value_pairs(components[1:])

        return cls(name=name, parameters=parameters, args=args, comment=comment)

    @classmethod
    def parse_key_value_pairs(cls, components: List[str]):
        """Parse key-value pairs separated with equal signs.

        Note: this gets called before the class is created, so no reference to self available.
        """
        parameters = {}
        remaining_args = []
        key = None  # the current key in a key-value pair

        # a int flag, if the next N components belongs to the previous one
        # for example: vec=0 0 0
        add_next_component = 0
        for c in components:
            if add_next_component > 0:
                # in this case, key will already be defined from below
                parameters[key] += f" {c}"
                add_next_component -= 1
                continue
            if "=" not in c:
                remaining_args.append(c)
                continue
            tmp = c.split("=")
            if len(tmp) == 2:
                key, value = tmp
                key = key.lower()
                parameters[key] = value
                if cls.multi_arg_keys:
                    if key in cls.multi_arg_keys.keys():
                        # since we already parsed one of the values, we subtract 1 here
                        add_next_component = cls.multi_arg_keys[key] - 1
            else:
                print(
                    f"[orange3]Warning[/] Data: {c} not implemented (in {components})."
                )
        return parameters, remaining_args


class Source(Data):
    """The `sdef` card.

    We currently don't support all possible entries, but try to parse many.
    """

    multi_arg_keys = {"pos": 3, "vec": 3}

    def __init__(self, parameters, args, comment: Optional[str] = None):
        self.parameters = parameters
        self.comment = comment
        self.args = args
        self.x = None
        self.y = None
        self.z = None
        self.position = None
        self.energy = None
        self.time = None
        self.surface = None
        self.direction = None
        self.vector = None

        # parse our some of the parameters, so that we can modify them more easily in python later
        if "x" in self.parameters:
            self.x = self.parameters["x"]
            del self.parameters["x"]
        if "y" in self.parameters:
            self.y = self.parameters["y"]
            del self.parameters["y"]
        if "z" in self.parameters:
            self.z = self.parameters["z"]
            del self.parameters["z"]
        if "pos" in self.parameters:
            self.position = self.parameters["pos"]
            del self.parameters["pos"]
        if "vec" in self.parameters:
            self.vector = self.parameters["vec"]
            del self.parameters["vec"]
        if "tme" in self.parameters:
            self.time = self.parameters["tme"]
            del self.parameters["tme"]
        if "sur" in self.parameters:
            self.surface = self.parameters["sur"]
            del self.parameters["sur"]
        if "erg" in self.parameters:
            self.energy = self.parameters["erg"]
            del self.parameters["erg"]
        if "dir" in self.parameters:
            self.direction = self.parameters["dir"]
            del self.parameters["dir"]

    def to_mcnp(self):
        out = "sdef " + self.parameters_to_str()
        out = out.strip()
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"

    def parameters_to_str(self):
        out = ""
        if self.energy:
            out += f"erg={self.energy} "
        if self.position:
            out += f"pos={self.position} "
        if self.x:
            out += f"X={self.x} "
        if self.y:
            out += f"Y={self.y} "
        if self.z:
            out += f"Z={self.z} "
        if self.direction:
            out += f"dir={self.direction} "
        if self.vector:
            out += f"vec={self.vector} "
        if self.time:
            out += f"tme={self.time} "
        if self.surface:
            out += f"sur={self.surface} "
        for k, v in self.parameters.items():
            out += f"{k}={v} "
        for v in self.args:
            out += f"{v} "
        return out

    @classmethod
    def from_mcnp(cls, line: InputLine):
        """Identify all key-value pairs and assume the rest are single arguments."""

        components = line.text.split()
        comment = line.comment
        parameters, args = cls.parse_key_value_pairs(components[1:])

        return cls(parameters=parameters, args=args, comment=comment)

    def __str__(self):
        out = "Source "
        if self.comment:
            out += f" ({self.comment}) "
        out += self.parameters_to_str()
        return out.strip() + "\n"


class SourceInformation(Data):
    def __init__(
        self,
        name: str,
        values: List[float],
        option: Optional[str] = None,
        comment: Optional[str] = None,
    ):
        self.name = name
        self.option = option
        self.values = values
        self.comment = comment

    def to_mcnp(self):
        out = f"{self.name} "
        if self.option is not None:
            out += f"{self.option} "
        out += " ".join(self.values)
        if self.comment:
            out += f" $ {self.comment}"
        return out.strip() + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()
        comment = line.comment

        name = components[0].lower()
        tmp = components[1]
        if is_numeric(tmp):
            option = float(tmp)
            if option >= 0:
                option = None
                values = components[1:]
            else:
                values = components[2:]
        else:
            option = tmp
            values = components[2:]

        return cls(name, values, option, comment=comment)

    def __str__(self):
        comment = f" ({self.comment})" if self.comment else ""
        out = f"Source information {self.name} {self.option}{comment}: "
        out += "     " + " ".join(self.values)
        return out.strip() + "\n"


class Nps(Data):
    def __init__(self, number, comment: Optional[str] = None):
        self.number = number
        self.comment = comment

    def to_mcnp(self):
        out = f"nps {self.number}"
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()
        comment = line.comment

        number = components[1]
        if is_numeric(number):
            number = int(float(number))
        else:
            print(f"[red]Error[/] Cannot parse {number}")
            return
        return cls(number, comment)

    def __str__(self):
        out = f"Number of particles: {self.number}"
        if self.comment:
            out += f" ({self.comment})"
        return out + "\n"


class Print(Data):
    def __init__(self, values, comment: Optional[str] = None):
        self.values = values
        self.comment = comment

    def to_mcnp(self):
        out = "Print " + " ".join(self.values)
        if self.comment:
            out += f" $ {self.comment}"
        return out.strip() + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()
        comment = line.comment

        values = components[1:]
        return cls(values, comment)

    def __str__(self):
        out = f"Print: {' '.join(self.values)}"
        if self.comment:
            out += f" ({self.comment})"
        return out + "\n"


class Random(Data):
    def __init__(self, parameters, comment: Optional[str] = None):
        self.parameters = parameters
        self.comment = comment

    def to_mcnp(self):
        out = f"rand "
        out += " ".join(f"{k}={v}" for k, v in self.parameters.items())
        out = out.strip()
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()
        comment = line.comment

        parameters, left_over = cls.parse_key_value_pairs(components[1:])
        if left_over:
            print(f"[orange3]Warning[/] Random: left over arguments: {left_over}")

        return cls(parameters, comment)

    def __str__(self):
        out = "Random "
        for k, v in self.parameters.items():
            out += f"{k}={v} "
        for v in self.args:
            out += f"{v} "
        out = out.strip()
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"


class Mode(Data):
    def __init__(
        self,
        neutrons: bool = False,
        photons: bool = False,
        comment: Optional[str] = None,
    ):
        self.neutrons = neutrons
        self.photons = photons
        self.comment = comment

    def to_mcnp(self):
        out = "mode "
        if self.neutrons:
            out += "n "
        if self.photons:
            out += "p "
        out = out.strip()
        if self.comment:
            out += f" ${self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()[1:]
        components = [c.lower() for c in components]
        comment = line.comment

        photons = "p" in components
        neutrons = "n" in components

        return cls(neutrons, photons, comment)

    def __str__(self):
        out = "Mode "
        if self.comment:
            out += f"({self.comment}) "
        if self.neutrons:
            out += "neutrons "
        if self.photons:
            out += "photons "
        out = out.strip()
        return out + "\n"


class Ptrac(Data):
    def __init__(self, parameters, comment: Optional[str] = None):
        self.parameters = parameters
        self.comment = comment

    def to_mcnp(self):
        out = "ptrac "
        for k, v in self.parameters.items():
            out += f"{k}={v} "
        out = out.strip()
        if self.comment:
            out += f"$ {self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        """Most lines in the data part will be parsed in the general class.

        For some we have specialized subclasses.
        """

        components = line.text.split()
        comment = line.comment

        parameters, args = cls.parse_key_value_pairs(components[1:])

        if args:
            print(f"[orange3]Warning[/] Ptrac: left over args: {args}")

        return cls(parameters=parameters, comment=comment)

    def __str__(self):
        out = "Ptrac "
        for k, v in self.parameters.items():
            out += f"{k}={v} "
        out = out.strip()
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"


class Tally(Data):
    def __init__(
        self, name, number, particle, parameters: str, comment: Optional[str] = None
    ):
        self.name = name  # F, Fmesh, ...
        self.number = number
        self.particle = particle
        self.parameters = parameters
        self.comment = comment

    def to_mcnp(self):
        out = f"{self.name}{self.number}:{self.particle} {self.parameters}"
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        """Most lines in the data part will be parsed in the general class.

        For some we have specialized subclasses.
        """

        components = line.text.split()
        comment = line.comment

        name = components[0]

        name, particle = name.split(":")

        # Use re.split() to split the string based on the pattern
        pattern = r"(\D+)(\d+)"
        matches = re.split(pattern, name)

        # Extract characters and the number from the matches
        name = matches[1]
        number = int(matches[2])

        parameters = " ".join(components[1:])

        return cls(name, number, particle, parameters=parameters, comment=comment)

    def __str__(self):
        comment = f" ({self.comment})" if self.comment else ""
        out = f"Tally number={self.number} particle={self.particle}{comment}:\n"
        out += f"     {self.parameters}\n"
        return out


class TallyModifier(Data):
    def __init__(self, name, number: int, parameters, comment: Optional[str] = None):
        self.name = name
        self.number = number
        self.parameters = parameters
        self.comment = comment

    def to_mcnp(self):
        out = f"{self.name}{self.number} "
        out += " ".join(self.parameters)
        out = out.strip()
        if self.comment:
            out += f" $ {self.comment}"
        return out + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()
        comment = line.comment

        name = components[0]
        pattern = r"(\D+)(\d+)"
        matches = re.split(pattern, name)

        # Extract characters and the number from the matches
        name = matches[1]
        number = int(matches[2])

        parameters = components[1:]

        return cls(name, number, parameters, comment)

    def __str__(self):
        out = "Tally Multiplier {self.number} "
        if self.comment:
            out += f" ({self.comment})"
        out = out.strip() + "\n"
        for p in self.parameters:
            out += f"{p} "
        out = out.strip()
        return out + "\n"


class Cut(Data):
    def __init__(
        self,
        particle,
        time_cutoff,
        energy_cutoff,
        weight_cutoff,
        weight_min,
        comment: Optional[str] = None,
    ):
        self.particle = particle
        self.time_cutoff = time_cutoff
        self.energy_cutoff = energy_cutoff
        self.weight_cutoff = weight_cutoff
        self.weight_min = weight_min
        self.comment = comment

    def to_mcnp(self):
        # go through reverse order, so that we can skip undefined options at the back
        if self.weight_min is None:
            out = ""
        else:
            out = f" {self.weight_min}"

        if self.weight_cutoff is None:
            if out:
                out = "j j " + out
        else:
            out = f"{self.weight_cutoff[0]} {self.weight_cutoff[1]} " + out

        if self.energy_cutoff is None:
            if out:
                out = "j " + out
        else:
            out = f"{self.energy_cutoff} " + out

        if self.time_cutoff is None:
            if out:
                out = "j " + out
        else:
            out = f"{self.time_cutoff} " + out

        out = f"cut:{self.particle} " + out
        return out.strip() + "\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        components = line.text.split()
        comment = line.comment

        particle = ""
        tc = None
        ec = None
        wc = None
        w_min = None

        for i, c in enumerate(components):
            if i == 0:
                particle = c[4]
            elif i == 1:
                tc = parse_number(c)
            elif i == 2:
                ec = parse_number(c)
            elif i == 3:
                wc = parse_number(c)
                if wc is not None:
                    wc = [wc, None]
            elif i == 4:
                tmp = parse_number(c)
                if wc:
                    wc[1] = tmp
            elif i == 5:
                w_min = parse_number(c)

        if wc is not None:
            if (wc[0] is None) or (wc[1] is None):
                print(
                    f"[orange3]Warning[/] Parsing '{line.text}'. Possible bug: only one weight cutoff given! ... Fixing it."
                )
            wc[0] = wc[0] if wc[0] is not None else 0
            wc[1] = wc[1] if wc[1] is not None else 0
        return cls(particle, tc, ec, wc, w_min, comment)

    def __str__(self):
        comment = f" ({self.comment})" if self.comment else ""
        p = self.particle
        tc = self.time_cutoff
        ec = self.energy_cutoff
        wc = self.weight_cutoff
        w_min = self.weight_min

        out = f"Cut particle={p}{comment}:\n"
        if tc:
            out += f"    time cutoff: {tc}\n"
        if ec:
            out += f"    energy cutoff: {ec}\n"
        if wc:
            out += f"    weight cutoff: {wc}\n"
        if w_min:
            out += f"    weight min: {w_min}\n"
        return out


class Energy(Data):
    def __init__(
        self,
        number,
        bins,
        nt: Optional[bool] = False,
        cumulative: Optional[bool] = False,
        comment: Optional[str] = None,
    ):
        self.number = number
        self.bins = bins
        self.nt = nt
        self.cumulative = cumulative
        self.comment = comment

    def to_mcnp(self):
        nt = " NT" if self.nt else ""
        c = " C" if self.cumulative else ""
        bins = " ".join(str(x) for x in self.bins)
        comment = f" $ {self.comment}" if self.comment else ""
        return f"E{self.number} {bins}{nt}{c}{comment}\n"

    @classmethod
    def from_mcnp(cls, line: InputLine):
        """Most lines in the data part will be parsed in the general class.

        For some we have specialized subclasses.
        """

        components = line.text.split()
        comment = line.comment

        number = int(components[0][1:])
        components = components[1:]

        nt = False
        c = False
        if components[-1].lower() == "c":
            c = True
            if components[-2].lower() == "nt":
                nt = True
                components = components[:-1]
            components = components[:-1]
        elif components[-1].lower() == "nt":
            nt = True
            components = components[:-1]

        return cls(number, components, nt=nt, cumulative=c, comment=comment)

    def __str__(self):
        comment = f" ({self.comment})" if self.comment else ""
        n = self.number
        nt = self.nt
        c = self.cumulative
        out = f"Energy number={n} no_total={nt} cumulative={c}{comment}:\n"
        out += f"    bins: {self.bins}\n"
        return out
