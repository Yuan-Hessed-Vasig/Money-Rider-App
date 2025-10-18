# Money Rider Application - Code Structure & Data Structures Documentation

## Table of Contents

1. [Overview](#overview)
2. [Imports & Dependencies](#imports--dependencies)
3. [Data Structures Implementation](#data-structures-implementation)
4. [Core Classes](#core-classes)
5. [Algorithm Implementations](#algorithm-implementations)
6. [UI Components](#ui-components)
7. [Data Flow](#data-flow)
8. [Performance Analysis](#performance-analysis)

## Overview

The Money Rider application is a comprehensive financial tracking system that demonstrates various data structures and algorithms in a real-world context. The application is built using Python's tkinter for the GUI and implements multiple data structures for efficient data management.

## Imports & Dependencies

```python
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime, timedelta
import calendar
import json
import os
import heapq
from collections import deque, defaultdict
from typing import List, Optional, Dict, Any, Tuple
import math
```

**Data Structure Context:**

- `heapq`: Used for implementing priority queues (heap-based)
- `deque`: Used for efficient queue operations (O(1) append/pop from both ends)
- `defaultdict`: Used for creating hash tables with default values
- `typing`: Provides type hints for better code documentation and IDE support

## Data Structures Implementation

### 1. Transaction Class

```python
class Transaction:
    """Transaction class representing a single financial transaction"""
    def __init__(self, id: str, description: str, amount: float, category: str,
                 transaction_type: str, date: datetime, tags: List[str] = None):
        self.id = id
        self.description = description
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type  # 'income' or 'expense'
        self.date = date
        self.tags = tags or []
        self.created_at = datetime.now()
```

**Data Structure Type:** Object/Entity
**Purpose:** Encapsulates all transaction data with proper typing
**Key Features:**

- Immutable core data (id, amount, date)
- Mutable metadata (tags, created_at)
- Serialization methods for persistence

### 2. Node Class (Linked List Node)

```python
class Node:
    """Node for linked list implementation"""
    def __init__(self, data: Transaction):
        self.data = data
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None
```

**Data Structure Type:** Linked List Node
**Purpose:** Individual elements in doubly linked list
**Key Features:**

- Points to both next and previous nodes
- Stores Transaction object as data
- Enables bidirectional traversal

### 3. Doubly Linked List

```python
class DoublyLinkedList:
    """Doubly Linked List for transaction history with O(1) insertion/deletion"""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0
```

**Data Structure Type:** Doubly Linked List
**Time Complexity:**

- Insertion: O(1)
- Deletion: O(1) if node reference known, O(n) if searching by value
- Search: O(n)
- Access: O(n)

**Key Methods:**

```python
def append(self, transaction: Transaction) -> None:
    """Add transaction to end of list - O(1)"""
    new_node = Node(transaction)
    if not self.head:
        self.head = self.tail = new_node
    else:
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
    self.size += 1
```

**Use Case:** Main storage for all transactions, allows efficient insertion at end

### 4. Stack Implementation

```python
class Stack:
    """Stack implementation for undo/redo functionality"""
    def __init__(self):
        self._items = []

    def push(self, item):
        """Push item to stack - O(1)"""
        self._items.append(item)

    def pop(self):
        """Pop item from stack - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()
```

**Data Structure Type:** Stack (LIFO - Last In, First Out)
**Time Complexity:** O(1) for all operations
**Use Case:** Undo/redo functionality, navigation history
**Implementation:** Uses Python list with append/pop operations

### 5. Queue Implementation

```python
class Queue:
    """Queue implementation for processing transactions"""
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Add item to queue - O(1)"""
        self._items.append(item)

    def dequeue(self):
        """Remove item from queue - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.popleft()
```

**Data Structure Type:** Queue (FIFO - First In, First Out)
**Time Complexity:** O(1) for all operations
**Use Case:** Transaction processing pipeline
**Implementation:** Uses collections.deque for efficient operations

### 6. Priority Queue

```python
class PriorityQueue:
    """Priority Queue for sorting transactions by amount or date"""
    def __init__(self):
        self._heap = []
        self._index = 0

    def push(self, item, priority):
        """Push item with priority - O(log n)"""
        heapq.heappush(self._heap, (priority, self._index, item))
        self._index += 1
```

**Data Structure Type:** Min-Heap (Binary Heap)
**Time Complexity:**

- Insertion: O(log n)
- Extraction: O(log n)
- Peek: O(1)

**Use Case:** Maintaining transactions sorted by amount or date
**Implementation:** Uses Python's heapq module

### 7. Hash Table

```python
class HashTable:
    """Hash Table for fast transaction lookup by category or date"""
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        """Simple hash function"""
        return hash(key) % self.size
```

**Data Structure Type:** Hash Table with Chaining
**Time Complexity:**

- Average: O(1)
- Worst Case: O(n) due to collisions
  **Use Case:** Fast lookup by transaction ID, category indexing
  **Collision Resolution:** Chaining (separate chaining)

### 8. Binary Search Tree

```python
class BinarySearchTree:
    """Binary Search Tree for sorted transaction storage"""
    class TreeNode:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
```

**Data Structure Type:** Binary Search Tree
**Time Complexity:**

- Average: O(log n)
- Worst Case: O(n) for unbalanced trees
  **Use Case:** Date-based queries, sorted data retrieval
  **Implementation:** Recursive insertion and search

## Core Classes

### FinancialDataManager Class

```python
class FinancialDataManager:
    """Main class managing all financial data with various data structures"""
    def __init__(self):
        self.transactions = DoublyLinkedList()        # Main storage
        self.transaction_lookup = HashTable()         # ID -> Transaction
        self.category_index = HashTable()             # Category -> List of IDs
        self.date_index = BinarySearchTree()          # Date -> List of IDs
        self.undo_stack = Stack()                     # Undo operations
        self.redo_stack = Stack()                     # Redo operations
        self.pending_transactions = Queue()           # Processing queue
        self.priority_queue = PriorityQueue()         # Sorted by amount
        self.transaction_counter = 0                  # ID generation
```

**Purpose:** Central coordinator for all data structures
**Design Pattern:** Facade Pattern - provides unified interface
**Key Responsibilities:**

- Transaction CRUD operations
- Data indexing and retrieval
- Undo/redo management
- Data persistence

### Key Methods Analysis:

#### add_transaction() - O(log n)

```python
def add_transaction(self, description: str, amount: float, category: str,
                   transaction_type: str, date: datetime, tags: List[str] = None) -> str:
    transaction_id = f"TXN_{self.transaction_counter:06d}"
    self.transaction_counter += 1

    transaction = Transaction(transaction_id, description, amount, category,
                            transaction_type, date, tags)

    # Add to main list - O(1)
    self.transactions.append(transaction)

    # Update indexes - O(1) average
    self.transaction_lookup.insert(transaction_id, transaction)

    # Category index - O(1) average
    category_key = f"{category}_{transaction_type}"
    existing = self.category_index.get(category_key) or []
    existing.append(transaction_id)
    self.category_index.insert(category_key, existing)

    # Date index - O(log n)
    date_key = date.strftime("%Y-%m-%d")
    existing_dates = self.date_index.search(date_key) or []
    existing_dates.append(transaction_id)
    self.date_index.insert(date_key, existing_dates)

    # Priority queue - O(log n)
    self.priority_queue.push(transaction, -amount)

    return transaction_id
```

**Data Structure Operations:**

1. **DoublyLinkedList.append()** - O(1) - Add to main storage
2. **HashTable.insert()** - O(1) - ID lookup index
3. **HashTable operations** - O(1) - Category indexing
4. **BinarySearchTree.insert()** - O(log n) - Date indexing
5. **PriorityQueue.push()** - O(log n) - Amount-based sorting

#### get_transactions_by_category() - O(1) average

```python
def get_transactions_by_category(self, category: str, transaction_type: str = None) -> List[Transaction]:
    if transaction_type:
        key = f"{category}_{transaction_type}"
        all_ids = self.category_index.get(key) or []
    else:
        # Search both income and expense - O(1) each
        income_key = f"{category}_income"
        expense_key = f"{category}_expense"
        income_ids = self.category_index.get(income_key) or []
        expense_ids = self.category_index.get(expense_key) or []
        all_ids = income_ids + expense_ids

    transactions = []
    for txn_id in all_ids:  # O(k) where k is number of transactions
        txn = self.transaction_lookup.get(txn_id)  # O(1)
        if txn:
            transactions.append(txn)

    return transactions
```

**Data Structure Operations:**

1. **HashTable.get()** - O(1) - Category lookup
2. **HashTable.get()** - O(1) - Transaction lookup by ID
3. **List operations** - O(k) - Building result list

## Algorithm Implementations

### Sorting Algorithms

#### Quick Sort - O(n log n) average, O(n²) worst case

```python
@staticmethod
def quick_sort(transactions: List[Transaction], key_func=lambda x: x.amount, reverse=False) -> List[Transaction]:
    if len(transactions) <= 1:
        return transactions

    pivot = transactions[len(transactions) // 2]
    left = [x for x in transactions if (key_func(x) < key_func(pivot)) != reverse]
    middle = [x for x in transactions if key_func(x) == key_func(pivot)]
    right = [x for x in transactions if (key_func(x) > key_func(pivot)) != reverse]

    return (SortingAlgorithms.quick_sort(left, key_func, reverse) +
            middle +
            SortingAlgorithms.quick_sort(right, key_func, reverse))
```

**Algorithm Type:** Divide and Conquer
**Pivot Selection:** Middle element
**Stability:** Not stable
**Space Complexity:** O(log n) due to recursion

#### Merge Sort - O(n log n) guaranteed

```python
@staticmethod
def merge_sort(transactions: List[Transaction], key_func=lambda x: x.amount, reverse=False) -> List[Transaction]:
    if len(transactions) <= 1:
        return transactions

    mid = len(transactions) // 2
    left = SortingAlgorithms.merge_sort(transactions[:mid], key_func, reverse)
    right = SortingAlgorithms.merge_sort(transactions[mid:], key_func, reverse)

    return SortingAlgorithms._merge(left, right, key_func, reverse)
```

**Algorithm Type:** Divide and Conquer
**Stability:** Stable
**Space Complexity:** O(n) for temporary arrays
**Guaranteed Performance:** Always O(n log n)

#### Heap Sort - O(n log n) guaranteed

```python
@staticmethod
def heap_sort(transactions: List[Transaction], key_func=lambda x: x.amount, reverse=False) -> List[Transaction]:
    if not transactions:
        return []

    # Create heap - O(n log n)
    heap = []
    for txn in transactions:
        priority = key_func(txn) if not reverse else -key_func(txn)
        heapq.heappush(heap, (priority, txn))

    # Extract elements - O(n log n)
    result = []
    while heap:
        _, txn = heapq.heappop(heap)
        result.append(txn)

    return result
```

**Algorithm Type:** Selection Sort using Heap
**Stability:** Not stable
**Space Complexity:** O(n) for heap
**In-place:** No (uses additional heap)

### Search Algorithms

#### Binary Search - O(log n)

```python
@staticmethod
def binary_search(transactions: List[Transaction], target_amount: float,
                 key_func=lambda x: x.amount) -> Optional[Transaction]:
    # First sort the transactions - O(n log n)
    sorted_transactions = SortingAlgorithms.merge_sort(transactions, key_func)

    left, right = 0, len(sorted_transactions) - 1

    while left <= right:  # O(log n)
        mid = (left + right) // 2
        current_amount = key_func(sorted_transactions[mid])

        if current_amount == target_amount:
            return sorted_transactions[mid]
        elif current_amount < target_amount:
            left = mid + 1
        else:
            right = mid - 1

    return None
```

**Algorithm Type:** Divide and Conquer
**Prerequisite:** Sorted array
**Space Complexity:** O(n) for sorting

#### Linear Search - O(n)

```python
@staticmethod
def linear_search(transactions: List[Transaction], predicate) -> List[Transaction]:
    return [txn for txn in transactions if predicate(txn)]
```

**Algorithm Type:** Sequential search
**Use Case:** Unsorted data, complex predicates
**Space Complexity:** O(k) where k is number of matches

## UI Components

### Screen Architecture

#### 1. Splash Screen

```python
def splash_screen():
    # Add to navigation history - Stack operation
    add_to_history('splash_screen')

    splash = tk.Tk()
    width, height = setup_adaptive_window(splash, "Money Rider - Financial Tracker")
```

**Data Structures Used:**

- **Stack (navigation_history)**: Tracks screen navigation
- **Adaptive UI System**: Responsive design based on screen size

#### 2. Calendar Screen

```python
def calendar_screen():
    # Data structure operations
    current_date = datetime.now()
    month_cal = calendar.monthcalendar(current_year, current_month)

    # Binary Search Tree for date queries
    for date_str in sorted(financial_data.keys()):
        if start_date_str <= date_str <= end_date_str:
            data = financial_data[date_str]
```

**Data Structures Used:**

- **Binary Search Tree (date_index)**: Date-based transaction lookup
- **Hash Table (financial_data)**: Date to transaction mapping
- **Calendar Data Structure**: Month grid representation

#### 3. Income/Expense Screens

```python
def income_screen(day, year, month):
    # Current transaction buffers - Arrays
    current_entries = []
    current_expenses = []

    # Undo/redo functionality - Stacks
    undo_stack = []
    redo_stack = []
```

**Data Structures Used:**

- **Arrays (current_entries, current_expenses)**: Temporary transaction storage
- **Stacks (undo_stack, redo_stack)**: Undo/redo operations
- **Doubly Linked List**: Main transaction storage

#### 4. Analytics Screen

```python
def analytics_screen():
    # Data structure statistics
    all_transactions = financial_data_manager.transactions.to_list()
    ds_stats = [
        f"Total Transactions: {len(all_transactions)}",
        f"Linked List Size: {len(financial_data_manager.transactions)}",
        f"Hash Table Entries: {sum(len(bucket) for bucket in financial_data_manager.transaction_lookup.table)}",
        f"Binary Search Tree Nodes: {financial_data_manager.date_index.size}",
        f"Priority Queue Size: {financial_data_manager.priority_queue.size()}",
    ]
```

**Data Structures Used:**

- **All implemented data structures**: For demonstration and analysis
- **Performance metrics**: Real-time complexity analysis

## Data Flow

### 1. Transaction Creation Flow

```
User Input → UI Validation → FinancialDataManager.add_transaction()
    ↓
Transaction Object Creation
    ↓
Multiple Data Structure Updates:
    ├── DoublyLinkedList.append() - O(1)
    ├── HashTable.insert() (ID lookup) - O(1)
    ├── HashTable.insert() (Category index) - O(1)
    ├── BinarySearchTree.insert() (Date index) - O(log n)
    └── PriorityQueue.push() (Amount sorting) - O(log n)
    ↓
Data Persistence (JSON serialization)
```

### 2. Transaction Query Flow

```
Query Request → FinancialDataManager
    ↓
Index Selection:
    ├── By ID → HashTable.get() - O(1)
    ├── By Category → HashTable.get() - O(1)
    ├── By Date Range → BinarySearchTree.search() - O(log n + k)
    └── By Amount → PriorityQueue operations - O(log n)
    ↓
Transaction Retrieval → HashTable.get() for each ID - O(1) each
    ↓
Result Assembly and Return
```

### 3. Undo/Redo Flow

```
User Action → Current State Capture
    ↓
Stack Operations:
    ├── Undo: undo_stack.pop() - O(1)
    └── Redo: redo_stack.push() - O(1)
    ↓
State Restoration
```

## Performance Analysis

### Time Complexity Summary

| Operation         | Data Structure   | Best Case  | Average Case | Worst Case |
| ----------------- | ---------------- | ---------- | ------------ | ---------- |
| Add Transaction   | DoublyLinkedList | O(1)       | O(1)         | O(1)       |
| Lookup by ID      | HashTable        | O(1)       | O(1)         | O(n)       |
| Category Search   | HashTable        | O(1)       | O(1)         | O(n)       |
| Date Range Query  | BinarySearchTree | O(log n)   | O(log n)     | O(n)       |
| Sort Transactions | Various          | O(n log n) | O(n log n)   | O(n²)      |
| Undo/Redo         | Stack            | O(1)       | O(1)         | O(1)       |
| Process Queue     | Queue            | O(1)       | O(1)         | O(1)       |

### Space Complexity Analysis

| Component           | Space Complexity | Justification     |
| ------------------- | ---------------- | ----------------- |
| Transaction Storage | O(n)             | n transactions    |
| Hash Table Indexes  | O(n)             | n transaction IDs |
| Binary Search Tree  | O(n)             | n date entries    |
| Priority Queue      | O(n)             | n transactions    |
| Undo/Redo Stacks    | O(k)             | k operations      |
| UI State            | O(1)             | Constant overhead |

### Memory Usage Patterns

1. **Primary Storage**: DoublyLinkedList - O(n)
2. **Indexing Overhead**: HashTables + BST - O(n)
3. **Temporary Storage**: Stacks, Queues - O(k) where k << n
4. **UI Components**: Constant - O(1)

## Educational Value

### Data Structure Learning Outcomes

1. **Linked Lists**: Understanding node-based data structures
2. **Stacks & Queues**: LIFO vs FIFO operations
3. **Hash Tables**: Fast lookup and collision handling
4. **Trees**: Hierarchical data organization
5. **Heaps**: Priority-based data management

### Algorithm Learning Outcomes

1. **Sorting**: Comparison of different sorting algorithms
2. **Searching**: Binary vs linear search trade-offs
3. **Time Complexity**: Real-world performance analysis
4. **Space Complexity**: Memory usage optimization

### Real-World Application

The Money Rider application demonstrates how theoretical data structures and algorithms are applied in practical software development, showing:

- **System Design**: How multiple data structures work together
- **Performance Optimization**: Choosing the right structure for each use case
- **User Experience**: Balancing functionality with performance
- **Maintainability**: Clean, well-documented code structure

This comprehensive implementation serves as both a functional financial application and an excellent educational resource for understanding data structures and algorithms in practice.
