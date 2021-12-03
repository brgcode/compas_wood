#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import
from __future__ import print_function

import io
from os import path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools

from setuptools.command.develop import develop
from setuptools.command.install import install

#here = path.abspath(path.dirname(__file__
here = os.path.abspath(os.path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(
        path.join(here, *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


long_description = read("README.md")
requirements = read("requirements.txt").split("\n")
optional_requirements = {}

conda_prefix = os.getenv('CONDA_PREFIX')

windows = os.name == 'nt'


def get_pybind_include():
    if windows:
        return os.path.join(conda_prefix, 'Library', 'include')
    return os.path.join(conda_prefix, 'include')


def get_eigen_include():
    if windows:
        return os.path.join(conda_prefix, 'Library', 'include', 'eigen3')
    return os.path.join(conda_prefix, 'include', 'eigen3')


def get_library_dirs():
    if windows:
        return os.path.join(conda_prefix, 'Library', 'lib')
    return os.path.join(conda_prefix, 'lib')
    
    
ext_modules = [
    Extension(
        'compas_wood._wood',
        sorted([
            'src/CGAL_BoxUtil.h',
            'src/CGAL_IntersectionUtil.h',
            'src/CGAL_MathUtil.h',
            'src/CGAL_MeshUtil.h',
            'src/CGAL_PlaneUtil.h',
            'src/CGAL_PolylineUtil.h',
            'src/CGAL_Print.h',
            'src/CGAL_VectorUtil.h',
            'src/CGAL_XFormUtil.h',
            'src/CGAL_clipper.cpp',
            'src/CGAL_clipper.h',
            'src/CGAL_compas.h',
            'src/CGAL_connection_zones.cpp',
            'src/CGAL_connection_zones.h',
            'src/CGAL_element.h',
            'src/CGAL_joint.h',
            'src/CGAL_joint_library.h',
            'src/CGAL_RTree.h',
            'src/CGAL_stdafx.h',
            'src/CGAL_xxx_interop_python.cpp',
            'src/CGAL_xxx_interop_python.h',
            
        ]),
        include_dirs=[
            './include',
            get_eigen_include(),
            get_pybind_include()
        ],
        library_dirs=[
            get_library_dirs(),
        ],
        libraries=['mpfr', 'gmp'],
        language='c++'
    ),
 ]   
    
    
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    import os
    with tempfile.NamedTemporaryFile('w', suffix='.cpp', delete=False) as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        fname = f.name
    try:
        compiler.compile([fname], extra_postargs=[flagname])
    except setuptools.distutils.errors.CompileError:
        return False
    finally:
        try:
            os.remove(fname)
        except OSError:
            pass
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.
    The newer version is prefered over c++11 (when it is available).
    """
    # flags = ['-std=c++17', '-std=c++14', '-std=c++11']
    flags = ['-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc', '/std:c++14'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    # if sys.platform == 'darwin':
    #     darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.14']
    #     c_opts['unix'] += darwin_opts
    #     l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
            opts.append('-DCGAL_DEBUG=1')
        for ext in self.extensions:
            ext.define_macros = [('VERSION_INFO', '"{}"'.format(self.distribution.get_version()))]
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


    
setup(
    name="compas_wood",
    version="0.1.0",
    description="Timber joinery generation based on CGAL library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibois-epfl/compas_wood",
    author="petras vestartas",
    author_email="petrasvestartas@gmail.com",
    license="GPL-3 License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GPL-3 License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=[],
    project_urls={},
    packages=["compas_wood"],
    package_dir={"": "src"},
    # package_data={},
    # data_files=[],
    # include_package_data=True,
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    setup_requires=['pybind11>=2.5.0'],
    install_requires=requirements,
    python_requires=">=3.6",
    extras_require=optional_requirements,
    zip_safe=False,
)
    
    
    
    



setup(
    name="compas_wood",
    version="0.1.0",
    description="joinery generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IBOIS/compas_wood",
    author="Petras Vestartas",
    author_email="petrasvestartas@gmail.com",
    license="MIT license",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=[],
    project_urls={},
    packages=["compas_wood"],
    package_dir={"": "src"},
    package_data={},
    data_files=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    python_requires=">=3.6",
    extras_require=optional_requirements,
    entry_points={
        "console_scripts": [],
    },
    ext_modules=[],
)
