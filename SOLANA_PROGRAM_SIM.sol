// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SolanaProgramSim {
    address public owner;
    uint256 public programId;
    mapping(address => uint256) public accountBalances;

    event ProgramInitialized(uint256 indexed id);
    event Transfer(address indexed from, address indexed to, uint256 amount);

    constructor() {
        owner = msg.sender;
        programId = uint256(uint160(address(this)));
        emit ProgramInitialized(programId);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function initializeAccount(address account) external onlyOwner {
        require(accountBalances[account] == 0, "Account exists");
        accountBalances[account] = 1000;
    }

    function transferBetweenAccounts(address from, address to, uint256 amount) external {
        require(accountBalances[from] >= amount, "Insufficient balance");
        require(accountBalances[to] > 0, "Target not initialized");

        accountBalances[from] -= amount;
        accountBalances[to] += amount;
        emit Transfer(from, to, amount);
    }

    function getAccountBalance(address account) external view returns (uint256) {
        return accountBalances[account];
    }

    function closeProgram() external onlyOwner {
        selfdestruct(payable(owner));
    }
}
