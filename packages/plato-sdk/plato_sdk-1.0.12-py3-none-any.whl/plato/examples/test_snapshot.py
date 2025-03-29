import asyncio
from plato.sdk import Plato

async def test_snapshot():
    client = Plato(base_url="http://localhost:25565/api")
    await client.process_snapshot("8a51809d-3c2a-4cfc-a492-a90e6c771f44")

if __name__ == "__main__":
    asyncio.run(test_snapshot())
