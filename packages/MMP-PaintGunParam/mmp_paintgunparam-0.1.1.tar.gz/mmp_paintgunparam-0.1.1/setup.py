from setuptools import setup

setup(
    name='MMP_PaintGunParam',
    version='0.1.1',
    description='Package allowing operations of a paint gun controller installed on a robot.',
    url='https://github.com/neurobotia/MMP-PaintGunParam/MMP_PaintGunParam',
    author='Technologies NeuroBotIA Inc.',
    author_email='michel.lessard@neurobotia.com',
    license='None',
    packages=['MMP_PaintGunParam'],
    install_requires=['open3d==0.18.0',
                      'numpy==1.26.4',
                      'PyYAML==6.0',
                      'pyModbusTCP==0.2.1'],
)
