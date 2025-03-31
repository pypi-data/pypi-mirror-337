
# Flowtune Python SDK (v1.2.0)

Flowtune Python SDK now supports auto configuration for optimized resource loading.

## What's New in v1.2.0

- Auto configuration support (`auto_config`)
- Easier and quicker setup for optimized loading strategies

## Installation

```bash
pip install flowtune
```

## Usage

```python
from flowtune.parser import QuantumFlowtuneParser
from flowtune.executor import QuantumFlowtuneExecutor

parser = QuantumFlowtuneParser('auto_demo.ft')
parser.parse(auto_config=True)

executor = QuantumFlowtuneExecutor(parser.resources, parser.groups, parser.execution_plan)
executor.run()
```

## License

MIT
