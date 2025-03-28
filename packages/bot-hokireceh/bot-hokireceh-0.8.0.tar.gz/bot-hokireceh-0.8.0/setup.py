from setuptools import setup, find_packages

setup(
    name='bot-hokireceh',
    version='0.8.0',
    description='Bot Telegram untuk komunitas Hoki Receh',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HokiReceh',
    author_email='ads.hokireceh@gmail.com',
    url='https://codeberg.org/pemulungrupiah/bot-hokireceh',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot',
        'aiohttp',
        'aiogram==3.19.0',
        'python-dotenv',
        'requests',
        'yt-dlp',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
