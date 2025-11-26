import pytest
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:7545")
FROM_ADDRESS = os.getenv("FROM_ADDRESS", "0x842D8aDd7b1FA25dfB35283f3E488Dc674cD221F")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "0x074448106d099f467b86848c7670db841857451b05f7944704275a87397fc516")
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "string", "name": "_description", "type": "string"}],
        "name": "addTask",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_index", "type": "uint256"}],
        "name": "completeTask",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_index", "type": "uint256"}],
        "name": "deleteTask",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTaskCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTasks",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "description", "type": "string"},
                    {"internalType": "bool", "name": "completed", "type": "bool"},
                    {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
                    {"internalType": "uint256", "name": "completedAt", "type": "uint256"}
                ],
                "internalType": "struct TodoList.Task[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_index", "type": "uint256"}],
        "name": "getTask",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "description", "type": "string"},
                    {"internalType": "bool", "name": "completed", "type": "bool"},
                    {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
                    {"internalType": "uint256", "name": "completedAt", "type": "uint256"}
                ],
                "internalType": "struct TodoList.Task",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getCompletedCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

@pytest.fixture(scope="session")
def w3():
    """Connect to Ganache"""
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    assert w3.is_connected(), "Failed to connect to Ganache"
    return w3

@pytest.fixture(scope="session")
def contract(w3):
    """Load contract instance"""
    if not os.path.exists('contract_address.txt'):
        pytest.skip("Contract not deployed. Run deploy.py first")
    
    with open('contract_address.txt', 'r') as f:
        contract_address = f.read().strip()
    
    contract = w3.eth.contract(
        address=w3.to_checksum_address(contract_address),
        abi=CONTRACT_ABI
    )
    return contract

def send_transaction(w3, function_call):
    """Helper to send transactions"""
    nonce = w3.eth.get_transaction_count(FROM_ADDRESS)
    txn = function_call.build_transaction({
        'from': FROM_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': w3.eth.chain_id
    })
    signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
    return tx_receipt

# ============================================
# TEST CASES
# ============================================

class TestAddTask:
    """Test adding tasks"""
    
    def test_add_single_task(self, w3, contract):
        """Test adding a single task"""
        initial_count = contract.functions.getTaskCount().call()
        
        send_transaction(w3, contract.functions.addTask("Test task 1"))
        
        new_count = contract.functions.getTaskCount().call()
        assert new_count == initial_count + 1, "Task count should increase by 1"
        
        # Verify task content
        tasks = contract.functions.getTasks().call()
        last_task = tasks[-1]
        assert last_task[0] == "Test task 1", "Task description mismatch"
        assert not last_task[1], "New task should not be completed"
        assert last_task[2] > 0, "Created timestamp should be set"

    def test_add_multiple_tasks(self, w3, contract):
        """Test adding multiple tasks"""
        initial_count = contract.functions.getTaskCount().call()
        
        descriptions = ["Task A", "Task B", "Task C"]
        for desc in descriptions:
            send_transaction(w3, contract.functions.addTask(desc))
        
        final_count = contract.functions.getTaskCount().call()
        assert final_count == initial_count + 3, "Should have added 3 tasks"

    def test_add_task_with_empty_description_fails(self, w3, contract):
        """Test that empty description is rejected"""
        with pytest.raises(Exception):
            send_transaction(w3, contract.functions.addTask(""))

class TestCompleteTask:
    """Test completing tasks"""
    
    def test_complete_task(self, w3, contract):
        """Test completing a task"""
        # Add a task
        send_transaction(w3, contract.functions.addTask("Complete me"))
        task_index = contract.functions.getTaskCount().call() - 1
        
        # Complete it
        send_transaction(w3, contract.functions.completeTask(task_index))
        
        # Verify
        task = contract.functions.getTask(task_index).call()
        assert task[1], "Task should be marked as completed"
        assert task[3] > 0, "Completed timestamp should be set"

    def test_cannot_complete_already_completed(self, w3, contract):
        """Test that completing a task twice fails"""
        # Add and complete a task
        send_transaction(w3, contract.functions.addTask("Already done"))
        task_index = contract.functions.getTaskCount().call() - 1
        send_transaction(w3, contract.functions.completeTask(task_index))
        
        # Try to complete again (should fail)
        with pytest.raises(Exception):
            send_transaction(w3, contract.functions.completeTask(task_index))

    def test_complete_nonexistent_task_fails(self, w3, contract):
        """Test that completing an invalid index fails"""
        task_count = contract.functions.getTaskCount().call()
        
        with pytest.raises(Exception):
            send_transaction(w3, contract.functions.completeTask(task_count + 100))

class TestDeleteTask:
    """Test deleting tasks"""
    
    def test_delete_task(self, w3, contract):
        """Test deleting a task"""
        # Add a task
        send_transaction(w3, contract.functions.addTask("Delete me"))
        initial_count = contract.functions.getTaskCount().call()
        delete_index = initial_count - 1
        
        # Delete it
        send_transaction(w3, contract.functions.deleteTask(delete_index))
        
        # Verify count decreased
        final_count = contract.functions.getTaskCount().call()
        assert final_count == initial_count - 1, "Task count should decrease by 1"

    def test_delete_task_shifts_array(self, w3, contract):
        """Test that deleting a task properly shifts the array"""
        # Add three tasks
        send_transaction(w3, contract.functions.addTask("First"))
        send_transaction(w3, contract.functions.addTask("Second"))
        send_transaction(w3, contract.functions.addTask("Third"))
        
        # Delete the first task
        first_index = contract.functions.getTaskCount().call() - 3
        send_transaction(w3, contract.functions.deleteTask(first_index))
        
        # Verify the shift
        tasks = contract.functions.getTasks().call()
        assert tasks[first_index][0] == "Second", "Second task should move to first position"

    def test_delete_nonexistent_task_fails(self, w3, contract):
        """Test that deleting an invalid index fails"""
        task_count = contract.functions.getTaskCount().call()
        
        with pytest.raises(Exception):
            send_transaction(w3, contract.functions.deleteTask(task_count + 50))

class TestViewTasks:
    """Test viewing tasks"""
    
    def test_get_task_count(self, w3, contract):
        """Test getting task count"""
        count = contract.functions.getTaskCount().call()
        assert isinstance(count, int), "Task count should be integer"
        assert count >= 0, "Task count cannot be negative"

    def test_get_all_tasks(self, w3, contract):
        """Test getting all tasks"""
        tasks = contract.functions.getTasks().call()
        assert isinstance(tasks, (list, tuple)), "getTasks should return iterable"
        
        # Verify task structure
        for task in tasks:
            assert len(task) == 4, "Each task should have 4 fields"
            assert isinstance(task[0], str), "Description should be string"
            assert isinstance(task[1], bool), "Completed should be bool"
            assert isinstance(task[2], int), "CreatedAt should be int"
            assert isinstance(task[3], int), "CompletedAt should be int"

    def test_get_completed_count(self, w3, contract):
        """Test getting completed count"""
        completed = contract.functions.getCompletedCount().call()
        total = contract.functions.getTaskCount().call()
        
        assert isinstance(completed, int), "Completed count should be integer"
        assert 0 <= completed <= total, "Completed count should be between 0 and total"

class TestTaskProgress:
    """Test task progress tracking"""
    
    def test_task_progress_statistics(self, w3, contract):
        """Test that we can track task statistics"""
        total_before = contract.functions.getTaskCount().call()
        completed_before = contract.functions.getCompletedCount().call()
        
        # Add a new task
        send_transaction(w3, contract.functions.addTask("Stat test"))
        new_task_index = contract.functions.getTaskCount().call() - 1
        
        # Verify it was added
        assert contract.functions.getTaskCount().call() == total_before + 1
        assert contract.functions.getCompletedCount().call() == completed_before
        
        # Complete it
        send_transaction(w3, contract.functions.completeTask(new_task_index))
        
        # Verify completion count increased
        assert contract.functions.getCompletedCount().call() == completed_before + 1

# ============================================
# RUN TESTS
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])