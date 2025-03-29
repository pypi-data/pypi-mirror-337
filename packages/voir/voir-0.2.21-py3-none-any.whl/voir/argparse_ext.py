"""This module defines an extension to ArgumentParser.

:class:`ExtendedArgumentParser` can be used to add groups of options defined in
a dataclass, and also provide defaults to them that may come from configuration
files and the like.
"""

import ast
import inspect
import tokenize
import warnings
from argparse import ArgumentParser
from dataclasses import MISSING, dataclass, fields, is_dataclass
from functools import partial
from textwrap import dedent
from typing import Union

from omegaconf import OmegaConf
from ovld import meta, ovld


@dataclass
class Info:
    name: str
    type: type
    help: str
    annotation: object
    prefix: str
    parser: ArgumentParser
    group: ArgumentParser


def _dash(base):
    base = base.replace("_", "-")
    if len(base) == 1:
        return f"-{base}"
    else:
        return f"--{base}"


@ovld
def contribute(default: meta(is_dataclass), info: Info):
    """Populate info.parser based on the default given.

    If there is no default value for the argument, ``default`` takes the value
    ``MISSING``.

    The :class:`Info` object already contains the name of the field, as well as its
    type, help string, etc. Depending on the type of the argument, an argument or
    a subparser will be added to ``info.parser``.
    """
    # NOTE: This function is called using ``contribute[argtype, Info](...)`` which
    # dispatches to the relevant version of ``contribute`` thanks to ``ovld``.
    group = info.parser
    hlp = getattr(info.type, "__help__", None) or info.type.__name__
    if hlp:
        group = info.parser.add_argument_group(hlp)
    docs = get_attribute_docstrings(info.type)
    if info.prefix is None:
        pfx = ""
    else:
        pfx = f"{info.prefix}{info.name}."
    info.parser.constructors[pfx] = (info.type, f"{info.prefix or ''}{info.name}")
    for field in fields(info.type):
        contribute[field.type, Info](
            field.default if default is MISSING else getattr(default, field.name),
            Info(
                name=field.name,
                type=field.type,
                help=docs.get(field.name, None),
                annotation=None,
                prefix=pfx,
                parser=info.parser,
                group=group,
            ),
        )


@ovld
def contribute(default: bool, info: Info):  # noqa: F811
    hlp = info.help
    pth = f"{info.prefix}{info.name}"

    is_default = "(Default) " if default is True else ""
    info.group.add_argument(
        # f"--{pth}",
        _dash(pth),
        action="store_true",
        dest=pth,
        default=default,
        help=f"{is_default}{hlp}",
    )

    pth_no = f"{info.prefix}no-{info.name}"
    is_default = "(Default) " if default is False else ""
    info.group.add_argument(
        _dash(pth_no),
        action="store_false",
        dest=pth,
        default=default,
        help=hlp and f"{is_default}Do not {hlp[0].lower()}{hlp[1:]}",
    )


@ovld
def contribute(default: Union[int, float, str], info: Info):  # noqa: F811
    info.group.add_argument(
        _dash(f"{info.prefix}{info.name}"),
        type=info.type,
        default=None if default is MISSING else default,
        required=default is MISSING,
        metavar=info.name.upper(),
        help=info.help,
    )


def _expand(args, constructors):
    for name in sorted(constructors, key=len, reverse=True):
        ln = len(name)
        cons, dest = constructors[name]
        cons_args = {}
        field_names = {f.name for f in fields(cons)}
        for k, v in list(vars(args).items()):
            if k.startswith(name):
                field_name = k[ln:]
                if field_name in field_names:
                    cons_args[field_name] = v
                    delattr(args, k)
        obj = cons(**cons_args)
        setattr(args, dest, obj)
    return args


class ExtendedArgumentParser(ArgumentParser):
    """Argument parser that supports adding option groups as dataclasses.

    Works just like :class:`argparse.ArgumentParser`, plus the method
    :meth:`~ExtendedArgumentParser.add_from_model`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constructors = {}
        self.base_configs = {}
        self.base_configs_locked = False
        self.used_base_configs = set()

    def merge_base_config(self, config: dict):
        """Merge default values for the configurations.

        This method must be called **before** ``add_from_model(...)``.

        Call this if e.g. you want to import the settings from a configuration file
        as if they had been given as command-line arguments. You can call this method
        multiple times if you have multiple sources of data. You do not need to set
        every option.

        Options provided on the command line will always override what
        is set through this method.

        (The reason ``merge_base_config`` must be called before ``add_from_model``
        is that it may modulate the command-line options, e.g. which ones are optional
        and which ones are required.)

        Arguments:
            config: A dictionary that contains default values for the options
                that will be contributed by ``add_from_model``.
        """
        if self.base_configs_locked:
            raise Exception(
                "Cannot merge a base config after add_from_model is called."
            )
        self.base_configs = OmegaConf.merge(self.base_configs, config)

    def add_from_model(self, dest: str, model: type, flatten: bool = True):
        """Add the attributes of the ``model`` dataclass as options.

        If, for example, we have this dataclass:

        .. code-block:: python

            @dataclass
            class Options:
                # Some number
                abc: int
                # A flag
                xyz: bool = False

        * ``add_from_model("opts", Options)`` will add ``--abc`` and ``--xyz``
          to the argument parser, using the comments as their documentation,
          and the values will be in ``args.opts.abc`` etc.
        * ``add_from_model("opts", Options, flatten=False)`` will add ``--opts.abc``
          and ``--opts.xyz`` (putting the values in the same place).
        * ``--abc`` will be required, ``--xyz`` will be optional because it has
          a default value.

        Arguments:
            dest: The destination key in the arguments Namespace returned by
                ``parse_args``.
            model: A dataclass.
            flatten: If True, the arguments declared in the dataclass will be
                available at the top level. Otherwise, they will have to be
                given as ``--dest-xyz``.
        """
        self.base_configs_locked = True

        if isinstance(model, type):
            typ = model
            model = MISSING
        else:
            typ = type(model)

        self.used_base_configs.add(dest)
        if dest in self.base_configs:
            assert model is MISSING
            model = OmegaConf.merge(OmegaConf.structured(typ), self.base_configs[dest])

        contribute[typ, Info](
            model,
            Info(
                name=dest,
                type=typ,
                help=None,
                annotation=None,
                prefix=None if flatten else dest,
                parser=self,
                group=self,
            ),
        )

    def _parse_known_args(self, *args, **kwargs):
        unused = set(self.base_configs) - self.used_base_configs
        if unused:
            warnings.warn(
                f"Configuration blocks {unused} were not used. Valid blocks are: {self.used_base_configs}. Did you forget a nesting level?"
            )
        ns, args = super()._parse_known_args(*args, **kwargs)
        _expand(ns, self.constructors)
        return ns, args


#############################
# Extracting the docstrings #
#############################


def scrape_comments(src: str):
    """Use the tokenizer module to fetch comments from source.

    Arguments:
        src: The source code.

    Returns:
        List of (line, column, "COMMENT", comment_string)
    """
    lines = bytes(src, encoding="utf8").splitlines(keepends=True)
    return [
        (*tok.start, "COMMENT", tok.string[1:].strip())
        for tok in tokenize.tokenize(partial(next, iter(lines)))
        if tok.type == tokenize.COMMENT
    ]


class AttributeVisitor(ast.NodeVisitor):
    """Walk an AST to gather variable and docstring tokens and their lines/columns."""

    def __init__(self):
        self.data = []
        self.prefix = None

    def add_data(self, node, kind, content):
        self.data.append((node.lineno, node.col_offset, kind, content))

    def visit_body(self, name, stmts):
        old_prefix = self.prefix
        if self.prefix is None:
            self.prefix = ""
        else:
            self.prefix += f"{name}."
        for stmt in stmts:
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)
            ):
                self.add_data(stmt, "DOC", stmt.value.value)
            else:
                self.visit(stmt)
        self.prefix = old_prefix

    def visit_ClassDef(self, node):
        if self.prefix is not None:
            self.add_data(node, "VARIABLE", f"{self.prefix}{node.name}")
        self.visit_body(node.name, node.body)

    def visit_FunctionDef(self, node):
        if self.prefix is not None:
            self.add_data(node, "VARIABLE", f"{self.prefix}{node.name}")
        self.visit_body(node.name, node.body)

    def visit_Assign(self, node):
        self.generic_visit(node, may_assign=True)

    def visit_AnnAssign(self, node):
        self.generic_visit(node, may_assign=True)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.add_data(node, "VARIABLE", f"{self.prefix}{node.id}")

    def generic_visit(self, node, may_assign=False):
        if isinstance(node, ast.stmt) and not may_assign:
            self.add_data(node, "OTHER", None)
        super().generic_visit(node)


def scrape_variables_and_docstrings(src: str):
    """Scrape the variables and docstrings from source code.

    Arguments:
        src: The source code.

    Returns:
        List of (line, column, "VARIABLE"|"DOC"|"OTHER", name_or_content)
    """
    visitor = AttributeVisitor()
    visitor.visit(ast.parse(src))
    return visitor.data


def get_attribute_docstrings(cls):
    """Get the docstrings for individual attributes of a class.

    Arguments:
        cls: The class for which we want to get attribute documentation.

    Returns:
        A dict from variable name to its associated docstring (after itself) and/or
        comment (above itself).
    """
    docs = {}
    current = None
    current_line = None
    for_next = []
    src = dedent(inspect.getsource(cls))
    # We concatenate comment tokens from the tokenizer with
    # variable/docstring tokens extracted using the ast module
    data = sorted(scrape_comments(src) + scrape_variables_and_docstrings(src))
    for line, _, kind, content in data:
        if kind == "COMMENT":
            if current is not None and current_line == line:
                docs[current].append(content)
            else:
                for_next.append(content)
        elif kind == "DOC" and current:
            docs[current].append(content)
        elif kind == "VARIABLE":
            docs[content] = for_next
            for_next = []
            current = content
            current_line = line
        elif kind == "OTHER":
            current = current_line = None
            for_next = []
    return {k: "\n".join(lines) for k, lines in docs.items()}
