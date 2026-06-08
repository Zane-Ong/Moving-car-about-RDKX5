from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtlebot3_cartographer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name, 'launch'),glob(os.path.join('launch','*launch.py'))),
        (os.path.join('share',package_name, 'launch'),glob(os.path.join('launch','*launch.xml'))),
        (os.path.join('share',package_name, 'rviz'),glob(os.path.join('rviz','*.rviz*'))),
        (os.path.join('share', package_name, 'params'), glob(os.path.join('params', '*.*'))),
        (os.path.join('share', package_name, 'maps'), glob(os.path.join('maps', '*.*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zungit',
    maintainer_email='zungit@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'setinitpose_node = turtlebot3_cartographer.setinitpose_node:main',
        ],
    },
)
