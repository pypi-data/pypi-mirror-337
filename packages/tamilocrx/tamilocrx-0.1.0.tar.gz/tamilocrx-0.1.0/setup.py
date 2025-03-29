from setuptools import setup, find_packages

setup(
    name='tamilocrx',
    version='0.1.0',
    author='Aro Barath Chandru B',
    author_email='chandru2021007@gmail.com',
    description='A Tamil OCR engine using PARSeq and CRAFT',
    long_description=open('README.md', encoding='utf-8').read(),  # ✅ only once
    long_description_content_type='text/markdown',
    url='https://github.com/cyber-bytezz/tamilocrx',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'torch',
        'torchvision',
        'gradio',
        'pytorch-lightning==1.9.5',
        'opencv-python',
        'numpy',
        'tqdm',
        'pillow',
        'scikit-image',
        'timm',
        'pyyaml',
        'gdown',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
