<br/>
<p align="center">
  <a href="https://github.com/mtralka/EOPlatform">
    <img src="images/logo.jpg" alt="EOP Logo" width="300" height="300">
  </a>

  <h3 align="center">An Earth Observation Platform</h3>

  <p align="center">
    Earth Observation made easy. 
    <br/>
    <br/>
    <a href="https://github.com/mtralka/EOPlatform/issues">Report Bug</a>
    |
    <a href="https://github.com/mtralka/EOPlatform/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/mtralka/EOPlatform/total) ![Forks](https://img.shields.io/github/forks/mtralka/EOPlatform?style=social) ![Stargazers](https://img.shields.io/github/stars/mtralka/EOPlatform?style=social) <br/> ![Issues](https://img.shields.io/github/issues/mtralka/EOPlatform) ![License](https://img.shields.io/github/license/mtralka/EOPlatform) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![mypy](https://img.shields.io/badge/mypy-checked-brightgreen)

## About

*eoplatform* is a Python package that aims to simplify Remote Sensing Earth Observation by providing actionable information on a wide swath of RS platforms and provide a simple API for downloading and visualizing RS imagery. Made for scientsits, educators, and hobbiests alike.

* Easy to access **information** on RS platforms
  * Band information
  * Orbit regimes
  * Scene statistics
* Accessible data downloading (in-progress)
  * Landsat 8
  * Sentinel-2
* Common band composites

### Installation

`eoplatform` can be installed by running `pip install eoplatform`. It requires Python 3.7 or above to run. 

If you want to install the latest version from git you can run 

```sh
pip install git+git://github.com/mtralka/eoplatform
```

### Example

<img src="images/eoplatform-info-landsat8.PNG" alt="Landsat8 Info" width="600">

## Usage

*eoplatform* is fully accessible through the command line (CLI) and as a module import.

### Querying platform info

#### CLI

`PLATFORM` argument is case-insensitive

```sh
Usage: eoplatform info [OPTIONS] PLATFORM

Arguments:
  PLATFORM  [required]

Options:
  -d, --description / -nd, --no-description
                                  [default: description]     
  --help                          Show this message and exit.
```

EX:

```sh
eoplatform info landsat8
```

show all info *eoplatform* has on `Landsat8`

```sh
eoplatform info landsat8 -b
```

shows only `Landsat8`'s bands

#### Module import

You can import your desired platform

```python
from eoplatform import landsat8

landsat8.info()  # OR print(landsat8)
```

or search from the *eoplatform* module itself

```python
import eoplatform as eop

eop.info("Landsat8")  # case insensitive
```

### Downloading platform scenes

#### CLI

in-progress

```sh
Usage: eoplatform download [OPTIONS] PLATFORM

Arguments:
  PLATFORM  [required]

Options:
  --help  Show this message and exit.
```

#### Module import

 in-progress

 ```python
from eoplatform import landsat8

landsat8.download()
```

```python
import eoplatform as eop

eop.download("landsat8")
```

both methods accept the full range of search keword arguments

## Roadmap

See the [open issues](https://github.com/mtralka/EOPlatform/issues) for a list of proposed features (and known issues).

* download support


## Contributing

Contributions are welcome. Currently, *eoplatform* is undergoing rapid development and contribution opportunities may be scarce.

* If you have suggestions for adding or removing features, feel free to [open an issue](https://github.com/mtralka/EOPlatform/issues/new) to discuss it, or directly create a pull request with the proposed changes.
* Create individual PR for each suggestion.
* Use pre-commit hooks - `pre-commit install`
* Code style is `black`, `mypy --strict`

## License

Distributed under the GNU GPL-3.0 License. See [LICENSE](https://github.com/mtralka/EOPlatform/blob/main/LICENSE.md) for more information.

## Built With

* [Rich](https://github.com/willmcgugan/rich)
* [Typer](https://github.com/tiangolo/typer)

## Authors

* [**Matthew Tralka**](https://github.com/mtralka/)
