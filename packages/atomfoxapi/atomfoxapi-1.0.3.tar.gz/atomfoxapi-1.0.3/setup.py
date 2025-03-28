import setuptools

setuptools.setup(
	name='atomfoxapi',
	version='1.0.3',
	author='mc_c0rp',
	author_email='mc.c0rp@icloud.com',
	description='ATOM API.',
	packages=['atomfoxapi'],
	install_requires=["requests", "pydantic"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)