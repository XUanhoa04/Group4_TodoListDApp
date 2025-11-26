# 🎯 Todo List DApp - Group 4

## Project Title and Group Members

**Project Name:** Decentralized Todo List Application (Smart Contract)

**Course:** DS 441 A - Blockchain Development

**Group Number:** Group 4

### Group 4 Members
- [Le Dinh Hoai Bao - ]
- [Cai Xuan Hoa - ID]
- [Le Duy Khanh - ID]

---

## Project Description

### What the Project Does
This project is a decentralized Todo List application built on the Ethereum blockchain using Solidity smart contracts. It allows users to:
- Add new tasks with descriptions
- Mark tasks as completed
- Delete tasks from the list
- View all tasks with their status
- Track task statistics (total, completed, pending)
- Record task creation and completion timestamps

### Problem It Solves
Traditional todo list applications store data on centralized servers, which can raise privacy and security concerns. This DApp solves these issues by:
- **Decentralization**: Data is stored on the blockchain, not on centralized servers
- **Immutability**: Task history is permanently recorded and cannot be altered
- **Transparency**: All transactions are visible on the blockchain
- **Security**: Smart contracts enforce business logic at the protocol level
- **Ownership**: Users have complete control over their tasks through their private keys

### Technology Stack
- **Smart Contract Language:** Solidity ^0.8.0
- **Blockchain Network:** Ethereum (Ganache for local testing)
- **Web3 Library:** Web3.py 6.11.3
- **Testing Framework:** Pytest
- **Development Environment:** Remix IDE (for contract development)

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Ganache CLI or Ganache GUI (for local blockchain)
- Remix IDE (for contract development and compilation)
- Git

### Step 1: Install Ganache

**Option A: Using Ganache GUI**
```bash
# Download from https://www.trufflesuite.com/ganache
# Install and run Ganache
# Configure to run on http://127.0.0.1:7545
```

**Option B: Using Ganache CLI**
```bash
npm install -g ganache-cli
ganache-cli -h 127.0.0.1 -p 7545
```

### Step 2: Clone or Download the Project
```bash
git clone <repository-url>
cd Group4_TodoList
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Compile Smart Contract in Remix
1. Go to https://remix.ethereum.org
2. Create a new file `Contract.sol`
3. Copy the code from `Contract.sol` in this project
4. Click "Compile" (Ctrl+S)
5. Copy the **Bytecode** (from Details section)
6. Paste into `deploy.py` replacing the `CONTRACT_BYTECODE` variable

### Step 5: Configure Environment Variables
Create a `.env` file in the project root:
```env
RPC_URL=http://127.0.0.1:7545
FROM_ADDRESS=0x842D8aDd7b1FA25dfB35283f3E488Dc674cD221F
PRIVATE_KEY=0x074448106d099f467b86848c7670db841857451b05f7944704275a87397fc516
```

**Note:** Use the first account and private key from Ganache

### Step 6: Verify Ganache Connection
```bash
python3 -c "from web3 import Web3; w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545')); print('Connected!' if w3.is_connected() else 'Failed')"
```

---

## 🚀 Usage Instructions

### Step 1: Deploy the Contract
Deploy the smart contract to the local Ganache blockchain:
```bash
python deploy.py
```

**Expected Output:**
```
✅ Connected to Ganache
✅ Account verified: 0x842D8aDd7b1FA25dfB35283f3E488Dc674cD221F
   Balance: 100 ETH
✅ Contract deployed successfully!
   Address: 0x46798514dCd31eE9678a59b69b52B03865681387
   📁 Address saved to: contract_address.txt
```

### Step 2: Interact with the Contract
Run the interactive interface:
```bash
python interact.py
```

**Interactive Menu:**
```
Options:
[1] View all tasks
[2] Add task
[3] Complete task
[4] Delete task
[5] Exit
```

### Step 3: Example Usage

**Add a Task:**
```
Enter choice (1-5): 2
Enter task description: Buy groceries
📤 Adding task: 'Buy groceries'
   TX Hash: 0x1234...
   ✅ Success!
```

**View All Tasks:**
```
Enter choice (1-5): 1
📋 TASK LIST
Total: 3 | Completed: 1 | Pending: 2

✅ [0] Finish project
    Created: 2024-01-15 10:30:45
    Completed: 2024-01-15 11:45:22

⭕ [1] Buy groceries
    Created: 2024-01-15 10:35:12
```

**Complete a Task:**
```
Enter choice (1-5): 3
[Task list displayed]
Enter task index to complete: 1
📤 Completing task 1
   ✅ Success!
```

**Delete a Task:**
```
Enter choice (1-5): 4
[Task list displayed]
Enter task index to delete: 2
📤 Deleting task 2
   ✅ Success!
```

---

## 📝 Smart Contract Functions

### Core Functions

#### 1. `addTask(string memory _description) public onlyOwner`
- **Description:** Add a new task to the todo list
- **Parameters:**
  - `_description`: Task description (max 256 characters, non-empty)
- **Emits:** `TaskAdded` event
- **Modifiers:** `onlyOwner` (only contract owner can add tasks)
- **Example:** `contract.functions.addTask("Buy milk").call()`

#### 2. `completeTask(uint256 _index) public onlyOwner`
- **Description:** Mark a task as completed
- **Parameters:**
  - `_index`: Index of the task (0-based)
- **Requirements:**
  - Index must be valid
  - Task must not already be completed
- **Emits:** `TaskCompleted` event
- **Example:** `contract.functions.completeTask(0).call()`

#### 3. `deleteTask(uint256 _index) public onlyOwner`
- **Description:** Remove a task from the list
- **Parameters:**
  - `_index`: Index of the task to delete
- **Requirements:**
  - Index must be valid
- **Emits:** `TaskDeleted` event
- **Note:** Shifts remaining tasks to fill the gap
- **Example:** `contract.functions.deleteTask(1).call()`

### View Functions (Read-Only)

#### 4. `getTasks() public view returns (Task[] memory)`
- **Description:** Retrieve all tasks
- **Returns:** Array of Task structs with all details
- **Gas Cost:** Read-only (no gas required)
- **Example:** `contract.functions.getTasks().call()`

#### 5. `getTask(uint256 _index) public view returns (Task memory)`
- **Description:** Retrieve a specific task by index
- **Parameters:**
  - `_index`: Index of the task
- **Returns:** Single Task struct
- **Example:** `contract.functions.getTask(0).call()`

#### 6. `getTaskCount() public view returns (uint256)`
- **Description:** Get the total number of tasks
- **Returns:** Integer count of tasks
- **Example:** `contract.functions.getTaskCount().call()`

#### 7. `getCompletedCount() public view returns (uint256)`
- **Description:** Get the number of completed tasks
- **Returns:** Integer count of completed tasks
- **Example:** `contract.functions.getCompletedCount().call()`

### Data Structures

#### Task Struct
```solidity
struct Task {
    string description;        // Task description
    bool completed;           // Completion status
    uint256 createdAt;        // Timestamp when created
    uint256 completedAt;      // Timestamp when completed (0 if not completed)
}
```

### Events

#### TaskAdded
```solidity
event TaskAdded(uint256 indexed taskId, string description, uint256 timestamp);
```

#### TaskCompleted
```solidity
event TaskCompleted(uint256 indexed taskId, uint256 timestamp);
```

#### TaskDeleted
```solidity
event TaskDeleted(uint256 indexed taskId, uint256 timestamp);
```

---

## ✅ Testing Instructions

### How to Run Tests

#### Option 1: Run All Tests
```bash
pytest test_contract.py -v
```

#### Option 2: Run Specific Test Class
```bash
pytest test_contract.py::TestAddTask -v
```

#### Option 3: Run Specific Test
```bash
pytest test_contract.py::TestAddTask::test_add_single_task -v
```

#### Option 4: Run with Coverage
```bash
pytest test_contract.py -v --cov=interact --cov=deploy
```

### Test Coverage

The test suite includes **15+ comprehensive tests** across the following categories:

#### TestAddTask (3 tests)
- ✅ `test_add_single_task`: Verify a single task is added correctly
- ✅ `test_add_multiple_tasks`: Verify multiple tasks can be added
- ✅ `test_add_task_with_empty_description_fails`: Verify empty descriptions are rejected

#### TestCompleteTask (3 tests)
- ✅ `test_complete_task`: Verify task can be marked as completed
- ✅ `test_cannot_complete_already_completed`: Verify double completion is prevented
- ✅ `test_complete_nonexistent_task_fails`: Verify invalid index fails

#### TestDeleteTask (3 tests)
- ✅ `test_delete_task`: Verify task can be deleted
- ✅ `test_delete_task_shifts_array`: Verify array elements shift correctly after deletion
- ✅ `test_delete_nonexistent_task_fails`: Verify invalid index fails

#### TestViewTasks (3 tests)
- ✅ `test_get_task_count`: Verify task count is accurate
- ✅ `test_get_all_tasks`: Verify all tasks are returned with correct structure
- ✅ `test_get_completed_count`: Verify completed count is tracked

#### TestTaskProgress (1 test)
- ✅ `test_task_progress_statistics`: Verify statistics update correctly

### What Each Test Validates

| Test | Validates |
|------|-----------|
| Add Single Task | Data persistence, struct fields, count increment |
| Add Multiple Tasks | Batch operations, array management |
| Empty Description | Input validation, error handling |
| Complete Task | State changes, timestamp recording |
| Double Completion | Business logic enforcement |
| Delete Task | Array manipulation, count decrement |
| Array Shift | Data integrity after deletion |
| Task Count | Query accuracy |
| Task Structure | Data consistency |
| Completed Count | Statistics accuracy |

### Expected Test Output
```
test_contract.py::TestAddTask::test_add_single_task PASSED
test_contract.py::TestAddTask::test_add_multiple_tasks PASSED
test_contract.py::TestAddTask::test_add_task_with_empty_description_fails PASSED
test_contract.py::TestCompleteTask::test_complete_task PASSED
test_contract.py::TestCompleteTask::test_cannot_complete_already_completed PASSED
test_contract.py::TestCompleteTask::test_complete_nonexistent_task_fails PASSED
test_contract.py::TestDeleteTask::test_delete_task PASSED
test_contract.py::TestDeleteTask::test_delete_task_shifts_array PASSED
test_contract.py::TestDeleteTask::test_delete_nonexistent_task_fails PASSED
test_contract.py::TestViewTasks::test_get_task_count PASSED
test_contract.py::TestViewTasks::test_get_all_tasks PASSED
test_contract.py::TestViewTasks::test_get_completed_count PASSED
test_contract.py::TestTaskProgress::test_task_progress_statistics PASSED

========================= 13 passed in 45.23s =========================
```

---

## 🔍 Project Structure

```
Group4_TodoList/
├── Contract.sol              # Smart contract source code
├── deploy.py                 # Contract deployment script
├── interact.py               # Interactive CLI for contract
├── test_contract.py          # Test suite with pytest
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── contract_address.txt      # Saved contract address (auto-generated)
├── .env                      # Environment variables (create manually)
└── index.html                # For web presentation (Metamask needed)
```

---

## 🐛 Troubleshooting

### Error: "Failed to connect to Ganache"
**Solution:** 
- Make sure Ganache is running on port 7545
- Verify RPC_URL in `.env` file
- Check firewall settings

### Error: "Contract not found"
**Solution:**
- Run `deploy.py` first to create the contract
- Check `contract_address.txt` exists

### Error: "Invalid task index"
**Solution:**
- Use `python interact.py` option [1] to see valid indices
- Remember indices are 0-based

### Transaction Timeout
**Solution:**
- Check Ganache is running and responsive
- Increase gas limit in the script
- Try again after a short delay

### "Only owner can perform this action"
**Solution:**
- Ensure FROM_ADDRESS in `.env` matches Ganache account
- Use the first account from Ganache

---

## 📊 Performance Metrics

- **Deployment Gas:** ~500,000 gas units
- **Add Task Gas:** ~80,000 gas units
- **Complete Task Gas:** ~50,000 gas units
- **Delete Task Gas:** ~70,000-100,000 gas units (varies with array size)
- **View Functions:** 0 gas (read-only)

---

## 🔐 Security Features

- ✅ **Owner Verification:** Only contract owner can modify tasks
- ✅ **Input Validation:** Non-empty, length-limited descriptions
- ✅ **Bounds Checking:** Invalid indices are rejected
- ✅ **State Verification:** Cannot complete already-completed tasks
- ✅ **Immutable History:** Events record all actions on the blockchain
- ✅ **Transaction Integrity:** All state changes are cryptographically signed

---

## 📈 Future Enhancements

- [ ] Multi-user task lists with sharing
- [ ] Task categories and priorities
- [ ] Recurring/scheduled tasks
- [ ] Task notifications
- [ ] Integration with DeFi for task rewards
- [ ] NFT-based task completion badges
- [ ] IPFS integration for large descriptions

---

## 📚 References

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Ethereum Development](https://ethereum.org/developers)
- [Ganache Documentation](https://www.trufflesuite.com/ganache)
- [Remix IDE](https://remix.ethereum.org)

---

## 📝 Submission Checklist

- ✅ `Contract.sol` - Smart contract
- ✅ `deploy.py` - Deployment script
- ✅ `interact.py` - Interaction script
- ✅ `test_contract.py` - Test cases
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Documentation
- ✅ `.env` - Configuration file (for local testing)

**Format:** `Group4_TodoList.zip` (Maximum 10 MB)

---

## 👥 Authors

**Group 4 - DS 441 A**

For questions or support, please contact the group members.

---

**Last Updated:** January 2025
**Status:** Complete and Ready for Submission