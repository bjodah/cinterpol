from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    from cinterpol.poly_coeff_expr import coeff_expr, render_mako_template_to
    use_cython = True

import numpy as np

mako_targets = {'cinterpol/poly_coeff{}.c'.format(i): (
    'cinterpol/poly_coeffX.c.mako', coeff_expr(i)) for i \
                in range(1, 6, 2)}

class my_build_ext(build_ext):
    """Subclassing according to modified:
    http://www.digip.org/blog/2011/01/generating-data-files-in-setup.py.html"""
    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            #target_dir = os.path.join(self.build_lib, 'mypkg/media')
            # mkpath is a distutils helper to create directories
            #self.mkpath(target_dir)
            for outpath, (tmpl_path, subsd) in mako_targets.iteritems():
                render_mako_template_to(tmpl_path, outpath, subsd)

        # distutils uses old-style classes, so no super()
        build_ext.run(self)


cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        Extension("cinterpol.core", mako_targets.keys() + [
            "cinterpol/core.pyx", 'cinterpol/newton_interval.c']),
    ]
    cmdclass.update({ 'build_ext': my_build_ext })
else:
    ext_modules += [
        Extension("cinterpol.core", [ "cinterpol/core.c" ]),
    ]

setup(
    name='cinterpol',
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    include_dirs=[np.get_include()],
    packages = ['cinterpol']
)
