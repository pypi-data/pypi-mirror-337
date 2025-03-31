#!/usr/bin/env python
# -*- encoding: utf8 -*-
import io
import os

from setuptools import setup, find_packages
from distutils.core import Extension #from setuptools import Extension #has a slightly different syntax
import numpy
import glob

long_description = """
Source code: https://github.com/aaspip/aaspip""".strip() 


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")).read()

## below compile seistr
dipc_module = Extension('dipcfun', sources=['aaspip/seistr/src/dip_cfuns.c'], 
										include_dirs=[numpy.get_include()])
sofc_module = Extension('sofcfun', sources=['aaspip/seistr/src/sof_cfuns.c'], 
										include_dirs=[numpy.get_include()])
sofc3d_module = Extension('sof3dcfun', sources=['aaspip/seistr/src/sof3d_cfuns.c'], 
										include_dirs=[numpy.get_include()])
sointc3d_module = Extension('soint3dcfun', sources=['aaspip/seistr/src/soint3d_cfuns.c'], 
										include_dirs=[numpy.get_include()])
sointc2d_module = Extension('soint2dcfun', sources=['aaspip/seistr/src/soint2d_cfuns.c'], 
										include_dirs=[numpy.get_include()])
bpc_module = Extension('bpcfun', sources=['aaspip/seistr/src/bp_cfuns.c'], 
										include_dirs=[numpy.get_include()])
cohc_module = Extension('cohcfun', sources=['aaspip/seistr/src/coh_cfuns.c'], 
										include_dirs=[numpy.get_include()])
paintc2d_module = Extension('paint2dcfun', sources=['aaspip/seistr/src/paint_cfuns.c'], 
										include_dirs=[numpy.get_include()])

## below compile ekfmm								
eikonalc_module = Extension('eikonalc', sources=['aaspip/ekfmm/src/eikonal.c'], 
										include_dirs=[numpy.get_include()])

eikonalvtic_module = Extension('eikonalvtic', sources=['aaspip/ekfmm/src/eikonalvti.c'], 
										include_dirs=[numpy.get_include()])				


## below compile wave	
aps_module = Extension('apscfun', sources=['aaspip/wave/src/aps.c',
                                                'aaspip/wave/src/wave_psp.c',
                                                'aaspip/wave/src/wave_ricker.c',
                                                'aaspip/wave/src/wave_abc.c',
                                                'aaspip/wave/src/wave_fft2.c',
                                                'aaspip/wave/src/wave_fft3.c',
                                                'aaspip/wave/src/wave_freqfilt.c',
                                                'aaspip/wave/src/wave_alloc.c',
                                                'aaspip/wave/src/wave_kissfft.c',
                                                'aaspip/wave/src/wave_komplex.c',
                                                'aaspip/wave/src/wave_conjgrad.c',
                                                'aaspip/wave/src/wave_cdivn.c',
                                                'aaspip/wave/src/wave_ctriangle.c',
                                                'aaspip/wave/src/wave_ctrianglen.c',
                                                'aaspip/wave/src/wave_cntriangle.c',
                                                'aaspip/wave/src/wave_cntrianglen.c',
                                                'aaspip/wave/src/wave_decart.c',
                                                'aaspip/wave/src/wave_win.c',
                                                'aaspip/wave/src/wave_memcpy.c',
                                                'aaspip/wave/src/wave_fft1.c'],
										depends=glob.glob('aaspip/wave/src/*.h'),
                                                include_dirs=[numpy.get_include()])

afd_module = Extension('afdcfun', sources=['aaspip/wave/src/afd.c',
                                                'aaspip/wave/src/wave_fdm.c',
                                                'aaspip/wave/src/wave_psp.c',
                                                'aaspip/wave/src/wave_ricker.c',
                                                'aaspip/wave/src/wave_abc.c',
                                                'aaspip/wave/src/wave_fft2.c',
                                                'aaspip/wave/src/wave_fft3.c',
                                                'aaspip/wave/src/wave_freqfilt.c',
                                                'aaspip/wave/src/wave_alloc.c',
                                                'aaspip/wave/src/wave_kissfft.c',
                                                'aaspip/wave/src/wave_komplex.c',
                                                'aaspip/wave/src/wave_conjgrad.c',
                                                'aaspip/wave/src/wave_cdivn.c',
                                                'aaspip/wave/src/wave_ctriangle.c',
                                                'aaspip/wave/src/wave_ctrianglen.c',
                                                'aaspip/wave/src/wave_cntriangle.c',
                                                'aaspip/wave/src/wave_cntrianglen.c',
                                                'aaspip/wave/src/wave_decart.c',
                                                'aaspip/wave/src/wave_win.c',
                                                'aaspip/wave/src/wave_memcpy.c',
                                                'aaspip/wave/src/wave_fft1.c'],
										depends=glob.glob('aaspip/wave/src/*.h'),
                                                include_dirs=[numpy.get_include()])

pfwi_module = Extension('pfwicfun', sources=['aaspip/wave/src/pfwi.c',
                                                'aaspip/wave/src/wave_fwi.c',
                                                'aaspip/wave/src/wave_fwiutil.c',
                                                'aaspip/wave/src/wave_fwigradient.c',
                                                'aaspip/wave/src/wave_fwilbfgs.c',
                                                'aaspip/wave/src/wave_fwimodeling.c',
                                                'aaspip/wave/src/wave_triutil.c',
                                                'aaspip/wave/src/wave_bigsolver.c',
                                                'aaspip/wave/src/wave_cgstep.c',
                                                'aaspip/wave/src/wave_butter.c',
                                                'aaspip/wave/src/wave_chain.c',
                                                'aaspip/wave/src/wave_fdm.c',
                                                'aaspip/wave/src/wave_psp.c',
                                                'aaspip/wave/src/wave_ricker.c',
                                                'aaspip/wave/src/wave_abc.c',
                                                'aaspip/wave/src/wave_fft2.c',
                                                'aaspip/wave/src/wave_fft3.c',
                                                'aaspip/wave/src/wave_freqfilt.c',
                                                'aaspip/wave/src/wave_alloc.c',
                                                'aaspip/wave/src/wave_kissfft.c',
                                                'aaspip/wave/src/wave_komplex.c',
                                                'aaspip/wave/src/wave_conjgrad.c',
                                                'aaspip/wave/src/wave_cdivn.c',
                                                'aaspip/wave/src/wave_triangle.c',
                                                'aaspip/wave/src/wave_ctriangle.c',
                                                'aaspip/wave/src/wave_ctrianglen.c',
                                                'aaspip/wave/src/wave_cntriangle.c',
                                                'aaspip/wave/src/wave_cntrianglen.c',
                                                'aaspip/wave/src/wave_blas.c',
                                                'aaspip/wave/src/wave_blasc.c',
                                                'aaspip/wave/src/wave_decart.c',
                                                'aaspip/wave/src/wave_win.c',
                                                'aaspip/wave/src/wave_memcpy.c',
                                                'aaspip/wave/src/wave_fft1.c'],
										depends=glob.glob('aaspip/wave/src/*.h'),
                                                include_dirs=[numpy.get_include()])

## below compile npre	
nprec3d_module = Extension('npre3dcfun', sources=['aaspip/npre/src/npre3d.c',
												'aaspip/npre/src/npre_fxynpre.c',
												'aaspip/npre/src/npre_alloc.c',
												'aaspip/npre/src/npre_kissfft.c',
												'aaspip/npre/src/npre_komplex.c',
												'aaspip/npre/src/npre_conjgrad.c',
												'aaspip/npre/src/npre_cdivn.c',
												'aaspip/npre/src/npre_triangle.c',
												'aaspip/npre/src/npre_trianglen.c',
												'aaspip/npre/src/npre_ntriangle.c',
												'aaspip/npre/src/npre_ntrianglen.c',		
												'aaspip/npre/src/npre_decart.c',	
												'aaspip/npre/src/npre_win.c',	
												'aaspip/npre/src/npre_memcpy.c',			
												'aaspip/npre/src/npre_fft1.c'], 
										depends=glob.glob('aaspip/npre/src/*.h'),
                                                include_dirs=[numpy.get_include()])

ftfa_module = Extension('ftfacfun', sources=['aaspip/npre/src/tf.c',
                                                'aaspip/npre/src/npre_fxynpre.c',
                                                'aaspip/npre/src/npre_alloc.c',
                                                'aaspip/npre/src/npre_kissfft.c',
                                                'aaspip/npre/src/npre_komplex.c',
                                                'aaspip/npre/src/npre_conjgrad.c',
                                                'aaspip/npre/src/npre_cdivn.c',
                                                'aaspip/npre/src/npre_triangle.c',
                                                'aaspip/npre/src/npre_trianglen.c',
                                                'aaspip/npre/src/npre_ntriangle.c',
                                                'aaspip/npre/src/npre_ntrianglen.c',
                                                'aaspip/npre/src/npre_decart.c',
                                                'aaspip/npre/src/npre_win.c',
                                                'aaspip/npre/src/npre_memcpy.c',
                                                'aaspip/npre/src/npre_fft1.c'],
										depends=glob.glob('aaspip/npre/src/*.h'),
                                                include_dirs=[numpy.get_include()])

## below compile ntfa
ntfac_module = Extension('ntfacfun', sources=['aaspip/ntfa/src/main.c',
											  'aaspip/ntfa/src/ntfa_alloc.c',
											  'aaspip/ntfa/src/ntfa_blas.c',
											  'aaspip/ntfa/src/ntfa_divnnsc.c',
											  'aaspip/ntfa/src/ntfa_conjgrad.c',
											  'aaspip/ntfa/src/ntfa_weight2.c',
											  'aaspip/ntfa/src/ntfa_decart.c',
											  'aaspip/ntfa/src/ntfa_triangle.c',
											  'aaspip/ntfa/src/ntfa_ntriangle.c',
											  'aaspip/ntfa/src/ntfa_ntrianglen.c'	],
										depends=glob.glob('aaspip/ntfa/src/*.h'),
                                        include_dirs=[numpy.get_include()])
                                                                
## below compile ortho
orthoc_module = Extension('orthocfun', sources=['aaspip/ortho/src/orthocfuns.c'], 
										include_dirs=[numpy.get_include()])

## below compile radon
radonc_module = Extension('radoncfun', sources=['aaspip/radon/src/radon.c','aaspip/radon/src/adjnull.c'],include_dirs=[numpy.get_include()])
                                                                
modules=[]
modules=modules+[dipc_module,sofc_module,sofc3d_module,sointc2d_module,sointc3d_module,bpc_module,paintc2d_module,cohc_module]
modules.append(eikonalc_module)
modules.append(eikonalvtic_module)
modules=modules+[aps_module,afd_module,pfwi_module]
modules=modules+[nprec3d_module,ftfa_module]
modules.append(ntfac_module)
modules.append(orthoc_module)
modules.append(radonc_module)
    
setup(
    name="aaspip",
    version="0.0.0.1",
    license='MIT License',
    description="AASPIP: Advanced Array Seismic Data Processing and Imaging Platform",
    long_description=long_description,
    author="aaspip developing team",
    author_email="chenyk2016@gmail.com",
    url="https://github.com/aaspip/aaspip",
    ext_modules=modules,
    packages=find_packages(),
    include_package_data=True,
#     exclude_package_data={
#             'aaspip.seistr': ['*'],
#             'aaspip.seistr': ['src/*'],
#             'aaspip.ekfmm': ['src/*'],
#     },
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    keywords=[
        "seismology", "earthquake seismology", "exploration seismology", "array seismology", "denoising", "science", "engineering", "structure", "local slope", "filtering"
    ],
    install_requires=[
        "numpy", "scipy", "matplotlib"
    ],
    extras_require={
        "docs": ["sphinx", "ipython", "runipy"]
    }
)
