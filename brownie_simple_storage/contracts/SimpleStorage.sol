//SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favnum;
    uint256 public num;

    struct People {
        uint256 favnum;
        string name;
    }
    People[] public people;
    mapping(string => uint256) public nameToFavNum;

    function store(uint256 _favnum) public {
        favnum = _favnum;
    }

    function retrieve() public view returns (uint256) {
        return favnum;
    }

    function addPerson(string memory _name, uint256 _favnum) public {
        people.push(People(_favnum, _name));
        nameToFavNum[_name] = _favnum;
    }

    function eight() public pure returns (uint256) {
        return 8;
    }

    function add() public {
        num += eight();
    }

    function viewAdd() public view returns (uint256) {
        return num;
    }
}
