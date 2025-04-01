"""
Setup script for the szn-libeaas package.
"""
from setuptools import setup, find_packages
from setuptools.command.install import install

# Read long description from README
with open('README.md', 'r') as f:
    long_description = f.read()

# Create a custom install command that runs post-install functionality
class CustomInstall(install):
    def run(self):
        install.run(self)
        # Import and run the post-install function directly
        try:
            from szn_libeaas import post_install
            post_install.run_post_install()
        except Exception as e:
            print(f"Note: Post-installation documentation fetch encountered an issue: {e}")
            print("This does not affect the installation. The package is installed correctly.")
            print("Documentation is available at: https://opicevopice.github.io/")

setup(
    name='szn-libeaas',
    version='3.0.2',  # Directly specify version
    description='Enterprise as a Service Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Roman Skvara',  # Directly specify author
    author_email='skvara.roman@gmail.com',
    url='https://github.com/opicevopice/szn-libeaas',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.0',
        'requests-html>=0.10.0',  # Added for open_readme functionality
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'black>=20.8b1',
            'flake8>=3.8.0',
            'mypy>=0.800',
            'twine>=3.3.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'szn-libeaas-info=szn_libeaas.post_install:run_post_install',
        ],
    },
    keywords='api, enterprise, client, sdk',
    project_urls={
        'Source': 'https://github.com/opicevopice/szn-libeaas',
        'Tracker': 'https://github.com/opicevopice/szn-libeaas/issues',
    },
    cmdclass={
        'install': CustomInstall,
    },
)
