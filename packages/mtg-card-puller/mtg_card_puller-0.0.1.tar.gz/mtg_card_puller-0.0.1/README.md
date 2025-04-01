# mtg_card_puller

Pull MTG card images in b

## Installation
To setup mtg_card_puller create a conda environment with the generated `environment.yaml`.
This sets up a development environment with all the required packages. This is what is used when building 
out the functionality of this project.
```bash
conda env create -f environment.yaml
conda activate mtg_puller
```

Then install the python module. This installs the module the same way as if someone just wanting 
to use this package would install it. This is what is used when using this package as a dependency.
**Note:** This installs the `dev` extra dependencies. When installing this to use as a standalone package,
you should leave off the `[dev]` part.
```bash
python -m pip install .[dev]
```

If functionality from this repo is needed in another project, you can install this package as a dependency
directly from the GitHub repo.
```bash
python -m pip install git+https://github.com/seerai/mtg_card_puller.git
```

You can then test that the docker image builds and runs correctly.
```bash
docker build -t mtg_card_puller:latest .
```
Once the build is complete, test the image:
```bash
docker run --rm mtg_card_puller:latest
```
You should see a message printed:
```
Replace this message by putting your code into mtg_card_puller.cli.main
See click documentation at https://click.palletsprojects.com/
```

## Development

### READMEs and Notes
Every folder in this project other than `mtg_card_puller`` should have a README.md
file (the template does this automatically for all folders). Each of these READMEs should be kept 
up to date and should describe the contents of the folder. This is especially important for the
the data folder and should include all data files, their sources and how to download them. This
is also a good place to put any notes about the contents of the folder. For example, if you are
working on a notebook and want to save some notes about what you are doing, you can put them in
the README for that folder. **You should always be asking yourself** "If someone else were to look at
this folder, would they know what is going on?". If the answer is no, then you should add more
information to the README.

### Dependency Management
When developing on this project, **make sure that you never directly `pip install` any packages**. This
leads to situations where peoples environemnts are different and the code will not run correctly
when another person tries to install the package. Instead, always add the dependency to the
`pyproject.toml` file and reinstall the package. This ensures that all dependencies are tracked and
others can use this package without issue. When possible, you should also pin a version or version range
of the dependency. i.e. `numpy==1.19.2` or `numpy>=1.19.2,<1.20.0`.

### Testing
Any functions implemened in this package should be covered by tests if possible. This doesnt mean that
every line of code needs to be tested, but that the functionality of the code is tested. Anything 
that is used only for development purposes can sometimes be excluded from testing. However, any 
function/class you expect someone to use after installing this as a package should be tested. 
**You should always be asking yourself** "If someone else were to use this code, would they know that it
works correctly?". If the answer is no, then you should add tests.

This project uses `pytest` for testing. To run the tests, cd to the root of the project and run:
```bash
coverage run -m pytest
```
This will run all the tests and generate a coverage report. To view the coverage report, run:
```bash
coverage report
```
