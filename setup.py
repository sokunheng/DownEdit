from setuptools import setup, find_packages

setup(
    name='downedit',
    version='2.4.0', 
    packages=find_packages(), 
    install_requires=[
        'pystyle', 'requests', 'inquirer', 'colorama', 'moviepy', 'rich',
        'requests-html', 'requests-random-user-agent', 'playwright',
        'undetected-chromedriver', 'beautifulsoup4', 'selenium', 'numpy',
        'scikit-image', 'torch', 'torchvision', 'tensorboard', 'pillow',
        'opencv-python', 'gdown', 'wmi', 'psutil'
    ],
    entry_points={
        'console_scripts': [
            'downedit = downedit.cli.__main__:main' 
        ]
    }
)