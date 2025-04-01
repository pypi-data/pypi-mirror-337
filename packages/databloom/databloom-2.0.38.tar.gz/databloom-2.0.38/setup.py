from setuptools import setup, find_packages
import os
import re

def get_version():
    """Get version from version.py."""
    version_file = os.path.join('databloom', 'version.py')
    with open(version_file, 'r') as f:
        content = f.read()
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def read_requirements(filename):
    """Read requirements from file."""
    requirements = []
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('-r'):
                    continue
                requirements.append(line)
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        return []
    return requirements

# Read requirements without importing
requirements = read_requirements('requirements.txt')
dev_requirements = read_requirements('requirements-dev.txt')

# Read long description from README
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='databloom',
    version=get_version(),
    description='A Python SDK client for data source connections and data warehouse integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nam Vu',
    author_email='namvq@databloom.ai',
    url='https://github.com/databloom-ai/connector',
    packages=find_packages(exclude=['tests*', 'example*', 'docs*']),
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='data, warehouse, connector, sdk',
) 