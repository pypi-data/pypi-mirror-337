from setuptools import setup, find_packages

#==============================================================================

setup(
    #----------------------------------
    # metadata

    name='junpy-dataset',
    description='JunPy-dataset is a collection of data used in JunPy tests and examples.',
    url='https://labstt.phy.ncu.edu.tw/junpy',
    author='Bao-Huei Huang',
    author_email='lise811020@gmail.com',
    license='GPL',
    platforms=['Unix', 'macOS', 'Windows'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'],

    #----------------------------------
    # package information

    packages=find_packages(),
    python_requires='>=3.6.0',
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)

#==============================================================================
