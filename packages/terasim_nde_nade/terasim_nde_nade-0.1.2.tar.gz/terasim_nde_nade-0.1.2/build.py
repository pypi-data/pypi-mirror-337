import numpy
from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.extension import Extension

extensions = [
    Extension(
        "terasim_nde_nade.utils.collision.collision_check_cy",
        ["terasim_nde_nade/utils/collision/collision_check_cy.pyx"],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        "terasim_nde_nade.utils.geometry.geometry_utils_cy",
        ["terasim_nde_nade/utils/geometry/geometry_utils_cy.pyx"],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        "terasim_nde_nade.utils.trajectory.trajectory_utils_cy",
        ["terasim_nde_nade/utils/trajectory/trajectory_utils_cy.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

def build(setup_kwargs):
    """
    This function is mandatory to build Cython extensions with poetry-core.
    """
    setup_kwargs.update(
        {
            "ext_modules": cythonize(
                extensions,
                compiler_directives={"language_level": 3},
                force=True,
            ),
            "zip_safe": False,
        }
    )
    # Also build in-place for development
    setup(ext_modules=cythonize(extensions, compiler_directives={"language_level": 3}, force=True), script_args=["build_ext", "--inplace"])
    return setup_kwargs
