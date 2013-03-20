from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from poly_coeff_expr import coeff_expr
from mako.template import Template

import numpy as np

mako_targets = {'poly_coeff{}.c'.format(i): ('poly_coeffX.c.mako', coeff_expr(i)) for i \
                in range(1, 6, 2)}

def render_mako_template_to(template_path, outpath, subsd):
    template_str = open(template_path, 'rt').read()
    ofh = open(outpath, 'wt')
    ofh.write(Template(template_str).render(**subsd))
    ofh.close()


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

setup(
    cmdclass = {'build_ext': my_build_ext},
    include_dirs =  [np.get_include()],
    ext_modules = [Extension("cinterpol", ["cinterpol.pyx", 'newton_interval.c'] +\
                             mako_targets.keys())],
)

