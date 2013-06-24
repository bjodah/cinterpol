from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
    import bz2
    open('cInterpol/core.c','wb').write(bz2.BZ2File('cInterpol/core.c.bz2').read())
else:
    from cInterpol.poly_coeff_expr import coeff_expr, render_mako_template_to
    use_cython = True
    mako_targets = {'cInterpol/poly_coeff{}.c'.format(i): (
        'cInterpol/poly_coeffX.c.mako', coeff_expr(i)) for i \
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


import numpy as np



cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        Extension("cInterpol.core", mako_targets.keys() + [
            "cInterpol/core.pyx", 'cInterpol/newton_interval.c']),
    ]
    cmdclass.update({ 'build_ext': my_build_ext })
else:
    ext_modules += [
        Extension("cInterpol.core", [ "cInterpol/core.c" ]),
    ]

setup(
    name='cInterpol',
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    include_dirs=[np.get_include()],
    packages = ['cInterpol']
)
