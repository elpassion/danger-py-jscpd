[![PyPI](https://img.shields.io/pypi/v/danger-py-cov)](https://pypi.org/project/danger-py-jscpd/)
![Python versions](https://img.shields.io/pypi/pyversions/danger-py-jscpd)
[![Build Status](https://travis-ci.com/elpassion/danger-py-jscpd.svg?token=nu9zU1tfHq8GJSir3pVq&branch=master)](https://travis-ci.com/elpassion/danger-py-jscpd)

# danger-py-jscpd

The plugin parses the [jscpd]((https://github.com/kucherenko/jscpd)) report json and visualizes how the pull request affects the results. The jscpd tool gives you the ability to find duplicated code.

<h3 align="center">
  <a href="https://www.elpassion.com">
    <img src="readme/elpassion.png" alt="Find your EL Passion"/>
  </a>
</h3>


## Example output in PR

### JSCPD found 3 clone(s)
| First | Second |
| ----- | ------ |
| examples/babi_rnn.py: 91-123 | examples/babi_memnn.py: 46-79 |
| examples/babi_rnn.py: 124-131 | examples/babi_memnn.py: 80-87 |
| examples/cifar10_resnet.py: 344-355 | examples/cifar10_resnet.py: 248-259 |


## Installation

```sh
# install danger-js
npm install -g danger
# install jscpd
npm install -g jscpd
# install danger-python
pip install danger-python
# install danger-py-jscpd
pip install danger-py-jscpd
# modify dangerfile.py to include plugin
danger_py_jscpd.jscpd()
# run danger-python
danger-python pr https://github.com/elpassion/danger-py-jscpd/pull/2
```

Add following to the `dangerfile.py`:

```python
import danger_py_jscpd

danger_py_jscpd.jscpd()
```

## Development

To develop the new features, clone the repository and then run:

```sh
# install dependencies
poetry install 
# activate virtual environment
poetry shell 
# run the test suite
pytest 
```

## License

`danger-py-jscpd` is released under an MIT license. See [LICENSE](https://github.com/elpassion/danger-py-jscpd/blob/master/LICENSE) for more information.
