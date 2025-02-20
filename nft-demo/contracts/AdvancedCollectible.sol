//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {VRFCoordinatorV2Interface} from "@chainlink/contracts/src/v0.8/vrf/interfaces/VRFCoordinatorV2Interface.sol";
import {VRFConsumerBaseV2} from "@chainlink/contracts/src/v0.8/vrf/VRFConsumerBaseV2.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    uint256 public tokenCounter;
    bytes32 internal keyHash;
    uint64 subscriptionId;
    uint32 public callbackGasLimit = 1000000;
    uint16 public requestConfirmations = 3;
    uint32 public numWords = 1;
    VRFCoordinatorV2Interface COORDINATOR;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(uint256 => address) public requestIdToSender;
    event requestedCollectible(uint256 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);
    constructor(
        address _vrfCoordinator,
        uint64 _subscriptionId,
        bytes32 _keyhash
    ) public VRFConsumerBaseV2(_vrfCoordinator) ERC721("Dogie", "Dog") {
        tokenCounter = 0;
        keyHash = _keyhash;
        subscriptionId = _subscriptionId;
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
    }

    function createCollectible() public returns (uint256) {
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyHash,
            subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomNumber
    ) internal override {
        Breed breed = Breed(randomNumber[0] % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address dogOwner = requestIdToSender[requestId];
        _safeMint(dogOwner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not the owner or approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
