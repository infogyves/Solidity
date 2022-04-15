// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract simpleStorage {
    uint256 simpleUINT256 = 25;
    uint256 simpleUNIT = 8;
    bool simmpleBOOL = false;
    string simpleSTRING = "Infogyves";
    int256 simpleINT = -4;
    address simpleADDRESS = 0x370E34336f210179b511e3C683DE017cE53bdb89;
    bytes32 simpleBYTE = "info chains";

    function simpleStore(uint256 _p1UINT256) public {
        simpleUINT256 = _p1UINT256;
    }

    //Creating a record
    struct simplePerson {
        uint256 simpleID;
        string simpleName;
        address simplePublicKey;
    }

    //Creating a list or array of records of people
    simplePerson[] public simpleList;
    mapping(string => uint256) public personNameToID;

    //People public simpleRecord = People({uint256 _pID, string _pName, address _pAddress});
    simplePerson public simpleRecord =
        simplePerson({
            simpleID: simpleUINT256,
            simpleName: "Infogyves",
            simplePublicKey: 0x370E34336f210179b511e3C683DE017cE53bdb89
        });

    function simpleRetrieve() public view returns (uint256) {
        return simpleUINT256;
    }

    function addPerson(
        uint256 _pPersonID,
        string memory _pPersonName,
        address _pPersonPK
    ) public {
        simpleList.push(
            simplePerson({
                simpleID: _pPersonID,
                simpleName: _pPersonName,
                simplePublicKey: _pPersonPK
            })
        );
        personNameToID[_pPersonName] = _pPersonID;
    }
}
