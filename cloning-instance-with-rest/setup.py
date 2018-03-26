from setuptools import setup
setup(
    name='appid_instance_copy',
    packages=['appid_instance_copy'],
    entry_points={
        'console_scripts' : [
            'appidc = appid_instance_copy.copy_config:main',
        ]
    },
    install_requires=[
        'requests',
    ]
)