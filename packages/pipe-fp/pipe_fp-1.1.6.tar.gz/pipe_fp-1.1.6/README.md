# ➡️ Pipe fp

### Functional piping for Python.

- Easy
- Clear
- Concise

## Usage
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
