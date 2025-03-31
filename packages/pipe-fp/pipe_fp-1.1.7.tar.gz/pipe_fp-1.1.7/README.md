# ➡️ Pipe fp

### Functional piping for Python.
Simple ⬦ Clear ⬦ Concise

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/A-4S/pipe-fp/python-app.yml?logo=github&label=unit%20test&style=for-the-badge)](https://github.com/A-4S/pipe-fp/actions/workflows/python-app.yml) [![PyPI - Version](https://img.shields.io/pypi/v/pipe-fp?style=for-the-badge)](https://pypi.org/project/pipe-fp/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipe-fp?style=for-the-badge)](https://pypi.org/project/pipe-fp/)

---
## Background
Piping is a method targeting code composition style, taking input data and passing it through a series of functions to produce a final output data.

## Usage
Pipe fp is a tool to compose code in a simple, clear, and concise manner.
### Example

```python
from pipe_fp import pipe


pipe(
  str.lower,
  str.title,
  str.split
)('WHY, HELLO THERE! 🐰')
``` 
### Returns

```python
['Why,', 'Hello', 'There!', '🐰']
```
