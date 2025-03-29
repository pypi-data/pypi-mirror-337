"""Writer class for writing python avro files"""

import json
import pkg_resources
import os
import shutil
from typing import Any, List, Optional
from anytree import Node, LevelOrderIter
from textwrap import TextWrapper, fill, wrap
from jinja2 import Environment, FileSystemLoader

import keyword
import builtins

from avro_to_python_etp.utils.avro.helpers import get_union_types, split_words
from avro_to_python_etp.utils.avro.primitive_types import PRIMITIVE_TYPE_MAP
from avro_to_python_etp.utils.paths import (
    get_system_path,
    verify_or_create_namespace_path,
    get_or_create_path,
    get_joined_path,
)


TEMPLATE_PATH = __file__.replace(get_joined_path("writer", "writer.py"), "templates/")
TEMPLATE_PATH = get_system_path(TEMPLATE_PATH)

PYTHON_FILE_LICENSE = """# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""


class AvroWriter(object):
    """writer class for writing python files

    Should initiate around a tree object with nodes as:

    {
        'children': {},
        'files': {},
        'visited': False
    }

    The "keys" of the children are the namespace names along avro
    namespace paths. The Files are the actual files within the
    namespace that need to be compiled.

    Note: The visited flag in each node is only for node traversal.

    This results in the following behavior given this sample tree:

    tree = {
        'children': {'test': {
            'children': {},
            'files': {'NestedTest': ...},
            'visited': False
        }},
        'files': {'Test' ...},
        'visited': False
    }

    files generated:
    /Test.py
    /test/NestedTest.py
    """

    root_dir = None
    files = []

    def __init__(
        self,
        tree: Node,
        pip: str = None,
        author: str = None,
        package_version: str = None,
    ) -> None:
        """Parses tree structured dictionaries into python files

        Parameters
        ----------
            tree: dict
                tree object
                acyclic tree representing a read avro schema namespace
            pip: str
                pip package name
            author: str
                author of pip package

        Returns
        -------
            None

        TODO: Check tree is valid
        """
        self.pip = pip
        self.author = author
        self.package_version = package_version
        self.tree = tree

        # jinja2 templates
        self.template_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
        self.template_env.filters.update(
            {
                "snake_case": self.snake_case,
                "compress": self.compress,
                "screaming_snake_case": self.screaming_snake_case,
                "lower_and_snake": self.lower_and_snake,
                "is_reserved": self.is_reserved,
            }
        )
        self.template = self.template_env.get_template("baseTemplate.j2")

    def lower_and_snake(self, value: str, **kwargs: Any) -> str:
        split = value.split(".")
        return "%s" % ".".join([self.snake_case(str(x)) for x in split])

    def snake_case(self, value: str, **kwargs: Any) -> str:
        """Convert the given string to snake case."""
        return "_".join(map(str.lower, split_words(value)))

    def is_reserved(self, value: str, **kwargs: Any) -> bool:
        builtins_list: List[str] = dir(builtins)
        return keyword.iskeyword(value) or value in builtins_list

    def compress(self, value: str, **kwargs: Any) -> str:
        """Compress and wraps the given string."""

        schema = ""
        for line in wrap(value, width=70):
            # print("---------")
            # print("'{}'".format(line))
            schema += "'{}'".format(line)
            schema += "\n"
            # print("---------")
        # print(schema)
        return schema  # fill(value, width=70)

    def screaming_snake_case(self, value: str, **kwargs: Any) -> str:
        """Convert the given string to screaming snake case."""
        return self.snake_case(value, **kwargs).upper()

    def write(self, root_dir: str) -> None:
        """Public runner method for writing all files in a tree

        Parameters
        ----------
            root_path: str
                root path to write files to

        Returns
        -------
            None
        """

        self.root_dir = get_system_path(root_dir)
        if self.pip:
            self.pip_import = self.pip.replace("-", "_")
            self.pip_dir = self.root_dir + "/" + self.pip
            self.root_dir += "/" + self.pip + "/" + self.pip.replace("-", "_")
            self.pip = self.pip.replace("-", "_")
        else:
            self.pip_import = ""
        get_or_create_path(self.root_dir)
        # self._write_helper_file()

        self._write_dfs()

        if self.pip:
            self._write_pyproject_file()
            # self._write_setup_file()
            self._write_pip_init_file()
            # self._write_manifest_file()
            self._write_py_typed_file()

        self.copy_raw()

    def _write_manifest_file(self) -> None:
        """writes manifest to recursively include packages"""
        filepath = self.pip_dir + "/MANIFEST.in"
        template = self.template_env.get_template("files/manifest.j2")
        filetext = template.render(pip=self.pip)
        with open(filepath, "w") as f:
            f.write(filetext)

    def _write_pyproject_file(self) -> None:
        """writes the pyproject.py file to the pip dir"""
        filepath = self.pip_dir + "/pyproject.toml"
        template = self.template_env.get_template("files/pyproject.j2")
        filetext = template.render(
            pip=self.pip, author=self.author, package_version=self.package_version
        )
        with open(filepath, "w") as f:
            f.write(filetext)

    def _write_setup_file(self) -> None:
        """writes the setup.py file to the pip dir"""
        filepath = self.pip_dir + "/setup.py"
        template = self.template_env.get_template("files/setup.j2")
        filetext = template.render(
            pip=self.pip, author=self.author, package_version=self.package_version
        )
        with open(filepath, "w") as f:
            f.write(PYTHON_FILE_LICENSE)
            f.write(filetext)

    def _write_pip_init_file(self) -> None:
        """writes the __init__ file to the pip dir"""
        filepath = self.pip_dir + "/" + self.pip + "/__init__.py"
        template = self.template_env.get_template("files/pip_init.j2")
        filetext = template.render(
            pip=self.pip, author=self.author, package_version=self.package_version
        )
        with open(filepath, "w") as f:
            f.write(PYTHON_FILE_LICENSE)
            f.write(filetext)

    def _write_py_typed_file(self) -> None:
        """writes the py.typed file to the pip dir, package comply with PEP-561"""
        filepath = self.pip_dir + "/" + self.pip + "/py.typed"
        template = self.template_env.get_template("files/py.j2")
        filetext = template.render()
        with open(filepath, "w") as f:
            f.write(filetext)

    def _write_helper_file(self) -> None:
        """writes the helper file to the root dir"""
        filepath = self.root_dir + "/helpers.py"
        template = self.template_env.get_template("files/helpers.j2")
        filetext = template.render()
        with open(filepath, "w") as f:
            f.write(PYTHON_FILE_LICENSE)
            f.write(filetext)

    def _write_init_file(
        self,
        imports: set,
        namespace: str,
        open_opt="w",
        init_namespace: Optional[str] = None,
        local: bool = False,
    ) -> None:
        """writes __init__.py files for namespace imports"""
        template = self.template_env.get_template("files/init.j2")
        filetext = template.render(
            imports=imports if not local else set(),
            imports_local=imports if local else set(),
            pip_import=self.pip_import,
            namespace=namespace,
            comment="a" not in open_opt,
        )
        if "a" not in open_opt:
            verify_or_create_namespace_path(rootdir=self.root_dir, namespace=namespace)
        filepath = (
            self.root_dir
            + "/"
            + (init_namespace or namespace).replace(".", "/")
            + "/"
            + "__init__.py"
        )  # NOQA
        print(filepath)
        with open(filepath, open_opt) as f:
            f.write(filetext)
        return

    def copy_raw(self):
        test_dir = self.pip_dir
        folder = pkg_resources.resource_filename("avro_to_python_etp", "raw_files")
        for path, dirs, files in os.walk(folder):
            cur_folder = path.replace(folder, "")
            while cur_folder.startswith("/") or cur_folder.startswith("\\"):
                cur_folder = cur_folder[1:]

            cur_folder = self.pip_dir + "/" + cur_folder

            try:
                os.makedirs(cur_folder)
            except FileExistsError:
                pass
            for file_name in files:
                shutil.copy(path + "/" + file_name, cur_folder + "/" + file_name)

    def _write_file(self, filename: str, filetext: str, namespace: str) -> None:
        """writes python filetext to appropriate namespace"""
        verify_or_create_namespace_path(rootdir=self.root_dir, namespace=namespace)
        filepath = (
            self.root_dir
            + "/"
            + namespace.replace(".", "/")
            + "/"
            + self.snake_case(filename)
            + ".py"
        )  # NOQA
        with open(filepath, "w") as f:
            f.write(PYTHON_FILE_LICENSE)
            f.write(filetext)

    def _render_file(self, file: dict) -> str:
        """compiles a file obj into python

        Parameters
        ----------
            file: dict
                file obj representing an avro file

        Returns
        -------
            filetext: str
                rendered python file as a sting
        """
        filetext = self.template.render(
            file=file,
            primitive_type_map=PRIMITIVE_TYPE_MAP,
            get_union_types=get_union_types,
            json=json,
            pip_import=self.pip_import,
            enumerate=enumerate,
        )
        return filetext

    def _write_dfs(self) -> None:
        # all_imports = {}
        for node in LevelOrderIter(self.tree, filter_=lambda n: not n.is_leaf):
            imports = set()
            path = [str(n.name) for n in node.path]
            print(path)
            namespace = "%s" % ".".join([self.snake_case(str(x)) for x in path])
            import_all = []
            # all_imports[namespace] = set()
            for c in node.children:
                if c.is_leaf:
                    filetext = self._render_file(file=c.file)
                    self._write_file(
                        filename=c.file.name, filetext=filetext, namespace=namespace
                    )
                    imports.add(c.file.name)
                    # if all_imports.get(namespace, None) is None:
                    #     all_imports[namespace] = set()
                    # all_imports[namespace].add(c.file.name)
                    # print(f'{namespace}.{c.file.name}')

            # self._write_init_file(
            #     imports=imports,
            #     local=True,
            #     namespace=namespace,
            #     # namespace=f".{namespace.split(".")[-1}",
            #     # init_namespace=namespace,
            # )
            self._write_init_file(imports=imports, namespace=namespace)

        # for ns, imports in all_imports.items():
        #     if len(imports) > 0:
        #         print(ns.split(".")[:-1])
        #         print(f"\t{imports}")
        #         self._write_init_file(
        #             imports=set(imports),
        #             local=True,
        #             namespace=f".{ns.split(".")[-1]}",
        #             open_opt="a",
        #             init_namespace=".".join(ns.split(".")[:-1]),
        #         )
        # try:
        #     for f_name in import_all:
        #         self._write_init_file(imports=set(['*']), namespace=f"{namespace}.{self.snake_case(f_name)}", open_opt="a", init_namespace=namespace)
        # except FileNotFoundError:
        #     pass

        # print(list(all_imports))
        # print(list(map(lambda xi: '.'.join(xi.split('.')[:-2]), all_imports)))

        # for node in LevelOrderIter(self.tree, filter_=lambda n: not n.is_leaf):
        #     imports = set()
        #     path = [str(n.name) for n in node.path]
        #     namespace = "%s" % ".".join([self.snake_case(str(x)) for x in path])
        #     for ns, f_name in all_imports:
        #         if namespace in ns and len(ns) > len(namespace):
        #             self._write_init_file(imports=set([f_name]), namespace=ns, open_opt="a")
