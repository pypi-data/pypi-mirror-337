from setuptools import setup


setup(
  name = 'invoice-crafter',
  packages = ['invoicing'],
  version = '1.0.0',         #* To be increased every time the library is changed
  license='MIT',             # Type of license
  description = 'This package converts Excel invoice files into PDF invoices. '
                'Simply provide an input and output directories, and also parameters to generate a PDF invoice for each file.',
  author = 'Anna Balitska',
  author_email = 'aa.llin.223@gmail.com',
  url = 'https://github.com/Xannii',
  keywords = ['invoice', 'excel', 'pdf', 'crafter'],
  install_requires=['pandas', 'fpdf', 'openpyxl'],     # 3rd-party libs that pip needs to install
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
