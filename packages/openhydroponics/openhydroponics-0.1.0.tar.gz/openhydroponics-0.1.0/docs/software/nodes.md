# Nodes

The Node Manager is a central component that manages all the nodes in your hydroponic system.

Nodes are individual components that perform specific tasks within the hydroponic system. They can have sensors, actuators, or controllers.

All applications need a [NodeManager](node_manager.NodeManager)

Example:

```python
import asyncio

from openhydroponics.node_manager import NodeManager


async def main():
    nm = NodeManager()
    await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

```

Getting a reference to a node object use the function [NodeManager.get_node()](openhydroponics.node_manager.NodeManager.get_node)
or [NodeManager.request_node()](openhydroponics.node_manager.NodeManager.request_node).

## Endpoints

All nodes have one or several endpoints. A node that supports temperature and humidity may have two endpoints, one for each
sensor. If a node supports multiple variants of the same type of sensor or actuators each individual sensor/actuator will have
its own endpoint. Example: A node with 3 pump outlets will have three endpoints, one for each pump.

## API reference

```{eval-rst}
.. automodule:: openhydroponics.node_manager
    :members:
    :undoc-members:
```
