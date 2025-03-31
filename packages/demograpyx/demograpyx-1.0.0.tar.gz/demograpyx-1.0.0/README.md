# demograpyx

A set of asynchronous bindings for the three Demograpix APIs: [`genderize`](https://genderize.io/), [`agify`](https://agify.io) and [`nationalize`](https://nationalize.io)

## Installation

Requires Python 3.10 or newer

```sh
$ pip install demograpyx
```

## Example usage

Functions are identical across all three API clients (`predict`, `batch_predict`)

```py
import asyncio
from demograpyx import Genderize, CountryCode

async def main() -> None:
    genderize = await Genderize.create() # optionally pass api_key kwarg for API key
    # alternatively, initialise an aiohttp.ClientSession and pass it as a kwarg
    # genderize = Genderize(session=aiohttp.ClientSession())

    data = await genderize.predict("Mike", country_id=CountryCode.UnitedStates) # country_id argument is optional, will improve prediction accuracy
    print(data)
    # GenderPrediction(count=675221, name='Mike', gender='male', probability=1.0, country_id='US')

if __name__ == "__main__":
    asyncio.run(main())
```