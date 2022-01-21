from setuptools import setup

setup(
    name='autopylot',
    version='0.0.1',
    description='An RC autonomous car python library',
    url='https://github.com/Autonomobile/AutoPylot',
    author='Autonomobile',
    license='MIT',
    packages=['autopylot'],
    install_requires=[
        'opencv-python >= 4.1.1',
        'tensorflow >= 2.3.2',
        'numpy >= 1.17',
        'pyserial',
    ],
)
