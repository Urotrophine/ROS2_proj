from setuptools import find_packages, setup

package_name = 'voice_ctrl_jazzy'

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
    maintainer='quzikun',
    maintainer_email='12411402@mail.sustech.edu.cn',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'asr_node = voice_ctrl_jazzy.asr_node:main',
        'shape_drawer = voice_ctrl_jazzy.shape_drawer:main',
        ],
    },
)
