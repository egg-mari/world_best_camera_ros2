from setuptools import find_packages, setup
import glob
import os
package_name = 'camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob.glob(os.path.join('launch', '*.launch.py'))),
        ('share/' + package_name + '/param',
            glob.glob(os.path.join('param', '*.yaml'))),
            ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jun',
    maintainer_email='ksg77772000@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera = camera.camera:main',
            'edge = camera.edge:main',
            'Sharpening = camera.Sharpening:main',
            'median = camera.median:main',
            'blur = camera.blur:main',
            'rens = camera.rens:main',
            'bolok = camera.bolok:main',
            'record = camera.record:main'
        ],
    },
)