from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrage
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected


def test_updating_storage():
    # Arrage
    account = accounts[0]
    simple_storgae = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    transaction = simple_storgae.store(expected, {"from": account})
    transaction.wait(1)
    # Assert
    assert expected == simple_storgae.retrieve()
