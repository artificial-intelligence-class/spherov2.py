from setuptools import setup, find_namespace_packages

with open('README.md', 'rt', encoding='utf_8') as f:
    long_desc = f.read()

setup(
    name='spherov2',
    version='0.11.1',
    author='Hanbang Wang', # and 'Elionardo Feliciano',
    author_email='hanbangw@cis.upenn.edu', # and 'elionardo.feliciano.dev@gmail.com',
    license='MIT',
    description='An unofficial Bluetooth low energy library for Sphero toys in Python.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/artificial-intelligence-class/spherov2.py',
    packages=find_namespace_packages(include=['spherov2', 'spherov2.*'],
                                     exclude=["*.test", "*.test.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Robot Framework :: Library',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='robotics Sphero toy bluetooth ble',
    python_requires='>=3.7',
    install_requires=['numpy', 'transforms3d']
)
