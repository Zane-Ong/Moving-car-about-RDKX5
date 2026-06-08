from setuptools import find_packages, setup

package_name = 'car_function'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sunrise',
    maintainer_email='sunrise@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'medicinedetect = car_function.medicinedetect:main',
            'AngleCorrectionNode = car_function.AngleCorrectionNode:main',
            'Correctangle = car_function.Correctangle:main',
        ],
    },
)
