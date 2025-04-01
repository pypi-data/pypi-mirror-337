# ICE Connect

ICE Connect is a Python package that implements Interactive Connectivity Establishment (ICE) as specified in RFC 5245.
It allows dynamic STUN server configuration for gathering local candidates.

## Installation
```sh
pip install ice_connect
```

## Usage
```python
from ice_connect import IceAgent
import asyncio

async def main():
    agent = IceAgent(stun_server="stun.l.google.com")
    await agent.gather_local_candidates()
    agent.add_remote_candidate("192.168.1.2", 3478)
    success = await agent.establish_connection()
    if success:
        print("Connection verified with HELLO message exchange.")
    else:
        print("Connection could not be established.")

asyncio.run(main())
```
