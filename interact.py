from web3 import Web3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:7545")
FROM_ADDRESS = os.getenv("FROM_ADDRESS", "0x842D8aDd7b1FA25dfB35283f3E488Dc674cD221F")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "0x074448106d099f467b86848c7670db841857451b05f7944704275a87397fc516")

# Contract ABI
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_description",
				"type": "string"
			}
		],
		"name": "addTask",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "completeTask",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "deleteTask",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "TaskAdded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "TaskCompleted",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "TaskDeleted",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "getCompletedCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "getTask",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "description",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "completed",
						"type": "bool"
					},
					{
						"internalType": "uint256",
						"name": "createdAt",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "completedAt",
						"type": "uint256"
					}
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
		"name": "getTaskCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTasks",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "description",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "completed",
						"type": "bool"
					},
					{
						"internalType": "uint256",
						"name": "createdAt",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "completedAt",
						"type": "uint256"
					}
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
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tasks",
		"outputs": [
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "completed",
				"type": "bool"
			},
			{
				"internalType": "uint256",
				"name": "createdAt",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "completedAt",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]


def load_contract_address():
    """Load contract address from file"""
    try:
        if os.path.exists('contract_address.txt'):
            with open('contract_address.txt', 'r') as f:
                return f.read().strip()
        else:
            print(" contract_address.txt not found")
            print("   Please run deploy.py first")
            return None
    except Exception as e:
        print(f" Error loading contract address: {e}")
        return None

def connect_to_ganache():
    """Connect to Ganache"""
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            print("Failed to connect to Ganache")
            return None
        print(" Connected to Ganache - OK")
        return w3
    except Exception as e:
        print(f" Connection error: {e}")
        return None

def get_contract(w3, contract_address):
    """Get contract instance"""
    try:
        checksum_address = w3.to_checksum_address(contract_address)
        contract = w3.eth.contract(address=checksum_address, abi=CONTRACT_ABI)
        print(f" Contract loaded: {checksum_address} - OK")
        return contract
    except Exception as e:
        print(f" Contract error: {e}")
        return None

def send_transaction(w3, function_call, description):
    """Send a transaction that modifies state"""
    try:
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
        
        print(f" {description}")
        print(f"   TX Hash: {tx_hash.hex()}")
        print(f"  Waiting for confirmation...")
        
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        
        print(f"   Success!")
        print(f"   Block: {tx_receipt['blockNumber']}")
        print(f"   Gas Used: {tx_receipt['gasUsed']}")
        
        return tx_receipt
    
    except Exception as e:
        print(f" Transaction error: {e}")
        return None

def add_task(contract, w3, description):
    """Add a new task"""
    try:
        if not description or len(description.strip()) == 0:
            print("Error: Task description cannot be empty")
            return False
        
        if len(description) > 256:
            print("Error: Task description too long (max 256 characters)")
            return False
        
        function_call = contract.functions.addTask(description)
        send_transaction(w3, function_call, f"Adding task: '{description}'")
        return True
    
    except Exception as e:
        print(f"Error adding task: {e}")
        return False

def complete_task(contract, w3, index):
    """Complete a task"""
    try:
        task_count = contract.functions.getTaskCount().call()
        
        if index < 0 or index >= task_count:
            print(f"Error: Invalid task index {index} (total tasks: {task_count})")
            return False
        
        task = contract.functions.getTask(index).call()
        
        if task[1]:  # Check if already completed
            print(f" Error: Task already completed")
            return False
        
        function_call = contract.functions.completeTask(index)
        send_transaction(w3, function_call, f"Completing task {index}")
        return True
    
    except Exception as e:
        print(f"Error completing task: {e}")
        return False

def delete_task(contract, w3, index):
    """Delete a task"""
    try:
        task_count = contract.functions.getTaskCount().call()
        
        if index < 0 or index >= task_count:
            print(f"Error: Invalid task index {index} (total tasks: {task_count})")
            return False
        
        function_call = contract.functions.deleteTask(index)
        send_transaction(w3, function_call, f"Deleting task {index}")
        return True
    
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False

def view_tasks(contract):
    """Display all tasks"""
    try:
        tasks = contract.functions.getTasks().call()
        total = contract.functions.getTaskCount().call()
        completed = contract.functions.getCompletedCount().call()
        
        print("\n" + "="*70)
        print(" TASK LIST")
        print("="*70)
        print(f"Total: {total} | Completed: {completed} | Pending: {total - completed}\n")
        
        if total == 0:
            print("No tasks yet. Add one to get started!")
        else:
            for i, task in enumerate(tasks):
                status = "Done" if task[1] else "Pending"
                created = datetime.fromtimestamp(task[2]).strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"{status} [{i}] {task[0]}")
                print(f"    Created: {created}")
                
                if task[1]:
                    completed_time = datetime.fromtimestamp(task[3]).strftime("%Y-%m-%d %H:%M:%S")
                    print(f"    Completed: {completed_time}")
                
                print()
        
        print("="*70)
        return tasks
    
    except Exception as e:
        print(f" Error viewing tasks: {e}")
        return None

def main():
    """Main interaction loop"""
    print("\n" + "="*70)
    print(" TODO LIST DAPP - INTERACTION")
    print("="*70 + "\n")
    
    # Connect to Ganache
    w3 = connect_to_ganache()
    if w3 is None:
        return
    
    # Load contract
    contract_address = load_contract_address()
    if contract_address is None:
        return
    
    contract = get_contract(w3, contract_address)
    if contract is None:
        return
    
    # Interactive loop
    while True:
        print("\nOptions:")
        print("[1] View all tasks")
        print("[2] Add task")
        print("[3] Complete task")
        print("[4] Delete task")
        print("[5] Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            view_tasks(contract)
        
        elif choice == "2":
            description = input("Enter task description: ").strip()
            add_task(contract, w3, description)
        
        elif choice == "3":
            view_tasks(contract)
            try:
                index = int(input("Enter task index to complete: ").strip())
                complete_task(contract, w3, index)
            except ValueError:
                print(" Error: Invalid index")
        
        elif choice == "4":
            view_tasks(contract)
            try:
                index = int(input("Enter task index to delete: ").strip())
                delete_task(contract, w3, index)
            except ValueError:
                print(" Error: Invalid index")
        
        elif choice == "5":
            print("\n Goodbye!")
            break
        
        else:
            print(" Invalid choice. Please try again.")

if __name__ == "__main__":
    main()