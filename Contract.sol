// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TodoList {
    struct Task {
        string description;
        bool completed;
    }

    Task[] public tasks;

    // Add a new task
    function addTask(string memory _description) public {
        tasks.push(Task({description: _description, completed: false}));
    }

    // Complete a task by index
    function completeTask(uint256 _index) public {
        require(_index < tasks.length, "Invalid task index");
        tasks[_index].completed = true;
    }

    // Delete a task by index (shifts array to remove)
    function deleteTask(uint256 _index) public {
        require(_index < tasks.length, "Invalid task index");
        for (uint256 i = _index; i < tasks.length - 1; i++) {
            tasks[i] = tasks[i + 1];
        }
        tasks.pop();
    }

    // View all tasks
    function getTasks() public view returns (Task[] memory) {
        return tasks;
    }

    // Get total number of tasks (helpful for viewing)
    function getTaskCount() public view returns (uint256) {
        return tasks.length;
    }
}