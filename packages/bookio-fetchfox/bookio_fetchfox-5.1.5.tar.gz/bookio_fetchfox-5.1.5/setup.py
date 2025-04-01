# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetchfox',
 'fetchfox.apis',
 'fetchfox.apis.algorand',
 'fetchfox.apis.algorand.algonodecloud',
 'fetchfox.apis.algorand.nfdomains',
 'fetchfox.apis.algorand.randswapcom',
 'fetchfox.apis.cardano',
 'fetchfox.apis.cardano.dexhunterio',
 'fetchfox.apis.cardano.gomaestroorg',
 'fetchfox.apis.cardano.jpgstore',
 'fetchfox.apis.coingeckocom',
 'fetchfox.apis.evm',
 'fetchfox.apis.evm.ensideascom',
 'fetchfox.apis.evm.moralisio',
 'fetchfox.apis.evm.openseaio',
 'fetchfox.blockchains',
 'fetchfox.blockchains.algorand',
 'fetchfox.blockchains.cardano',
 'fetchfox.blockchains.ethereum',
 'fetchfox.blockchains.evm',
 'fetchfox.blockchains.polygon',
 'fetchfox.constants',
 'fetchfox.constants.algorand',
 'fetchfox.constants.cardano',
 'fetchfox.constants.cardano.pools',
 'fetchfox.constants.cardano.tokens',
 'fetchfox.constants.ethereum',
 'fetchfox.constants.evm',
 'fetchfox.constants.polygon',
 'fetchfox.dtos',
 'fetchfox.helpers',
 'fetchfox.pools',
 'fetchfox.tokens']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'backoff>=2.2.1,<3.0.0',
 'cachetools>=5.3.1,<6.0.0',
 'certifi>=2024.2.2,<2025.0.0',
 'pydantic>=2.10.3,<3.0.0',
 'pytz>=2024.2,<2025.0']

setup_kwargs = {
    'name': 'bookio-fetchfox',
    'version': '5.1.5',
    'description': 'Collection of API services to fetch information from several blockchains.',
    'long_description': '# book.io / fetchfox\n\n> Collection of API services to fetch information from several blockchains.\n\n![](https://s2.coinmarketcap.com/static/img/coins/64x64/4030.png)\n![](https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png)\n![](https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png)\n![](https://s2.coinmarketcap.com/static/img/coins/64x64/3890.png)\n\n\n## Supported Blockchains\n\n### Algorand\n\n```python\nimport os\nfrom fetchfox.blockchains import Algorand\n\nalgorand = Algorand()\n\n# Brave New World\ncreator_address = "6WII6ES4H6UW7G7T7RJX63CUNPKJEPEGQ3PTYVVU3JHJ652W34GCJV5OVY"\n\nfor asset in algorand.get_assets(creator_address):\n    print(asset)\n```\n\n#### Services\n\n* get_asset ([algonode.cloud](https://algonode.cloud))\n* get_assets ([algonode.cloud](https://algonode.cloud))\n* get_holdings ([algonode.cloud](https://algonode.cloud))\n* get_snapshot ([algonode.cloud](https://algonode.cloud))\n* get_listings ([randgallery.com](https://randgallery.com) / [algoxnft.com](https://algoxnft.com))\n* get_floor ([randgallery.com](https://randgallery.com) / [algoxnft.com](https://algoxnft.com))\n* get_sales ([nftexplorer.app¹](https://nftexplorer.app))\n\n\n### Cardano\n\n```python\nimport os\nfrom fetchfox.blockchains import Cardano\n\ncardano = Cardano(\n    gomaestroorg_api_key=os.getenv("GOMAESTROORG_API_KEY"),\n)\n\n# Gutenberg Bible\npolicy_id = "477cec772adb1466b301fb8161f505aa66ed1ee8d69d3e7984256a43"\n\nfor asset in cardano.get_collection_assets(policy_id):\n    print(asset)\n```\n\n#### Services\n\n* get_asset ([gomaestro.org²](https://gomaestro.org))\n* get_assets ([gomaestro.org²](https://gomaestro.org))\n* get_holdings ([gomaestro.org²](https://bgomaestro.org))\n* get_snapshot ([gomaestro.org²](https://gomaestro.org))\n* get_listings ([jpg.store](https://jpg.store))\n* get_floor ([jpg.store](https://jpg.store))\n* get_sales ([jpg.store](https://jpg.store))\n\n\n### EVM (Ethereum and Polygon)\n\n```python\nimport os\nfrom fetchfox.blockchains import Ethereum, Polygon\n\nethereum = Ethereum(\n    geckodriver_path=os.getenv("GECKODRIVER_PATH"),\n    moralisio_api_key=os.getenv("MORALIS_API_KEY"),\n    openseaio_api_key=os.getenv("OPENSEA_API_KEY"),\n)\n\npolygon = Polygon(\n    geckodriver_path=os.getenv("GECKODRIVER_PATH"),\n    moralisio_api_key=os.getenv("MORALIS_API_KEY"),\n    openseaio_api_key=os.getenv("OPENSEA_API_KEY"),\n)\n\n\n# Alice in Wonderland\ncontract_address = "0x919da7fef646226f88f70305201de392ff365059"\n\nfor asset in ethereum.get_assets(contract_address):\n    print(asset)\n\n# Art of War\ncontract_address = "0xb56010e0500e4f163758881603b8083996ae47ec"\n\nfor asset in polygon.get_assets(contract_address):\n    print(asset)\n```\n\n#### Services\n\n* get_asset ([moralis.io³](https://moralis.io))\n* get_assets ([moralis.io³](https://moralis.io))\n* get_holdings ([moralis.io³](https://moralis.io))\n* get_snapshot ([moralis.io³](https://moralis.io))\n* get_listings ([opensea.io⁴](https://opensea.io))\n* get_floor ([opensea.io⁴](https://opensea.io))\n* get_sales ([opensea.io⁴](https://opensea.io))\n\n\n> ¹ **nftexplorer.app** this api has been deprecated.\n> \n> ² **gomaestro.org** services require an [api key](https://www.gomaestro.org/pricing).\n> \n> ³ **moralis.io** services require an [api key](https://moralis.io/pricing).\n> \n> ⁴ **opensea.io** some services also require an [api key](https://docs.opensea.io/reference/api-keys). \n\n---\n\n![fetch, the fox](https://i.imgur.com/fm6mqzS.png)\n> fetch, the fox\n\n',
    'author': 'Fede',
    'author_email': 'fede@book.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/book-io/fetchfox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
