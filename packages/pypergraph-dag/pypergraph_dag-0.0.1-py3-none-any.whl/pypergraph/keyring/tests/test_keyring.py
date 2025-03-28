import pytest

from pypergraph.keyring import KeyringManager, MultiKeyWallet, MultiAccountWallet
from pypergraph.keyring.tests.secret import mnemo
from pypergraph.keystore import KeyStore

# We need to write some more tests

@pytest.fixture
def key_manager():
    return KeyringManager(storage_file_path="key_storage.json")

@pytest.mark.asyncio
async def test_create_or_restore_wallet(key_manager):
    wallet = await key_manager.create_or_restore_vault(password="super_S3cretP_Asswo0rd", seed=mnemo)
    assert wallet.model_dump() == {
        'type': 'MCW',
        'label': 'Wallet #1',
        'secret': 'multiply angle perfect verify behind sibling skirt attract first lift remove fortune',
        'rings': [
            {
                'network': 'Constellation',
                'accounts': [
                    {
                        'bip44_index': 0
                    }
                ]
            },
            {
                'network': 'Ethereum',
                'accounts': [
                    {
                        'tokens': [
                            '0xa393473d64d2F9F026B60b6Df7859A689715d092'
                        ],
                        'bip44_index': 0
                    }
                ]
            }
        ]
    }


@pytest.mark.asyncio
async def test_create_hd_wallet(key_manager):
    key_manager.set_password("super_S3cretP_Asswo0rd")
    wallet = await key_manager.create_multi_chain_hd_wallet(seed=mnemo)
    assert wallet.model_dump() == {
        'type': 'MCW',
        'label': 'Wallet #1',
        'secret': 'multiply angle perfect verify behind sibling skirt attract first lift remove fortune',
        'rings': [
            {
                'network': 'Constellation',
                'accounts': [
                    {
                        'bip44_index': 0
                    }
                ]
            },
            {
                'network': 'Ethereum',
                'accounts': [
                    {
                        'tokens': [
                            '0xa393473d64d2F9F026B60b6Df7859A689715d092'
                        ],
                        'bip44_index': 0
                    }
                ]
            }
        ]
    }


@pytest.mark.asyncio
async def test_create_single_account_wallet(key_manager):
    key_manager.set_password("super_S3cretP_Asswo0rd")
    pk = KeyStore.get_private_key_from_mnemonic(mnemo)
    wallet = await key_manager.create_single_account_wallet(label="New SAW", private_key=pk)
    assert wallet.model_dump() == {
        'type': 'SAW',
        'label': 'New SAW',
        'network': 'Constellation',
        'secret': '18e19114377f0b4ae5b9426105ffa4d18c791f738374b5867ebea836e5722710'
    }


@pytest.mark.asyncio
async def test_create_wallet_ids(key_manager):
    key_manager.set_password("super_S3cretP_Asswo0rd")
    pk = KeyStore.get_private_key_from_mnemonic(mnemo)
    await key_manager.create_single_account_wallet(label="New SAW", private_key=pk)
    await key_manager.create_multi_chain_hd_wallet(seed=mnemo)
    assert [wallet.id for wallet in key_manager.wallets] == ['SAW4', 'MCW5']

@pytest.mark.asyncio
async def test_manager_login(key_manager):
    """Retrieves data from encryted json storage"""
    await key_manager.login("super_S3cretP_Asswo0rd")
    assert [wallet.model_dump() for wallet in key_manager.wallets] == [
        {
            'type': 'SAW',
            'label': 'New SAW',
            'network': 'Constellation',
            'secret': '18e19114377f0b4ae5b9426105ffa4d18c791f738374b5867ebea836e5722710'
        },
        {
            'type': 'MCW',
            'label': 'Wallet #2',
            'secret': 'multiply angle perfect verify behind sibling skirt attract first lift remove fortune',
            'rings': [
                {
                    'network': 'Constellation',
                    'accounts': [{'bip44_index': 0}]},
                {
                    'network': 'Ethereum',
                    'accounts': [
                        {'tokens': [
                            '0xa393473d64d2F9F026B60b6Df7859A689715d092'
                        ],
                            'bip44_index': 0
                        }
                    ]
                }
            ]
        }
    ]


@pytest.mark.asyncio
async def test_create_multi_key_wallet(key_manager):
    """
    Can import pk but not export:
    Imports an account using the given secret and label, creates a keyring and adds it to the keyrings list.
    """
    pk = KeyStore.get_private_key_from_mnemonic(mnemo)
    wallet = MultiKeyWallet()
    wallet.create(network="Constellation", label="New MKW")
    wallet.import_account(private_key=pk, label="Keyring 1")
    wallet.import_account(private_key=pk, label="Keyring 2")
    assert wallet.model_dump() == {
        'type': 'MKW',
        'label': 'New MKW',
        'secret': None,
        'rings': [
            {
                'network': 'Constellation',
                'accounts': [
                    {
                        'private_key': '18e19114377f0b4ae5b9426105ffa4d18c791f738374b5867ebea836e5722710',
                        'label': 'Keyring 1'
                    }
                ]
            },
            {
                'network': 'Constellation',
                'accounts': [
                    {
                        'private_key': '18e19114377f0b4ae5b9426105ffa4d18c791f738374b5867ebea836e5722710',
                        'label': 'Keyring 2'
                    }
                ]
            }
        ]
    }


@pytest.mark.asyncio
async def test_create_multi_account_wallet(key_manager):

    wallet = MultiAccountWallet()
    wallet.create(network="Constellation", label="New MAW", mnemonic=mnemo, num_of_accounts=2)
    model = wallet.model_dump()
    for i, account in enumerate(model["rings"][0][1]):
        model["rings"][0][1][i]["wallet"] = f"TEST_SIGNING_KEY_PLACEHOLDER_{i}"
    model["rings"][1] = ('hd_path', 'TEST_HD_PATH_PLACEHOLDER')
    model["rings"][4] = ('root_key', 'TEST_BIP32_KEY_PLACEHOLDER')
    assert model == {
        'type': 'MAW',
        'label': 'New MAW',
        'secret': 'multiply angle perfect verify behind sibling skirt attract first lift remove fortune',
        'rings': [
            (
                'accounts', [
                    {
                        'tokens': [],
                        'wallet': 'TEST_SIGNING_KEY_PLACEHOLDER_0',
                        'assets': [],
                        'bip44_index': 0,
                        'provider': None,
                        'label': None
                    },
                    {
                        'tokens': [],
                        'wallet': 'TEST_SIGNING_KEY_PLACEHOLDER_1',
                        'assets': [],
                        'bip44_index': 1,
                        'provider': None,
                        'label': None
                    }
                ]
            ),
            ('hd_path', 'TEST_HD_PATH_PLACEHOLDER'),
            ('mnemonic', 'multiply angle perfect verify behind sibling skirt attract first lift remove fortune'),
            ('extended_key', None),
            ('root_key', 'TEST_BIP32_KEY_PLACEHOLDER'),
            ('network', 'Constellation')
        ]
    }
    wallet.create(network="Ethereum", label="New MAW", mnemonic=mnemo, num_of_accounts=1)
    model = wallet.model_dump()
    vk = model["rings"][0][1][0]["wallet"].get_verifying_key().to_string()
    import eth_keys
    address = eth_keys.keys.PublicKey(vk).to_address()
    assert address == '0x8fbc948ba2dd081a51036de02582f5dcb51a310c'
