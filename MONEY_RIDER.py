
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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading

# ==================== CONSTANTS ====================
HASH_TABLE_SIZE = 1000
DEFAULT_ANALYTICS_DAYS = 30
CHART_FIGSIZE_WIDTH = 10
CHART_FIGSIZE_HEIGHT = 6
CHART_FONTSIZE = 14

# Layout Constants
LAYOUT_PADDING = {
    'xs': 2,
    'sm': 5,
    'md': 10,
    'lg': 15,
    'xl': 20,
    'xxl': 30
}

LAYOUT_MARGINS = {
    'xs': 3,
    'sm': 8,
    'md': 12,
    'lg': 18,
    'xl': 25,
    'xxl': 35
}

# ==================== DATA STRUCTURES AND ALGORITHMS ====================

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

    def __str__(self):
        return f"{self.transaction_type.upper()}: {self.description} - ₱{self.amount:,.2f}"

    def __repr__(self):
        return f"Transaction(id={self.id}, desc={self.description}, amount={self.amount})"

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'transaction_type': self.transaction_type,
            'date': self.date.isoformat(),
            'tags': self.tags,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            description=data['description'],
            amount=data['amount'],
            category=data['category'],
            transaction_type=data['transaction_type'],
            date=datetime.fromisoformat(data['date']),
            tags=data.get('tags', [])
        )

class Node:
    """Node for linked list implementation"""
    def __init__(self, data: Transaction):
        self.data = data
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None

class DoublyLinkedList:
    """Doubly Linked List for transaction history with O(1) insertion/deletion"""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0

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

    def prepend(self, transaction: Transaction) -> None:
        """Add transaction to beginning of list - O(1)"""
        new_node = Node(transaction)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def remove_by_id(self, transaction_id: str) -> bool:
        """Remove transaction by ID - O(n)"""
        current = self.head
        while current:
            if current.data.id == transaction_id:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self.size -= 1
                return True
            current = current.next
        return False

    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """Find transaction by ID - O(n)"""
        current = self.head
        while current:
            if current.data.id == transaction_id:
                return current.data
            current = current.next
        return None

    def to_list(self) -> List[Transaction]:
        """Convert to Python list - O(n)"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        return self.size

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

    def peek(self):
        """Peek at top item - O(1)"""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return len(self._items) == 0

    def size(self):
        """Get stack size - O(1)"""
        return len(self._items)

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

    def front(self):
        """Get front item - O(1)"""
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self._items) == 0

    def size(self):
        """Get queue size - O(1)"""
        return len(self._items)

class PriorityQueue:
    """Priority Queue for sorting transactions by amount or date"""
    def __init__(self):
        self._heap = []
        self._index = 0

    def push(self, item, priority):
        """Push item with priority - O(log n)"""
        heapq.heappush(self._heap, (priority, self._index, item))
        self._index += 1

    def pop(self):
        """Pop highest priority item - O(log n)"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self._heap)[2]

    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self._heap) == 0

    def size(self):
        """Get queue size - O(1)"""
        return len(self._heap)

class HashTable:
    """Hash Table for fast transaction lookup by category or date"""
    def __init__(self, size=HASH_TABLE_SIZE):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        """Simple hash function"""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert key-value pair - O(1) average"""
        index = self._hash(key)
        bucket = self.table[index]

        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key):
        """Get value by key - O(1) average"""
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Delete key-value pair - O(1) average"""
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

class BinarySearchTree:
    """Binary Search Tree for sorted transaction storage"""
    class TreeNode:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key, value):
        """Insert key-value pair - O(log n) average"""
        self.root = self._insert_recursive(self.root, key, value)
        self.size += 1

    def _insert_recursive(self, node, key, value):
        if node is None:
            return self.TreeNode(key, value)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            node.value = value  # Update existing key

        return node

    def search(self, key):
        """Search for key - O(log n) average"""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node.value if node else None

        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def inorder_traversal(self):
        """In-order traversal - O(n)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)

class FinancialDataManager:
    """Main class managing all financial data with various data structures"""
    def __init__(self):
        self.transactions = DoublyLinkedList()
        self.transaction_lookup = HashTable()  # ID -> Transaction
        self.category_index = HashTable()  # Category -> List of Transaction IDs
        self.date_index = BinarySearchTree()  # Date -> List of Transaction IDs
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.pending_transactions = Queue()
        self.priority_queue = PriorityQueue()
        self.transaction_counter = 0

    def add_transaction(self, description: str, amount: float, category: str,
                       transaction_type: str, date: datetime, tags: List[str] = None) -> str:
        """Add new transaction - O(log n)"""
        transaction_id = f"TXN_{self.transaction_counter:06d}"
        self.transaction_counter += 1

        transaction = Transaction(transaction_id, description, amount, category,
                                transaction_type, date, tags)

        # Add to main list
        self.transactions.append(transaction)

        # Update indexes
        self.transaction_lookup.insert(transaction_id, transaction)

        # Category index
        category_key = f"{category}_{transaction_type}"
        existing = self.category_index.get(category_key) or []
        existing.append(transaction_id)
        self.category_index.insert(category_key, existing)

        # Date index
        date_key = date.strftime("%Y-%m-%d")
        existing_dates = self.date_index.search(date_key) or []
        existing_dates.append(transaction_id)
        self.date_index.insert(date_key, existing_dates)

        # Add to priority queue for sorting
        self.priority_queue.push(transaction, -amount)  # Negative for max-heap behavior

        return transaction_id

    def get_transactions_by_category(self, category: str, transaction_type: str = None) -> List[Transaction]:
        """Get transactions by category - O(1) average"""
        if transaction_type:
            key = f"{category}_{transaction_type}"
            all_ids = self.category_index.get(key) or []
        else:
            # Search both income and expense
            income_key = f"{category}_income"
            expense_key = f"{category}_expense"
            income_ids = self.category_index.get(income_key) or []
            expense_ids = self.category_index.get(expense_key) or []
            all_ids = income_ids + expense_ids

        transactions = []
        for txn_id in all_ids:
            txn = self.transaction_lookup.get(txn_id)
            if txn:
                transactions.append(txn)

        return transactions

    def get_transactions_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        """Get transactions in date range - O(log n + k) where k is result size"""
        transactions = []
        current_date = start_date

        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            txn_ids = self.date_index.search(date_key) or []

            for txn_id in txn_ids:
                txn = self.transaction_lookup.get(txn_id)
                if txn:
                    transactions.append(txn)

            current_date += timedelta(days=1)

        return transactions

    def get_top_transactions(self, n: int, by_amount: bool = True) -> List[Transaction]:
        """Get top N transactions by amount or date - O(n log n)"""
        if by_amount:
            # Use priority queue
            top_transactions = []
            temp_queue = PriorityQueue()

            # Copy priority queue
            while not self.priority_queue.is_empty():
                txn = self.priority_queue.pop()
                top_transactions.append(txn)
                temp_queue.push(txn, -txn.amount)

            # Restore priority queue
            while not temp_queue.is_empty():
                txn = temp_queue.pop()
                self.priority_queue.push(txn, -txn.amount)

            return top_transactions[:n]
        else:
            # Sort by date
            all_transactions = self.transactions.to_list()
            all_transactions.sort(key=lambda x: x.date, reverse=True)
            return all_transactions[:n]

    def calculate_total_by_category(self, category: str, transaction_type: str = None) -> float:
        """Calculate total amount by category - O(1) average"""
        transactions = self.get_transactions_by_category(category, transaction_type)
        return sum(txn.amount for txn in transactions)

    def calculate_monthly_summary(self, year: int, month: int) -> Dict[str, float]:
        """Calculate monthly financial summary - O(n)"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)

        transactions = self.get_transactions_by_date_range(start_date, end_date)

        summary = {
            'total_income': 0.0,
            'total_expenses': 0.0,
            'net_total': 0.0,
            'transaction_count': len(transactions),
            'categories': defaultdict(float)
        }

        for txn in transactions:
            if txn.transaction_type == 'income':
                summary['total_income'] += txn.amount
            else:
                summary['total_expenses'] += txn.amount

            summary['categories'][txn.category] += txn.amount

        summary['net_total'] = summary['total_income'] - summary['total_expenses']
        return summary

class SortingAlgorithms:
    """Collection of sorting algorithms for financial data"""

    @staticmethod
    def quick_sort(transactions: List[Transaction], key_func=lambda x: x.amount, reverse=False) -> List[Transaction]:
        """Quick sort implementation - O(n log n) average, O(n²) worst case"""
        if len(transactions) <= 1:
            return transactions

        pivot = transactions[len(transactions) // 2]
        left = [x for x in transactions if (key_func(x) < key_func(pivot)) != reverse]
        middle = [x for x in transactions if key_func(x) == key_func(pivot)]
        right = [x for x in transactions if (key_func(x) > key_func(pivot)) != reverse]

        return (SortingAlgorithms.quick_sort(left, key_func, reverse) +
                middle +
                SortingAlgorithms.quick_sort(right, key_func, reverse))

    @staticmethod
    def merge_sort(transactions: List[Transaction], key_func=lambda x: x.amount, reverse=False) -> List[Transaction]:
        """Merge sort implementation - O(n log n) guaranteed"""
        if len(transactions) <= 1:
            return transactions

        mid = len(transactions) // 2
        left = SortingAlgorithms.merge_sort(transactions[:mid], key_func, reverse)
        right = SortingAlgorithms.merge_sort(transactions[mid:], key_func, reverse)

        return SortingAlgorithms._merge(left, right, key_func, reverse)

    @staticmethod
    def _merge(left: List[Transaction], right: List[Transaction],
               key_func, reverse: bool) -> List[Transaction]:
        """Helper method for merge sort"""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if (key_func(left[i]) <= key_func(right[j])) != reverse:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def heap_sort(transactions: List[Transaction], key_func=lambda x: x.amount, reverse=False) -> List[Transaction]:
        """Heap sort implementation - O(n log n) guaranteed"""
        if not transactions:
            return []

        # Create heap
        heap = []
        for txn in transactions:
            priority = key_func(txn) if not reverse else -key_func(txn)
            heapq.heappush(heap, (priority, txn))

        # Extract elements
        result = []
        while heap:
            _, txn = heapq.heappop(heap)
            result.append(txn)

        return result

class SearchAlgorithms:
    """Collection of search algorithms for financial data"""

    @staticmethod
    def binary_search(transactions: List[Transaction], target_amount: float,
                     key_func=lambda x: x.amount) -> Optional[Transaction]:
        """Binary search for exact amount - O(log n)"""
        # First sort the transactions
        sorted_transactions = SortingAlgorithms.merge_sort(transactions, key_func)

        left, right = 0, len(sorted_transactions) - 1

        while left <= right:
            mid = (left + right) // 2
            current_amount = key_func(sorted_transactions[mid])

            if current_amount == target_amount:
                return sorted_transactions[mid]
            elif current_amount < target_amount:
                left = mid + 1
            else:
                right = mid - 1

        return None

    @staticmethod
    def linear_search(transactions: List[Transaction], predicate) -> List[Transaction]:
        """Linear search with custom predicate - O(n)"""
        return [txn for txn in transactions if predicate(txn)]

    @staticmethod
    def find_transactions_in_range(transactions: List[Transaction],
                                 min_amount: float, max_amount: float) -> List[Transaction]:
        """Find transactions in amount range - O(n)"""
        return SearchAlgorithms.linear_search(
            transactions,
            lambda txn: min_amount <= txn.amount <= max_amount
        )

class FinancialAnalytics:
    """Advanced financial analytics using data structures and algorithms"""

    def __init__(self, data_manager: FinancialDataManager):
        self.data_manager = data_manager

    def calculate_trends(self, days: int = DEFAULT_ANALYTICS_DAYS) -> Dict[str, Any]:
        """Calculate spending/income trends over specified days - O(n)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        transactions = self.data_manager.get_transactions_by_date_range(start_date, end_date)

        daily_data = defaultdict(lambda: {'income': 0, 'expenses': 0})

        for txn in transactions:
            date_key = txn.date.strftime("%Y-%m-%d")
            if txn.transaction_type == 'income':
                daily_data[date_key]['income'] += txn.amount
            else:
                daily_data[date_key]['expenses'] += txn.amount

        # Calculate trends
        income_trend = self._calculate_trend(list(daily_data.values()), 'income')
        expense_trend = self._calculate_trend(list(daily_data.values()), 'expenses')

        return {
            'income_trend': income_trend,
            'expense_trend': expense_trend,
            'daily_average_income': sum(d['income'] for d in daily_data.values()) / len(daily_data),
            'daily_average_expenses': sum(d['expenses'] for d in daily_data.values()) / len(daily_data),
            'total_days': len(daily_data)
        }

    def _calculate_trend(self, data: List[Dict], key: str) -> str:
        """Calculate trend direction (increasing/decreasing/stable)"""
        if len(data) < 2:
            return "insufficient_data"

        values = [d[key] for d in data]
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)

        if second_half > first_half * 1.1:
            return "increasing"
        elif second_half < first_half * 0.9:
            return "decreasing"
        else:
            return "stable"

    def find_anomalies(self, threshold: float = 2.0) -> List[Transaction]:
        """Find anomalous transactions using statistical analysis - O(n log n)"""
        all_transactions = self.data_manager.transactions.to_list()

        if len(all_transactions) < 3:
            return []

        # Calculate mean and standard deviation
        amounts = [txn.amount for txn in all_transactions]
        mean = sum(amounts) / len(amounts)
        variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
        std_dev = math.sqrt(variance)

        # Find anomalies (transactions more than threshold standard deviations from mean)
        anomalies = []
        for txn in all_transactions:
            z_score = abs(txn.amount - mean) / std_dev if std_dev > 0 else 0
            if z_score > threshold:
                anomalies.append(txn)

        return anomalies

    def calculate_category_distribution(self) -> Dict[str, Dict[str, float]]:
        """Calculate spending distribution by category - O(n)"""
        all_transactions = self.data_manager.transactions.to_list()

        category_totals = defaultdict(lambda: {'income': 0, 'expenses': 0})

        for txn in all_transactions:
            category_totals[txn.category][txn.transaction_type] += txn.amount

        # Calculate percentages
        total_income = sum(cat['income'] for cat in category_totals.values())
        total_expenses = sum(cat['expenses'] for cat in category_totals.values())

        distribution = {}
        for category, amounts in category_totals.items():
            distribution[category] = {
                'income': amounts['income'],
                'expenses': amounts['expenses'],
                'income_percentage': (amounts['income'] / total_income * 100) if total_income > 0 else 0,
                'expense_percentage': (amounts['expenses'] / total_expenses * 100) if total_expenses > 0 else 0
            }

        return distribution

    def create_income_expense_chart(self, days: int = DEFAULT_ANALYTICS_DAYS) -> Figure:
        """Create income vs expense chart for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Get transactions in date range
        transactions = self.data_manager.get_transactions_by_date_range(start_date, end_date)

        # Group by date
        daily_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        for txn in transactions:
            date_key = txn.date.date()
            if txn.transaction_type == 'income':
                daily_data[date_key]['income'] += txn.amount
            else:
                daily_data[date_key]['expense'] += txn.amount

        # Sort by date
        sorted_dates = sorted(daily_data.keys())
        dates = [datetime.combine(d, datetime.min.time()) for d in sorted_dates]
        income_amounts = [daily_data[d]['income'] for d in sorted_dates]
        expense_amounts = [daily_data[d]['expense'] for d in sorted_dates]

        # Create figure
        fig = Figure(figsize=(CHART_FIGSIZE_WIDTH, CHART_FIGSIZE_HEIGHT), facecolor=MODERN_COLORS['background'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(MODERN_COLORS['card'])

        # Plot data
        ax.plot(dates, income_amounts, label='Income', color=MODERN_COLORS['success'], linewidth=2, marker='o')
        ax.plot(dates, expense_amounts, label='Expenses', color=MODERN_COLORS['danger'], linewidth=2, marker='s')

        # Formatting
        ax.set_title(f'Income vs Expenses - Last {days} Days',
                    color=MODERN_COLORS['text_primary'], fontsize=CHART_FONTSIZE, fontweight='bold')
        ax.set_xlabel('Date', color=MODERN_COLORS['text_primary'])
        ax.set_ylabel('Amount (₱)', color=MODERN_COLORS['text_primary'])
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        # Color formatting
        ax.tick_params(colors=MODERN_COLORS['text_primary'])
        ax.spines['bottom'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['top'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['right'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['left'].set_color(MODERN_COLORS['text_secondary'])

        fig.tight_layout()
        return fig

    def create_category_pie_chart(self) -> Figure:
        """Create pie chart for category distribution"""
        distribution = self.calculate_category_distribution()

        # Prepare data
        categories = []
        income_amounts = []
        expense_amounts = []

        for category, data in distribution.items():
            if data['income'] > 0 or data['expenses'] > 0:
                categories.append(category)
                income_amounts.append(data['income'])
                expense_amounts.append(data['expenses'])

        # Create figure with subplots
        fig = Figure(figsize=(12, 6), facecolor=MODERN_COLORS['background'])

        # Income pie chart
        ax1 = fig.add_subplot(121)
        ax1.set_facecolor(MODERN_COLORS['card'])
        if any(income_amounts):
            ax1.pie(income_amounts, labels=categories, autopct='%1.1f%%',
                   colors=plt.cm.Set3(np.linspace(0, 1, len(categories))))
            ax1.set_title('Income by Category', color=MODERN_COLORS['text_primary'], fontweight='bold')

        # Expense pie chart
        ax2 = fig.add_subplot(122)
        ax2.set_facecolor(MODERN_COLORS['card'])
        if any(expense_amounts):
            ax2.pie(expense_amounts, labels=categories, autopct='%1.1f%%',
                   colors=plt.cm.Set3(np.linspace(0, 1, len(categories))))
            ax2.set_title('Expenses by Category', color=MODERN_COLORS['text_primary'], fontweight='bold')

        # Color formatting
        for ax in [ax1, ax2]:
            ax.tick_params(colors=MODERN_COLORS['text_primary'])

        fig.tight_layout()
        return fig

    def create_monthly_trend_chart(self, months: int = 6) -> Figure:
        """Create monthly trend chart"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        # Get transactions
        transactions = self.data_manager.get_transactions_by_date_range(start_date, end_date)

        # Group by month
        monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0, 'net': 0})
        for txn in transactions:
            month_key = txn.date.replace(day=1)
            if txn.transaction_type == 'income':
                monthly_data[month_key]['income'] += txn.amount
            else:
                monthly_data[month_key]['expense'] += txn.amount

        # Calculate net
        for month in monthly_data:
            monthly_data[month]['net'] = monthly_data[month]['income'] - monthly_data[month]['expense']

        # Sort by month
        sorted_months = sorted(monthly_data.keys())
        months_list = [m for m in sorted_months]
        income_amounts = [monthly_data[m]['income'] for m in sorted_months]
        expense_amounts = [monthly_data[m]['expense'] for m in sorted_months]
        net_amounts = [monthly_data[m]['net'] for m in sorted_months]

        # Create figure
        fig = Figure(figsize=(12, 8), facecolor=MODERN_COLORS['background'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(MODERN_COLORS['card'])

        # Create bar chart
        x = np.arange(len(months_list))
        width = 0.25

        ax.bar(x - width, income_amounts, width, label='Income', color=MODERN_COLORS['success'], alpha=0.8)
        ax.bar(x, expense_amounts, width, label='Expenses', color=MODERN_COLORS['danger'], alpha=0.8)
        ax.bar(x + width, net_amounts, width, label='Net', color=MODERN_COLORS['primary'], alpha=0.8)

        # Formatting
        ax.set_title(f'Monthly Financial Trends - Last {months} Months',
                    color=MODERN_COLORS['text_primary'], fontsize=CHART_FONTSIZE, fontweight='bold')
        ax.set_xlabel('Month', color=MODERN_COLORS['text_primary'])
        ax.set_ylabel('Amount (₱)', color=MODERN_COLORS['text_primary'])
        ax.set_xticks(x)
        ax.set_xticklabels([m.strftime('%b %Y') for m in months_list], rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Color formatting
        ax.tick_params(colors=MODERN_COLORS['text_primary'])
        ax.spines['bottom'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['top'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['right'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['left'].set_color(MODERN_COLORS['text_secondary'])

        fig.tight_layout()
        return fig

    def create_spending_analysis_chart(self) -> Figure:
        """Create spending analysis with top categories"""
        distribution = self.calculate_category_distribution()

        # Get top spending categories
        category_totals = []
        for category, data in distribution.items():
            total = data['income'] + data['expenses']
            if total > 0:
                category_totals.append((category, total, data['income'], data['expenses']))

        # Sort by total amount
        category_totals.sort(key=lambda x: x[1], reverse=True)
        top_categories = category_totals[:8]  # Top 8 categories

        if not top_categories:
            # Create empty chart
            fig = Figure(figsize=(CHART_FIGSIZE_WIDTH, CHART_FIGSIZE_HEIGHT), facecolor=MODERN_COLORS['background'])
            ax = fig.add_subplot(111)
            ax.set_facecolor(MODERN_COLORS['card'])
            ax.text(0.5, 0.5, 'No spending data available',
                   ha='center', va='center', transform=ax.transAxes,
                   color=MODERN_COLORS['text_primary'], fontsize=16)
            ax.set_title('Spending Analysis', color=MODERN_COLORS['text_primary'], fontweight='bold')
            return fig

        categories = [cat[0] for cat in top_categories]
        income_amounts = [cat[2] for cat in top_categories]
        expense_amounts = [cat[3] for cat in top_categories]

        # Create figure
        fig = Figure(figsize=(12, 8), facecolor=MODERN_COLORS['background'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(MODERN_COLORS['card'])

        # Create horizontal bar chart
        y_pos = np.arange(len(categories))

        ax.barh(y_pos, income_amounts, label='Income', color=MODERN_COLORS['success'], alpha=0.8)
        ax.barh(y_pos, [-exp for exp in expense_amounts], label='Expenses', color=MODERN_COLORS['danger'], alpha=0.8)

        # Formatting
        ax.set_title('Top Categories - Income vs Expenses',
                    color=MODERN_COLORS['text_primary'], fontsize=CHART_FONTSIZE, fontweight='bold')
        ax.set_xlabel('Amount (₱)', color=MODERN_COLORS['text_primary'])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axvline(x=0, color=MODERN_COLORS['text_secondary'], linewidth=0.8)

        # Color formatting
        ax.tick_params(colors=MODERN_COLORS['text_primary'])
        ax.spines['bottom'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['top'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['right'].set_color(MODERN_COLORS['text_secondary'])
        ax.spines['left'].set_color(MODERN_COLORS['text_secondary'])

        fig.tight_layout()
        return fig

# ==================== END DATA STRUCTURES AND ALGORITHMS ====================

# Theme Configuration
THEMES = {
    'forest': {
        'name': 'Lush Forest',
    'primary': '#68BA7F',      # Medium Sage Green - Primary buttons and accents
    'primary_dark': '#2E6F40', # Dark Forest Green - Hover states
    'secondary': '#68BA7F',    # Medium Sage Green - Secondary elements
    'success': '#68BA7F',      # Medium Sage Green - Success states
    'danger': '#EF4444',       # Red - Keep for danger states
    'warning': '#F59E0B',      # Orange - Keep for warnings
    'dark': '#253D2C',         # Very Dark Green - Primary text
    'darker': '#1A2B1F',       # Even darker green - Darkest elements
    'light': '#CFFFDC',        # Light Mint Green - Background
    'white': '#F8F9FA',        # Soft off-white - Cards and highlights
    'border': '#68BA7F',       # Medium Sage Green - Borders
    'surface': '#253D2C',      # Very Dark Green - Surface elements
    'text_primary': '#FFFFFF', # White - Primary text on dark backgrounds
    'text_secondary': '#CFFFDC', # Light Mint - Secondary text
    'background': '#253D2C',   # Very Dark Green - Main background
    'card': '#2E6F40',         # Dark Forest Green - Card backgrounds
    'input_bg': '#2E6F40',     # Dark Forest Green - Input backgrounds
    'input_border': '#68BA7F', # Medium Sage Green - Input borders
    'accent': '#CFFFDC'        # Light Mint - Accent elements
    },
    'ocean': {
        'name': 'Ocean Blue',
        'primary': '#3B82F6',      # Blue - Primary buttons and accents
        'primary_dark': '#1E40AF', # Dark Blue - Hover states
        'secondary': '#3B82F6',    # Blue - Secondary elements
        'success': '#10B981',      # Emerald - Success states
        'danger': '#EF4444',       # Red - Danger states
        'warning': '#F59E0B',      # Orange - Warnings
        'dark': '#1E293B',         # Dark Slate - Primary text
        'darker': '#0F172A',       # Darker Slate - Darkest elements
        'light': '#E0F2FE',        # Light Blue - Background
        'white': '#F8F9FA',        # Soft off-white - Cards and highlights
        'border': '#3B82F6',       # Blue - Borders
        'surface': '#1E293B',      # Dark Slate - Surface elements
        'text_primary': '#FFFFFF', # White - Primary text on dark backgrounds
        'text_secondary': '#E0F2FE', # Light Blue - Secondary text
        'background': '#1E293B',   # Dark Slate - Main background
        'card': '#334155',         # Slate - Card backgrounds
        'input_bg': '#334155',     # Slate - Input backgrounds
        'input_border': '#3B82F6', # Blue - Input borders
        'accent': '#E0F2FE'        # Light Blue - Accent elements
    },
    'sunset': {
        'name': 'Sunset Orange',
        'primary': '#F97316',      # Orange - Primary buttons and accents
        'primary_dark': '#C2410C', # Dark Orange - Hover states
        'secondary': '#F97316',    # Orange - Secondary elements
        'success': '#22C55E',      # Green - Success states
        'danger': '#EF4444',       # Red - Danger states
        'warning': '#F59E0B',      # Orange - Warnings
        'dark': '#2D1B69',         # Dark Purple - Primary text
        'darker': '#1A0B2E',       # Darker Purple - Darkest elements
        'light': '#FED7AA',        # Light Orange - Background
        'white': '#F8F9FA',        # Soft off-white - Cards and highlights
        'border': '#F97316',       # Orange - Borders
        'surface': '#2D1B69',      # Dark Purple - Surface elements
        'text_primary': '#FFFFFF', # White - Primary text on dark backgrounds
        'text_secondary': '#FED7AA', # Light Orange - Secondary text
        'background': '#2D1B69',   # Dark Purple - Main background
        'card': '#7C3AED',         # Purple - Card backgrounds
        'input_bg': '#7C3AED',     # Purple - Input backgrounds
        'input_border': '#F97316', # Orange - Input borders
        'accent': '#FED7AA'        # Light Orange - Accent elements
    },
    'midnight': {
        'name': 'Midnight Dark',
        'primary': '#8B5CF6',      # Purple - Primary buttons and accents
        'primary_dark': '#6D28D9', # Dark Purple - Hover states
        'secondary': '#8B5CF6',    # Purple - Secondary elements
        'success': '#10B981',      # Emerald - Success states
        'danger': '#EF4444',       # Red - Danger states
        'warning': '#F59E0B',      # Orange - Warnings
        'dark': '#111827',         # Dark Gray - Primary text
        'darker': '#000000',       # Black - Darkest elements
        'light': '#F3F4F6',        # Light Gray - Background
        'white': '#F8F9FA',        # Soft off-white - Cards and highlights
        'border': '#8B5CF6',       # Purple - Borders
        'surface': '#111827',      # Dark Gray - Surface elements
        'text_primary': '#FFFFFF', # White - Primary text on dark backgrounds
        'text_secondary': '#F3F4F6', # Light Gray - Secondary text
        'background': '#111827',   # Dark Gray - Main background
        'card': '#1F2937',         # Darker Gray - Card backgrounds
        'input_bg': '#1F2937',     # Darker Gray - Input backgrounds
        'input_border': '#8B5CF6', # Purple - Input borders
        'accent': '#F3F4F6'        # Light Gray - Accent elements
    }
}

# Current theme (default to forest)
CURRENT_THEME = 'forest'
MODERN_COLORS = THEMES[CURRENT_THEME]

# Theme management functions
def change_theme(theme_name):
    """Change the application theme"""
    global CURRENT_THEME, MODERN_COLORS
    if theme_name in THEMES:
        CURRENT_THEME = theme_name
        MODERN_COLORS = THEMES[theme_name]
        return True
    return False

def get_current_theme():
    """Get the current theme name"""
    return CURRENT_THEME

def get_available_themes():
    """Get list of available themes"""
    return list(THEMES.keys())

def save_theme_preference(theme_name):
    """Save theme preference to file"""
    try:
        with open("theme_preference.json", "w") as f:
            json.dump({"theme": theme_name}, f)
    except Exception as e:
        print(f"Error saving theme preference: {e}")

def load_theme_preference():
    """Load theme preference from file"""
    global CURRENT_THEME, MODERN_COLORS
    try:
        if os.path.exists("theme_preference.json"):
            with open("theme_preference.json", "r") as f:
                data = json.load(f)
                theme_name = data.get("theme", "forest")
                if theme_name in THEMES:
                    CURRENT_THEME = theme_name
                    MODERN_COLORS = THEMES[theme_name]
    except Exception as e:
        print(f"Error loading theme preference: {e}")
        # Default to forest theme
        CURRENT_THEME = 'forest'
        MODERN_COLORS = THEMES[CURRENT_THEME]

# ==================== SMOOTH TRANSITIONS ====================

def smooth_color_transition(widget, start_color, end_color, duration=200, steps=20):
    """Create smooth color transition for widgets"""
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def interpolate_color(start_rgb, end_rgb, factor):
        return tuple(int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * factor) for i in range(3))

    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    def animate_step(step):
        if step <= steps:
            factor = step / steps
            current_rgb = interpolate_color(start_rgb, end_rgb, factor)
            current_color = rgb_to_hex(current_rgb)

            try:
                widget.config(bg=current_color)
                widget.after(duration // steps, lambda: animate_step(step + 1))
            except tk.TclError:
                pass  # Widget might be destroyed

    animate_step(0)

def smooth_scale_transition(widget, start_scale=1.0, end_scale=1.05, duration=150, steps=15):
    """Create smooth scale transition for widgets"""
    def animate_scale(step):
        if step <= steps:
            factor = step / steps
            current_scale = start_scale + (end_scale - start_scale) * factor

            try:
                # Apply scale by adjusting font size
                if hasattr(widget, 'cget') and 'font' in widget.config():
                    current_font = widget.cget('font')
                    if isinstance(current_font, tuple):
                        font_family, font_size = current_font[0], int(current_font[1])
                        new_size = int(font_size * current_scale)
                        widget.config(font=(font_family, new_size))

                widget.after(duration // steps, lambda: animate_scale(step + 1))
            except tk.TclError:
                pass  # Widget might be destroyed

    animate_scale(0)

def add_smooth_hover_effect(widget, original_bg, hover_bg, scale_effect=True):
    """Add smooth hover effects to widgets"""
    def on_enter(e):
        smooth_color_transition(widget, original_bg, hover_bg, duration=150)
        if scale_effect:
            smooth_scale_transition(widget, 1.0, 1.02, duration=100)

    def on_leave(e):
        smooth_color_transition(widget, hover_bg, original_bg, duration=150)
        if scale_effect:
            smooth_scale_transition(widget, 1.02, 1.0, duration=100)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def add_smooth_click_effect(widget, click_bg, original_bg):
    """Add smooth click effects to widgets"""
    def on_click(e):
        smooth_color_transition(widget, original_bg, click_bg, duration=100)
        widget.after(100, lambda: smooth_color_transition(widget, click_bg, original_bg, duration=100))

    widget.bind("<Button-1>", on_click)

def smooth_tab_transition(notebook, from_tab, to_tab, duration=300):
    """Create smooth transition between tabs"""
    def animate_tab_switch(step):
        if step <= 10:
            try:
                # Simulate smooth transition by gradually changing opacity
                notebook.after(duration // 10, lambda: animate_tab_switch(step + 1))
            except tk.TclError:
                pass

    animate_tab_switch(0)

def smooth_listbox_selection(listbox, duration=100):
    """Add smooth selection effect to listbox"""
    def on_select(e):
        try:
            selection = listbox.curselection()
            if selection:
                # Add a subtle highlight effect
                smooth_color_transition(listbox, MODERN_COLORS['white'], MODERN_COLORS['primary_light'], duration=50)
                listbox.after(200, lambda: smooth_color_transition(
                    listbox, MODERN_COLORS['primary_light'], 
                    MODERN_COLORS['white'], duration=50))
        except tk.TclError:
            pass

    listbox.bind("<<ListboxSelect>>", on_select)

adaptive_fonts = {
    'title': ('Segoe UI', 28, 'bold'),
    'heading': ('Segoe UI', 20, 'bold'),
    'subheading': ('Segoe UI', 16, 'bold'),
    'body': ('Segoe UI', 12),
    'small': ('Segoe UI', 10)
}

# Adaptive Resolution System
def detect_device_type():
    """Detect if running on mobile device vs PC based on screen size and DPI"""
    root = tk.Tk()
    root.withdraw()  # Hide the window

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dpi = root.winfo_fpixels('1i')  # Get DPI

    root.destroy()

    # Mobile detection criteria:
    # 1. Screen width < 768px (common mobile breakpoint)
    # 2. High DPI (> 120) often indicates mobile/tablet
    # 3. Aspect ratio close to mobile (height > width by significant margin)

    is_mobile = (
        screen_width < 768 or  # Small screen width
        dpi > 120 or  # High DPI
        (screen_height > screen_width * 1.5)  # Mobile-like aspect ratio
    )

    return is_mobile, screen_width, screen_height, dpi

def get_adaptive_dimensions():
    """Get adaptive window dimensions based on device type"""
    is_mobile, screen_width, screen_height, dpi = detect_device_type()

    if is_mobile:
        # Mobile adaptive sizing
        # Use percentage of screen size with reasonable limits
        width = max(320, min(screen_width * 0.9, 450))  # 90% of screen, min 320px, max 450px
        height = max(600, min(screen_height * 0.85, 900))  # 85% of screen, min 600px, max 900px

        # Adjust for very small screens
        if screen_width < 400:
            width = max(300, screen_width - 20)  # Leave small margin
            height = max(500, screen_height - 50)  # Leave small margin
    else:
        # PC - keep original dimensions
        width = 450
        height = 800

    return int(width), int(height)

def get_adaptive_fonts():
    """Get adaptive font sizes based on device type"""
    is_mobile, screen_width, screen_height, dpi = detect_device_type()

    if is_mobile:
        # Scale fonts based on screen size
        scale_factor = min(screen_width / 450, screen_height / 800)
        scale_factor = max(0.8, min(1.3, scale_factor))  # Limit scaling between 0.8x and 1.3x

        return {
            'title': ('Segoe UI', int(28 * scale_factor), 'bold'),
            'heading': ('Segoe UI', int(20 * scale_factor), 'bold'),
            'subheading': ('Segoe UI', int(16 * scale_factor), 'bold'),
            'body': ('Segoe UI', int(12 * scale_factor)),
            'small': ('Segoe UI', int(10 * scale_factor))
        }
    else:
        # PC - keep original fonts
        return adaptive_fonts

def get_adaptive_padding():
    """Get adaptive padding based on device type"""
    is_mobile, screen_width, screen_height, dpi = detect_device_type()

    if is_mobile:
        # Scale padding based on screen size
        scale_factor = min(screen_width / 450, screen_height / 800)
        scale_factor = max(0.7, min(1.2, scale_factor))

        return {
            'small': int(5 * scale_factor),
            'medium': int(10 * scale_factor),
            'large': int(20 * scale_factor),
            'xlarge': int(30 * scale_factor)
        }
    else:
        # PC - keep original padding
        return {
            'small': 5,
            'medium': 10,
            'large': 20,
            'xlarge': 30
        }

def setup_adaptive_window(window, title):
    """Setup window with adaptive dimensions and positioning"""
    width, height = get_adaptive_dimensions()

    window.title(title)
    window.geometry(f"{width}x{height}")
    window.configure(bg=MODERN_COLORS['background'])
    window.resizable(False, False)

    # Center the window
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

    return width, height

def get_standard_padding():
    """Get standardized padding values based on device type"""
    is_mobile, screen_width, screen_height, dpi = detect_device_type()
    
    if is_mobile:
        scale_factor = min(screen_width / 450, screen_height / 800)
        scale_factor = max(0.7, min(1.2, scale_factor))
        
        return {
            'container': int(LAYOUT_MARGINS['lg'] * scale_factor),
            'section': int(LAYOUT_PADDING['lg'] * scale_factor),
            'element': int(LAYOUT_PADDING['md'] * scale_factor),
            'small': int(LAYOUT_PADDING['sm'] * scale_factor),
            'large': int(LAYOUT_PADDING['xl'] * scale_factor),
            'xxl': int(LAYOUT_PADDING['xxl'] * scale_factor)
        }
    else:
        return {
            'container': LAYOUT_MARGINS['lg'],
            'section': LAYOUT_PADDING['lg'],
            'element': LAYOUT_PADDING['md'],
            'small': LAYOUT_PADDING['sm'],
            'large': LAYOUT_PADDING['xl'],
            'xxl': LAYOUT_PADDING['xxl']
        }

def create_standard_container(parent, bg=None):
    """Create a standardized container with consistent padding"""
    if bg is None:
        bg = MODERN_COLORS['background']
    
    padding = get_standard_padding()
    container = create_modern_frame(parent, bg)
    container.pack(fill=tk.BOTH, expand=True, 
                   padx=padding['container'], pady=padding['container'])
    return container

def create_standard_section(parent, bg=None):
    """Create a standardized section with consistent spacing"""
    if bg is None:
        bg = MODERN_COLORS['card']
    
    padding = get_standard_padding()
    section = create_modern_frame(parent, bg)
    section.pack(fill=tk.X, padx=padding['section'], pady=padding['section'])
    return section

def create_button_group(parent, buttons, orientation='vertical', spacing='element'):
    """Create a standardized button group with consistent spacing and alignment"""
    padding = get_standard_padding()
    
    if orientation == 'vertical':
        for i, button in enumerate(buttons):
            if i > 0:
                button.pack(pady=padding[spacing])
            else:
                button.pack()
    else:  # horizontal
        for i, button in enumerate(buttons):
            if i > 0:
                button.pack(side=tk.LEFT, padx=padding[spacing])
            else:
                button.pack(side=tk.LEFT)

def create_centered_container(parent, bg=None):
    """Create a centered container for better alignment"""
    if bg is None:
        bg = MODERN_COLORS['background']
    
    container = create_modern_frame(parent, bg)
    container.pack(expand=True, fill=tk.BOTH)
    return container

def create_modern_button(parent, text, command=None, style='primary', width=None, height=None):
    """Create a mobile-friendly styled button with smooth transitions"""
    if style == 'primary':
        bg = MODERN_COLORS['primary']
        hover_bg = MODERN_COLORS['primary_dark']
        click_bg = '#1E40AF'  # Darker blue for click
        fg = MODERN_COLORS['white']
    elif style == 'secondary':
        bg = MODERN_COLORS['secondary']
        hover_bg = '#6D28D9'
        click_bg = '#5B21B6'
        fg = MODERN_COLORS['white']
    elif style == 'success':
        bg = MODERN_COLORS['success']
        hover_bg = '#059669'
        click_bg = '#047857'
        fg = MODERN_COLORS['white']
    elif style == 'danger':
        bg = MODERN_COLORS['danger']
        hover_bg = '#DC2626'
        click_bg = '#B91C1C'
        fg = MODERN_COLORS['white']
    elif style == 'warning':
        bg = MODERN_COLORS['warning']
        hover_bg = '#D97706'
        click_bg = '#B45309'
        fg = MODERN_COLORS['white']
    else:  # default
        bg = MODERN_COLORS['dark']
        hover_bg = '#374151'
        click_bg = '#1F2937'
        fg = MODERN_COLORS['white']

    # Get adaptive fonts and standardized padding
    adaptive_fonts = get_adaptive_fonts()
    padding = get_standard_padding()

    # Mobile-friendly button sizing with adaptive scaling
    button_height = 1 if height is None else height
    button_width = 12 if width is None else width

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=adaptive_fonts['subheading'],
        relief='flat',
        bd=0,
        cursor='hand2',
        width=button_width,
        height=button_height,
        padx=padding['element'],
        pady=padding['small'],
        activebackground=hover_bg,
        activeforeground=fg
    )

    # Add smooth transitions
    add_smooth_hover_effect(button, bg, hover_bg, scale_effect=True)
    add_smooth_click_effect(button, click_bg, bg)

    return button

def create_modern_entry(parent, placeholder="", show=None, width=None):
    """Create a mobile-friendly styled entry field with smooth transitions"""
    # Get adaptive fonts
    adaptive_fonts = get_adaptive_fonts()

    # Set default width if not provided
    if width is None:
        width = 20  # Reduced default width for better fit

    entry = tk.Entry(
        parent,
        font=adaptive_fonts['subheading'],  # Use adaptive font
        relief='flat',
        bd=2,
        highlightthickness=3,
        highlightcolor=MODERN_COLORS['primary'],
        highlightbackground=MODERN_COLORS['input_border'],
        bg=MODERN_COLORS['input_bg'],
        fg=MODERN_COLORS['text_primary'],
        insertbackground=MODERN_COLORS['primary'],
        show=show,
        width=width
    )

    # Add smooth focus transitions
    def on_focus_in(e):
        smooth_color_transition(entry, MODERN_COLORS['input_bg'], MODERN_COLORS['primary_light'], duration=200)
        entry.config(highlightthickness=4)

    def on_focus_out(e):
        smooth_color_transition(entry, MODERN_COLORS['primary_light'], MODERN_COLORS['input_bg'], duration=200)
        entry.config(highlightthickness=3)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry

def create_modern_frame(parent, bg=None):
    """Create a modern styled frame"""
    if bg is None:
        bg = MODERN_COLORS['light']

    frame = tk.Frame(
        parent,
        bg=bg,
        relief='flat',
        bd=0
    )
    return frame

def create_scrollable_frame(parent, bg=None, hide_scrollbar=True):
    """Create a scrollable frame with modern styling and optional hidden scrollbar"""
    if bg is None:
        bg = MODERN_COLORS['background']

    # Create main frame
    main_frame = tk.Frame(parent, bg=bg)

    # Create canvas for scrolling
    canvas = tk.Canvas(main_frame, bg=bg, highlightthickness=0,
                      relief='flat', bd=0)

    # Create scrollbar (hidden if hide_scrollbar is True)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview,
                           bg=MODERN_COLORS['background'],
                           activebackground=MODERN_COLORS['primary'],
                           troughcolor=MODERN_COLORS['border'],
                           highlightthickness=0,
                           relief='flat',
                           bd=0,
                           width=12)

    scrollable_frame = tk.Frame(canvas, bg=bg)

    # Configure scrolling
    def configure_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=(0, 0))
    
    if not hide_scrollbar:
        # Show scrollbar if not hidden
        scrollbar.pack(side="right", fill="y", padx=(0, 0))
    else:
        # Hide scrollbar but keep it functional
        scrollbar.pack_forget()

    # Bind mousewheel to canvas for scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Bind touchpad scrolling for better mobile experience
    def _on_touchpad_scroll(event):
        if event.delta:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:  # Scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<Button-4>", _on_touchpad_scroll)
    canvas.bind_all("<Button-5>", _on_touchpad_scroll)
    
    # Bind keyboard scrolling for accessibility
    def _on_key_scroll(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")
        elif event.keysym == "Page_Up":
            canvas.yview_scroll(-5, "units")
        elif event.keysym == "Page_Down":
            canvas.yview_scroll(5, "units")
        elif event.keysym == "Home":
            canvas.yview_moveto(0)
        elif event.keysym == "End":
            canvas.yview_moveto(1)

    canvas.bind_all("<KeyPress>", _on_key_scroll)
    canvas.focus_set()  # Allow keyboard focus

    # Store references for cleanup
    main_frame.canvas = canvas
    main_frame.scrollable_frame = scrollable_frame
    main_frame.scrollbar = scrollbar

    return main_frame

def toggle_scrollbar_visibility(scrollable_frame, show=True):
    """Toggle scrollbar visibility for a scrollable frame"""
    if hasattr(scrollable_frame, 'scrollbar'):
        if show:
            scrollable_frame.scrollbar.pack(side="right", fill="y", padx=(0, 0))
        else:
            scrollable_frame.scrollbar.pack_forget()

# --- Storage files/folders ---
ACCOUNTS_FILE = "accounts.json"
USERS_FOLDER = "users"
if not os.path.exists(USERS_FOLDER):
    os.makedirs(USERS_FOLDER)

# Global data structures
accounts = {}
current_user = None

# New data structure integration
financial_data_manager = FinancialDataManager()
financial_analytics = FinancialAnalytics(financial_data_manager)

# Legacy variables for backward compatibility
current_entries = []
current_expenses = []
undo_stack = []
redo_stack = []
undo_expense_stack = []
redo_expense_stack = []

# Navigation history for undo functionality
navigation_history = []

# Global financial data (legacy)
financial_data = {}

def add_to_history(function_name, *args):
    """Add current screen to navigation history"""
    global navigation_history
    navigation_history.append((function_name, args))
    # Keep only last 10 entries to prevent memory issues
    if len(navigation_history) > 10:
        navigation_history.pop(0)

def navigate_back():
    """Go back to previous screen"""
    global navigation_history
    if len(navigation_history) >= 2:
        # Remove current screen
        navigation_history.pop()
        # Get previous screen
        prev_function, prev_args = navigation_history[-1]
        # Remove it from history so we don't create a loop
        navigation_history.pop()
        # Navigate to previous screen
        if prev_function == 'calendar_screen':
            calendar_screen()
        elif prev_function == 'income_screen':
            income_screen(*prev_args)
        elif prev_function == 'expenses_screen':
            expenses_screen(*prev_args)
        elif prev_function == 'total_screen':
            total_screen(*prev_args)
        elif prev_function == 'login_screen':
            login_screen()
        elif prev_function == 'create_account_screen':
            create_account_screen()
        elif prev_function == 'splash_screen':
            splash_screen()
    else:
        messagebox.showinfo("Info", "No previous page to go back to")

def create_undo_button(parent, command=None, style='warning', width=15):
    """Create a standardized undo button"""
    if command is None:
        command = navigate_back

    undo_btn = create_modern_button(parent, "← Back",
                                   command=command,
                                   style=style, width=width)
    return undo_btn

def add_global_undo_shortcut(window):
    """Add Ctrl+Z keyboard shortcut for undo functionality"""
    window.bind('<Control-z>', lambda e: navigate_back())
    window.bind('<Control-Z>', lambda e: navigate_back())


def load_accounts():
    global accounts
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                accounts = json.load(f)
        except Exception:
            accounts = {}
    else:
        accounts = {}

def save_accounts():
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

def user_file(username):
    return os.path.join(USERS_FOLDER, f"{username}.json")

def load_user_data(username):
    global financial_data, financial_data_manager
    path = user_file(username)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                financial_data = data

                # Load transactions into new data structures
                financial_data_manager = FinancialDataManager()
                for date_str, day_data in data.items():
                    if isinstance(day_data, dict) and 'entries' in day_data:
                        # Load income entries
                        for entry in day_data.get('entries', []):
                            if len(entry) >= 2:
                                transaction_date = datetime.fromisoformat(date_str)
                                financial_data_manager.add_transaction(
                                    description=entry[0],
                                    amount=float(entry[1]),
                                    category="Income",
                                    transaction_type="income",
                                    date=transaction_date
                                )

                        # Load expense entries
                        for entry in day_data.get('expense_entries', []):
                            if len(entry) >= 2:
                                transaction_date = datetime.fromisoformat(date_str)
                                financial_data_manager.add_transaction(
                                    description=entry[0],
                                    amount=float(entry[1]),
                                    category=entry[0],  # Use description as category for expenses
                                    transaction_type="expense",
                                    date=transaction_date
                                )

                # Update analytics
                global financial_analytics
                financial_analytics = FinancialAnalytics(financial_data_manager)

        except Exception as e:
            print(f"Error loading user data: {e}")
            financial_data = {}
            financial_data_manager = FinancialDataManager()
            financial_analytics = FinancialAnalytics(financial_data_manager)
    else:
        financial_data = {}
        financial_data_manager = FinancialDataManager()
        financial_analytics = FinancialAnalytics(financial_data_manager)

def save_user_data(username):
    global financial_data, financial_data_manager
    path = user_file(username)

    # Convert new data structures back to legacy format
    financial_data = {}
    all_transactions = financial_data_manager.transactions.to_list()

    for transaction in all_transactions:
        date_str = transaction.date.strftime("%Y-%m-%d")
        if date_str not in financial_data:
            financial_data[date_str] = {
                "income": 0.0,
                "expenses": 0.0,
                "entries": [],
                "expense_entries": []
            }

        if transaction.transaction_type == "income":
            financial_data[date_str]["entries"].append([transaction.description, transaction.amount])
            financial_data[date_str]["income"] += transaction.amount
        else:
            financial_data[date_str]["expense_entries"].append([transaction.description, transaction.amount])
            financial_data[date_str]["expenses"] += transaction.amount

    with open(path, "w") as f:
        json.dump(financial_data, f, indent=2)


load_accounts()


def splash_screen():
    # Add to navigation history
    add_to_history('splash_screen')

    splash = tk.Tk()
    width, height = setup_adaptive_window(splash, "Money Rider - Financial Tracker")

    # Get adaptive fonts for consistent sizing
    adaptive_fonts = get_adaptive_fonts()

    # Main container with standardized padding
    main_container = create_standard_container(splash)

    # Header section
    header_frame = create_standard_section(main_container, MODERN_COLORS['background'])
    padding = get_standard_padding()
    header_frame.pack(pady=(padding['large'], padding['xxl']))

    # App icon/logo area - standardized
    icon_frame = create_modern_frame(header_frame, MODERN_COLORS['primary'])
    icon_frame.pack(pady=padding['large'])
    icon_frame.configure(relief='flat', bd=0, height=120, width=120)

    # Option 1: Use emoji logo (current)
    icon_label = tk.Label(icon_frame, text="🏍️", font=('Segoe UI Emoji', 50),
                         bg=MODERN_COLORS['primary'], fg=MODERN_COLORS['white'])
    icon_label.pack(expand=True)

    # Title - adaptive typography
    title = tk.Label(header_frame, text="Money Rider",
                    font=adaptive_fonts['title'],
                    bg=MODERN_COLORS['background'],
                    fg=MODERN_COLORS['text_primary'])
    title.pack(pady=padding['element'])

    # Subtitle
    subtitle = tk.Label(header_frame, text="Track your finances with ease",
                       font=adaptive_fonts['subheading'],
                       bg=MODERN_COLORS['background'],
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=padding['small'])

    # Button container with standardized spacing
    button_frame = create_standard_section(main_container, MODERN_COLORS['background'])
    button_frame.pack(pady=padding['xxl'])

    # Login button - standardized
    login_btn = create_modern_button(button_frame, "📱 Sign In",
                                   command=lambda:[splash.destroy(), login_screen()],
                                   style='primary', width=20)
    login_btn.pack(pady=padding['large'])

    # Create account button - standardized
    create_account_btn = create_modern_button(button_frame, "👤 Create Account",
                                            command=lambda:[splash.destroy(), create_account_screen()],
                                            style='secondary', width=20)
    create_account_btn.pack(pady=padding['element'])

    # Footer - standardized
    footer_frame = create_standard_section(main_container, MODERN_COLORS['background'])
    footer_frame.pack(side=tk.BOTTOM, pady=padding['large'])

    footer_text = tk.Label(footer_frame, text="© 2024 Money Rider",
                          font=adaptive_fonts['body'],
                          bg=MODERN_COLORS['background'],
                          fg=MODERN_COLORS['text_secondary'])
    footer_text.pack()

    splash.mainloop()

# ---------------- Create Account ----------------
def create_account_screen():
    # Add to navigation history
    add_to_history('create_account_screen')

    create = tk.Tk()
    width, height = setup_adaptive_window(create, "Create Account - Money Rider")

    # Get adaptive fonts for consistent sizing
    adaptive_fonts = get_adaptive_fonts()

    # Main container with standardized padding
    main_container = create_standard_container(create)

    # Header - standardized
    header_frame = create_standard_section(main_container, MODERN_COLORS['background'])
    padding = get_standard_padding()
    header_frame.pack(pady=(0, padding['xxl']))

    title = tk.Label(header_frame, text="Create Account",
                    font=adaptive_fonts['title'],
                    bg=MODERN_COLORS['background'],
                    fg=MODERN_COLORS['text_primary'])
    title.pack(pady=padding['element'])

    subtitle = tk.Label(header_frame, text="Join Money Rider today",
                       font=adaptive_fonts['subheading'],
                       bg=MODERN_COLORS['background'],
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=padding['small'])

    # Form container - standardized card style
    form_frame = create_standard_section(main_container, MODERN_COLORS['card'])
    form_frame.pack(fill=tk.X, pady=padding['large'])
    form_frame.configure(relief='solid', bd=2)

    # Username field - mobile style
    tk.Label(form_frame, text="Username",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', padx=25, pady=(25, 8))

    username_entry = create_modern_entry(form_frame)
    username_entry.pack(fill=tk.X, padx=25, pady=(0, 20))

    # Password field - mobile style
    tk.Label(form_frame, text="Password",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', padx=25, pady=(15, 8))

    password_var = tk.StringVar()
    password_entry = create_modern_entry(form_frame, show="*")
    password_entry.config(textvariable=password_var)
    password_entry.pack(fill=tk.X, padx=25, pady=(0, 10))

    # Password visibility toggle - mobile style
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁 Show Password")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈 Hide Password")

    eye_btn = create_modern_button(form_frame, "👁 Show Password", command=toggle_pw, style='secondary', width=20)
    eye_btn.pack(pady=(0, 25))

    def create_account():
        username = username_entry.get().strip()
        password = password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        if username in accounts:
            messagebox.showerror("Error", "Username already exists")
            return
        accounts[username] = password
        save_accounts()
        # create user data file (empty financial_data)
        with open(user_file(username), "w") as f:
            json.dump({}, f)
        messagebox.showinfo("Success", "Account created successfully! Please sign in.")
        create.destroy()
        splash_screen()

    # Button container - mobile style
    button_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    button_frame.pack(pady=30)

    # Create button - mobile style
    create_btn = create_modern_button(button_frame, "✅ Create Account",
                                    command=create_account,
                                    style='primary', width=20)
    create_btn.pack(pady=20)

    # Back button - mobile style
    back_btn = create_modern_button(button_frame, "← Back to Sign In",
                                  command=lambda: [create.destroy(), splash_screen()],
                                  style='secondary', width=20)
    back_btn.pack(pady=10)

# ---------------- Login ----------------
def login_screen():
    # Add to navigation history
    add_to_history('login_screen')

    login = tk.Tk()
    width, height = setup_adaptive_window(login, "Sign In - Money Rider")

    # Get adaptive fonts for consistent sizing
    adaptive_fonts = get_adaptive_fonts()

    # Main container with standardized padding
    main_container = create_standard_container(login)

    # Header - standardized
    header_frame = create_standard_section(main_container, MODERN_COLORS['background'])
    padding = get_standard_padding()
    header_frame.pack(pady=(0, padding['xxl']))

    title = tk.Label(header_frame, text="Welcome Back",
                    font=adaptive_fonts['title'],
                    bg=MODERN_COLORS['background'],
                    fg=MODERN_COLORS['text_primary'])
    title.pack(pady=padding['element'])

    subtitle = tk.Label(header_frame, text="Sign in to your account",
                       font=adaptive_fonts['subheading'],
                       bg=MODERN_COLORS['background'],
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=padding['small'])

    # Form container - standardized card style
    form_frame = create_standard_section(main_container, MODERN_COLORS['card'])
    form_frame.pack(fill=tk.X, pady=padding['large'])
    form_frame.configure(relief='solid', bd=2)

    # Username field - mobile style
    tk.Label(form_frame, text="Username",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', padx=25, pady=(25, 8))

    username_entry = create_modern_entry(form_frame)
    username_entry.pack(fill=tk.X, padx=25, pady=(0, 20))

    # Password field - mobile style
    tk.Label(form_frame, text="Password",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', padx=25, pady=(15, 8))

    password_var = tk.StringVar()
    password_entry = create_modern_entry(form_frame, show="*")
    password_entry.config(textvariable=password_var)
    password_entry.pack(fill=tk.X, padx=25, pady=(0, 10))

    # Password visibility toggle - mobile style
    def toggle_pw():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_btn.config(text="👁 Show Password")
        else:
            password_entry.config(show="")
            eye_btn.config(text="🙈 Hide Password")

    eye_btn = create_modern_button(form_frame, "👁 Show Password", command=toggle_pw, style='secondary', width=20)
    eye_btn.pack(pady=(0, 25))

    def validate_login():
        username = username_entry.get().strip()
        password = password_var.get()
        if username in accounts and accounts[username] == password:
            # load this user's data
            global current_user, financial_data
            current_user = username
            load_user_data(current_user)
            login.destroy()
            calendar_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    # Button container - mobile style
    button_frame = create_modern_frame(main_container, MODERN_COLORS['background'])
    button_frame.pack(pady=10)

    # Login button - mobile style
    login_btn = create_modern_button(button_frame, "🔑 Sign In",
                                   command=validate_login,
                                   style='primary', width=20)
    login_btn.pack(pady=20)

    # Back button - mobile style
    back_btn = create_modern_button(button_frame, "← Back to Home",
                                  command=lambda: [login.destroy(), splash_screen()],
                                  style='secondary', width=20)
    back_btn.pack(pady=10)

    # Add global undo shortcut
    add_global_undo_shortcut(login)

    # Focus on username entry
    username_entry.focus()

# ---------------- Calendar Screen (same layout/flow as original) ----------------
def calendar_screen():
    # Add to navigation history
    add_to_history('calendar_screen')

    cal = tk.Tk()
    width, height = setup_adaptive_window(cal, "Money Rider - Calendar")

    # Get adaptive fonts for consistent sizing
    adaptive_fonts = get_adaptive_fonts()

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Define variables for month/year selection
    month_var = tk.StringVar()
    year_var = tk.StringVar()

    def show_saved_data(date_str, day):
        # Create a popup window to display saved data
        popup = tk.Toplevel(cal)
        popup.title(f"Saved Data - {date_str}")
        popup.geometry("500x600")
        popup.configure(bg="#1C1C1C")

        # Main frame
        main_frame = tk.Frame(popup, bg="#1C1C1C")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        tk.Label(main_frame, text=f"Saved Financial Data", bg="#1C1C1C", fg="light",
                 font=("Bubblegum Sans", 20, "bold")).pack(pady=10)
        tk.Label(main_frame, text=date_str, bg="#1C1C1C", fg="#4CAF50",
                 font=("Bubblegum Sans", 14)).pack(pady=5)

        # Get the saved data (if missing, show zeros)
        data = financial_data.get(date_str, {"income": 0.0, "expenses": 0.0, "entries": [], "expense_entries": []})

        # Summary frame
        summary_frame = tk.Frame(main_frame, bg="#2C2C2C", bd=2, relief=tk.RIDGE)
        summary_frame.pack(fill=tk.X, padx=10, pady=15)

        # Income summary
        income_frame = tk.Frame(summary_frame, bg="#2C2C2C")
        income_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(income_frame, text="Total Income:", bg="#2C2C2C", fg="light",
                 font=("Bubblegum Sans", 14)).pack(side=tk.LEFT)
        tk.Label(income_frame, text=f"₱{data['income']:,.2f}", bg="#2C2C2C", fg="#4CAF50",
                 font=("Bubblegum Sans", 14, "bold")).pack(side=tk.RIGHT)

        # Expenses summary
        expenses_frame = tk.Frame(summary_frame, bg="#2C2C2C")
        expenses_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(expenses_frame, text="Total Expenses:", bg="#2C2C2C", fg="light",
                 font=("Bubblegum Sans", 14)).pack(side=tk.LEFT)
        tk.Label(expenses_frame, text=f"₱{data['expenses']:,.2f}", bg="#2C2C2C", fg="#F44336",
                 font=("Bubblegum Sans", 14, "bold")).pack(side=tk.RIGHT)

        # Net total
        net_frame = tk.Frame(summary_frame, bg="#2C2C2C")
        net_frame.pack(fill=tk.X, padx=10, pady=10)

        net_total = data['income'] - data['expenses']
        tk.Label(net_frame, text="Net Total:", bg="#2C2C2C", fg="light",
                 font=("Bubblegum Sans", 16)).pack(side=tk.LEFT)
        tk.Label(net_frame, text=f"₱{net_total:,.2f}", bg="#2C2C2C",
                 fg="#4CAF50" if net_total >= 0 else "#F44336",
                 font=("Bubblegum Sans", 16, "bold")).pack(side=tk.RIGHT)

        # Details frame
        details_frame = tk.Frame(main_frame, bg="#1C1C1C")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Notebook for income/expense details
        notebook = ttk.Notebook(details_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Income tab
        income_tab = tk.Frame(notebook, bg="#1C1C1C")
        notebook.add(income_tab, text="Income Details")

        if data.get('entries'):
            income_listbox = tk.Listbox(income_tab, bg="#404040", fg="white",
                                       font=("Courier New", 12), width=50)
            income_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for entry in data['entries']:
                income_listbox.insert(tk.END, f"{entry[0].ljust(30)}{str(entry[1]).rjust(10)}")
        else:
            tk.Label(income_tab, text="No income data", bg="#1C1C1C", fg="white",
                     font=("Bubblegum Sans", 14)).pack(pady=20)

        # Expenses tab
        expense_tab = tk.Frame(notebook, bg="#1C1C1C")
        notebook.add(expense_tab, text="Expense Details")

        if data.get('expense_entries'):
            expense_listbox = tk.Listbox(expense_tab, bg="#404040", fg="white",
                                         font=("Courier New", 12), width=50)
            expense_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for expense in data['expense_entries']:
                expense_listbox.insert(tk.END, f"{expense[0].ljust(30)}{str(expense[1]).rjust(10)}")
        else:
            tk.Label(expense_tab, text="No expense data", bg="#1C1C1C", fg="white",
                     font=("Bubblegum Sans", 14)).pack(pady=20)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1C1C1C")
        button_frame.pack(pady=10)

        # View/edit button (go to main entry screen for that day)
        edit_btn = create_modern_button(button_frame, "✏️ View/Edit",
                                       command=lambda: [popup.destroy(), cal.destroy(), 
                                                       income_screen(day, current_year, current_month)],
                                       style='primary', width=12)
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Close button
        close_btn = create_modern_button(button_frame, "❌ Close",
                                        command=popup.destroy,
                                        style='secondary', width=12)
        close_btn.pack(side=tk.LEFT, padx=5)

    def go_to_income(day):
        global current_entries, current_expenses

        # Save current date for later reference
        selected_date = f"{current_year}-{current_month:02d}-{day:02d}"

        # Load entries for this date (if exist) into buffers
        if selected_date in financial_data:
            daydata = financial_data[selected_date]
            current_entries = [(e[0], float(e[1])) for e in daydata.get("entries", [])]
            current_expenses = [(e[0], float(e[1])) for e in daydata.get("expense_entries", [])]
        else:
            current_entries = []
            current_expenses = []
        cal.destroy()
        income_screen(day, current_year, current_month)

    def create_calendar_grid():
        for widget in cal.winfo_children():
            widget.destroy()

        # Main container with scrolling
        cal_frame = create_scrollable_frame(cal, MODERN_COLORS['background'])
        padding = get_standard_padding()
        cal_frame.pack(fill=tk.BOTH, expand=True, padx=padding['element'], pady=padding['element'])

        # Get the scrollable frame for adding widgets
        scrollable_content = cal_frame.scrollable_frame

        # Header with title and controls
        header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title
        title_label = tk.Label(header_frame, text="Financial Calendar",
                              font=adaptive_fonts['heading'],
                              bg=MODERN_COLORS['background'],
                              fg=MODERN_COLORS['text_primary'])
        title_label.pack(pady=(0, 15))

        # Month and year selection
        controls_frame = create_modern_frame(header_frame, MODERN_COLORS['background'])
        controls_frame.pack()

        # Set current values
        month_var.set(calendar.month_name[current_month])
        month_menu = ttk.Combobox(controls_frame, textvariable=month_var,
                                 values=list(calendar.month_name[1:]),
                                 state="readonly",
                                 font=adaptive_fonts['body'],
                                 justify="center",
                                 width=12)
        month_menu.grid(row=0, column=0, padx=5, pady=5)
        month_menu.bind("<<ComboboxSelected>>", lambda e: change_month())

        year_var.set(str(current_year))
        year_menu = ttk.Combobox(controls_frame, textvariable=year_var,
                                values=list(range(2020, 2031)),
                                state="readonly",
                                font=adaptive_fonts['body'],
                                justify="center",
                                width=8)
        year_menu.grid(row=0, column=1, padx=5, pady=5)
        year_menu.bind("<<ComboboxSelected>>", lambda e: change_year())

        # Calendar container
        calendar_container = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
        calendar_container.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        calendar_container.configure(relief='solid', bd=1)

        # Days of week header
        days_frame = create_modern_frame(calendar_container, MODERN_COLORS['card'])
        days_frame.pack(fill=tk.X, padx=5, pady=10)

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days_of_week):
            day_label = tk.Label(days_frame, text=day,
                               bg=MODERN_COLORS['card'],
                               fg=MODERN_COLORS['text_primary'],
                               font=adaptive_fonts['body'])
            day_label.grid(row=0, column=col, padx=1, pady=5, sticky='ew')

        # Configure grid weights for weekday headers to match calendar grid
        for i in range(7):
            days_frame.grid_columnconfigure(i, weight=1)

        # Calendar days grid
        days_grid_frame = create_modern_frame(calendar_container, MODERN_COLORS['card'])
        days_grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

        month_cal = calendar.monthcalendar(current_year, current_month)
        for row, week in enumerate(month_cal):
            for col, day in enumerate(week):
                if day == 0:
                    # Empty space for days not in the month
                    empty_label = tk.Label(days_grid_frame, text="",
                                         bg=MODERN_COLORS['light'])
                    empty_label.grid(row=row+1, column=col, padx=1, pady=1, sticky='nsew')
                    continue

                date_str = f"{current_year}-{current_month:02d}-{day:02d}"

                # Determine button style
                if (day == current_date.day and
                    current_month == current_date.month and
                    current_year == current_date.year):
                    # Current day
                    day_bg = MODERN_COLORS['primary']
                    day_fg = MODERN_COLORS['white']
                elif date_str in financial_data:
                    # Days with data
                    day_bg = MODERN_COLORS['success']
                    day_fg = MODERN_COLORS['white']
                else:
                    # Regular days
                    day_bg = MODERN_COLORS['light']
                    day_fg = MODERN_COLORS['dark']

                day_button = tk.Button(days_grid_frame, text=str(day),
                                     bg=day_bg, fg=day_fg,
                                     font=adaptive_fonts['body'],
                                     relief='flat', bd=1,
                                     cursor='hand2',
                                     command=lambda d=day: go_to_income(d))
                day_button.grid(row=row + 1, column=col, padx=1, pady=1, sticky='nsew')

                # Add hover effect
                # Add smooth hover effect
                if day_bg == MODERN_COLORS['primary']:
                    hover_bg = MODERN_COLORS['primary_dark']
                elif day_bg == MODERN_COLORS['success']:
                    hover_bg = '#059669'
                else:
                    hover_bg = MODERN_COLORS['border']

                add_smooth_hover_effect(day_button, day_bg, hover_bg, scale_effect=False)

        # Configure grid weights for proper sizing
        for i in range(7):
            days_grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            days_grid_frame.grid_rowconfigure(i, weight=1)

        # Date range calculation section
        range_container = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
        range_container.pack(fill=tk.X, pady=15, padx=5)

        range_title = tk.Label(range_container, text="Date Range Calculator",
                              font=adaptive_fonts['subheading'],
                              bg=MODERN_COLORS['background'],
                              fg=MODERN_COLORS['text_primary'])
        range_title.pack(pady=(0, 10))

        # Range input frame
        range_frame = create_modern_frame(range_container, MODERN_COLORS['card'])
        range_frame.pack(fill=tk.X, pady=10)
        range_frame.configure(relief='solid', bd=1)

        # Date input frame using grid for better width utilization
        date_input_frame = create_modern_frame(range_frame, MODERN_COLORS['card'])
        date_input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Configure grid weights for better distribution
        for i in range(4):
            date_input_frame.grid_columnconfigure(i, weight=1)

        # Start date row
        tk.Label(date_input_frame, text="From:",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)

        start_day = ttk.Combobox(date_input_frame, values=list(range(1, 32)), width=4,
                                 font=adaptive_fonts['body'], state="readonly")
        start_day.grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        start_day.set("1")

        start_month = ttk.Combobox(date_input_frame, values=list(calendar.month_name[1:]), width=15,
                                   font=adaptive_fonts['body'], state="readonly")
        start_month.grid(row=0, column=2, sticky="ew", padx=2, pady=5)
        start_month.set(calendar.month_name[current_month])

        start_year = ttk.Combobox(date_input_frame, values=list(range(2020, 2031)), width=8,
                                  font=adaptive_fonts['body'], state="readonly")
        start_year.grid(row=0, column=3, sticky="ew", padx=2, pady=5)
        start_year.set(str(current_year))

        # End date row
        tk.Label(date_input_frame, text="To:",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=5)

        end_day = ttk.Combobox(date_input_frame, values=list(range(1, 32)), width=4,
                               font=adaptive_fonts['body'], state="readonly")
        end_day.grid(row=1, column=1, sticky="ew", padx=2, pady=5)
        end_day.set("1")

        end_month = ttk.Combobox(date_input_frame, values=list(calendar.month_name[1:]), width=15,
                                 font=adaptive_fonts['body'], state="readonly")
        end_month.grid(row=1, column=2, sticky="ew", padx=2, pady=5)
        end_month.set(calendar.month_name[current_month])

        end_year = ttk.Combobox(date_input_frame, values=list(range(2020, 2031)), width=8,
                                font=adaptive_fonts['body'], state="readonly")
        end_year.grid(row=1, column=3, sticky="ew", padx=2, pady=5)
        end_year.set(str(current_year))

        def calculate_range():
            try:
                # Get start date components
                start_d = int(start_day.get())
                start_m = list(calendar.month_name).index(start_month.get())
                start_y = int(start_year.get())

                # Get end date components
                end_d = int(end_day.get())
                end_m = list(calendar.month_name).index(end_month.get())
                end_y = int(end_year.get())

                # Create date strings for comparison
                start_date_str = f"{start_y}-{start_m:02d}-{start_d:02d}"
                end_date_str = f"{end_y}-{end_m:02d}-{end_d:02d}"

                # Validate date range
                if start_date_str > end_date_str:
                    messagebox.showerror("Error", "Start date must be before end date")
                    return

                # Calculate totals
                total_income = 0.0
                total_expenses = 0.0
                days_with_data = 0

                for date_str in sorted(financial_data.keys()):
                    if start_date_str <= date_str <= end_date_str:
                        data = financial_data[date_str]
                        total_income += float(data.get("income", 0))
                        total_expenses += float(data.get("expenses", 0))
                        days_with_data += 1

                net_total = total_income - total_expenses

                # Display results in modern window
                result_window = tk.Toplevel(cal)
                result_window.title("Date Range Results")
                result_window.geometry("500x400")
                result_window.configure(bg=MODERN_COLORS['light'])
                result_window.resizable(False, False)

                # Center the result window
                result_window.update_idletasks()
                x = (result_window.winfo_screenwidth() // 2) - (500 // 2)
                y = (result_window.winfo_screenheight() // 2) - (400 // 2)
                result_window.geometry(f"500x400+{x}+{y}")

                # Main container
                result_container = create_modern_frame(result_window, MODERN_COLORS['light'])
                result_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

                # Title
                title_label = tk.Label(result_container, text="Financial Summary",
                                     font=adaptive_fonts['heading'],
                                     bg=MODERN_COLORS['light'],
                                     fg=MODERN_COLORS['dark'])
                title_label.pack(pady=(0, 20))

                # Date range
                date_label = tk.Label(result_container, text=f"{start_date_str} to {end_date_str}",
                                     font=adaptive_fonts['body'],
                                     bg=MODERN_COLORS['light'],
                                     fg=MODERN_COLORS['dark'])
                date_label.pack(pady=(0, 20))

                # Summary frame
                summary_frame = create_modern_frame(result_container, MODERN_COLORS['light'])
                summary_frame.pack(fill=tk.X, pady=10)
                summary_frame.configure(relief='solid', bd=1)

                # Results
                results = [
                    ("Days with data", str(days_with_data), MODERN_COLORS['dark']),
                    ("Total Income", f"₱{total_income:,.2f}", MODERN_COLORS['success']),
                    ("Total Expenses", f"₱{total_expenses:,.2f}", MODERN_COLORS['danger']),
                    ("Net Total", f"₱{net_total:,.2f}", 
                     MODERN_COLORS['success'] if net_total >= 0 else MODERN_COLORS['danger'])
                ]

                for label, value, color in results:
                    result_frame = create_modern_frame(summary_frame, MODERN_COLORS['light'])
                    result_frame.pack(fill=tk.X, padx=20, pady=8)

                    tk.Label(result_frame, text=label,
                            font=adaptive_fonts['body'],
                            bg=MODERN_COLORS['dark'],
                            fg=MODERN_COLORS['white']).pack(side=tk.LEFT)

                    tk.Label(result_frame, text=value,
                            font=adaptive_fonts['body'],
                            bg=MODERN_COLORS['dark'],
                            fg=color).pack(side=tk.RIGHT)

                # Close button
                close_btn = create_modern_button(result_container, "Close",
                                               command=result_window.destroy,
                                               style='primary', width=15)
                close_btn.pack(pady=20)

            except ValueError:
                messagebox.showerror("Error", "Invalid date selection")

        # Calculate button
        calc_button = create_modern_button(range_frame, "Calculate Range",
                                         command=calculate_range,
                                         style='primary', width=20)
        calc_button.pack(pady=10)

        # Navigation buttons - mobile style
        nav_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
        nav_frame.pack(pady=20)

        # Undo button - mobile style
        undo_btn = create_undo_button(nav_frame,
                                     command=lambda: [cal.destroy(), navigate_back()],
                                     style='warning', width=20)
        undo_btn.pack(pady=5)

        # Settings button - mobile style
        settings_btn = create_modern_button(nav_frame, "⚙️ Settings",
                                          command=lambda: [cal.destroy(), settings_screen()],
                                          style='secondary', width=20)
        settings_btn.pack(pady=5)

        # Charts & Visualizations button - mobile style
        charts_btn = create_modern_button(nav_frame, "📊 Charts & Visualizations",
                                        command=lambda: [cal.destroy(), charts_screen()],
                                        style='secondary', width=20)
        charts_btn.pack(pady=5)

        # Sign out button with better mobile styling
        signout_btn = create_modern_button(nav_frame, "🚪 Sign Out",
                                          command=lambda: [cal.destroy(), login_screen()],
                                          style='danger', width=20)
        signout_btn.pack(pady=5)

    def change_month():
        nonlocal current_month
        selected_month = month_var.get()
        current_month = list(calendar.month_name).index(selected_month)
        create_calendar_grid()

    def change_year():
        nonlocal current_year
        current_year = int(year_var.get())
        create_calendar_grid()

    # Add global undo shortcut
    add_global_undo_shortcut(cal)

    create_calendar_grid()
    cal.mainloop()

# ---------------- Financial Tracking Screen (Redesigned with Consistency) ----------------
def income_screen(day, year, month):
    # Add to navigation history
    add_to_history('income_screen', day, year, month)

    inc = tk.Tk()
    width, height = setup_adaptive_window(inc, "Financial Tracking - Money Rider")

    # Get adaptive fonts and standardized padding
    adaptive_fonts = get_adaptive_fonts()
    padding = get_standard_padding()

    # Variables for form data
    name_var = tk.StringVar()
    income_var = tk.StringVar()
    expense_var = tk.StringVar()
    amount_var = tk.StringVar()
    category_var = tk.StringVar()
    custom_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Main container with standardized scrolling
    main_container = create_scrollable_frame(inc, MODERN_COLORS['background'])
    main_container.pack(fill=tk.BOTH, expand=True, padx=padding['element'], pady=padding['element'])

    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Configure scrolling properly
    def configure_scroll_region(event=None):
        main_container.canvas.configure(scrollregion=main_container.canvas.bbox("all"))

    scrollable_content.bind("<Configure>", configure_scroll_region)

    # Header section - standardized
    header_frame = create_standard_section(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(fill=tk.X, pady=(0, padding['large']))

    # Title - centered and consistent
    title_label = tk.Label(header_frame, text="Financial Tracking",
                          font=adaptive_fonts['title'],
                          bg=MODERN_COLORS['background'],
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, padding['small']))

    # Date display - centered and consistent
    date_label = tk.Label(header_frame, text=f"{year}-{month:02d}-{day:02d}",
                         font=adaptive_fonts['subheading'],
                         bg=MODERN_COLORS['background'],
                         fg=MODERN_COLORS['text_secondary'])
    date_label.pack(pady=padding['small'])

    # Navigation buttons - standardized
    nav_frame = create_standard_section(header_frame, MODERN_COLORS['background'])
    nav_frame.pack(fill=tk.X, pady=padding['element'])

    # Back button - consistent styling
    back_btn = create_undo_button(nav_frame,
                                 command=lambda: [inc.destroy(), navigate_back()],
                                 style='warning', width=20)
    back_btn.pack(pady=padding['small'])

    # Input section with standardized cards
    input_frame = create_standard_section(scrollable_content, MODERN_COLORS['background'])
    input_frame.pack(fill=tk.X, pady=(0, padding['element']))

    # Create notebook for tabs with consistent styling
    notebook = ttk.Notebook(input_frame)
    notebook.pack(fill=tk.X, padx=padding['small'])

    # Style the notebook consistently
    style = ttk.Style()
    style.configure('TNotebook', tabposition='n')
    style.configure('TNotebook.Tab', padding=[padding['element'], padding['small']], 
                   font=adaptive_fonts['body'])

    # Add smooth tab transitions
    def on_tab_change(event):
        smooth_tab_transition(notebook, None, None, duration=200)

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    # Income tab with consistent card styling
    income_tab = create_modern_frame(notebook, MODERN_COLORS['card'])
    notebook.add(income_tab, text="💰 Income")

    # Income card container - standardized
    income_card = create_standard_section(income_tab, MODERN_COLORS['card'])
    income_card.configure(relief='solid', bd=1)

    # Income Source field - consistent styling
    tk.Label(income_card, text="Income Source",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=padding['element'], 
                                                   pady=(padding['element'], padding['small']))

    name_entry = create_modern_entry(income_card, width=25)
    name_entry.config(textvariable=name_var)
    name_entry.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))

    # Income amount field - consistent styling
    tk.Label(income_card, text="Amount (₱)",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=padding['element'], 
                                                   pady=(padding['small'], padding['small']))

    income_entry = create_modern_entry(income_card, width=25)
    income_entry.config(textvariable=income_var)
    income_entry.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))

    # Define functions before buttons
    def enter_income():
        name = name_var.get().strip()
        income = income_var.get().strip()
        if not name or not income:
            messagebox.showinfo("Error", "Please fill in all fields!")
            return

        try:
            income_val = float(income)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            return

        entry = (name, income_val)
        current_entries.append(entry)
        # Format with modern styling
        income_listbox.insert(tk.END, f"{name:<30} ₱{income_val:>10,.2f}")
        name_var.set("")
        income_var.set("")
        # autosave to user's financial_data
        save_data(current_date_str)

    def enter_expense():
        category = category_var.get()
        if category == "Other":
            category = custom_var.get().strip()
        amount = amount_var.get().strip()
        if not category or not amount:
            messagebox.showinfo("Error", "Please fill in all fields!")
            return
        try:
            amount_val = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            return

        entry = (category, amount_val)
        current_expenses.append(entry)
        # Format with modern styling
        expense_listbox.insert(tk.END, f"{category:<30} ₱{amount_val:>10,.2f}")
        amount_var.set("")
        custom_var.set("")
        # autosave to user's financial_data
        save_data(current_date_str)

    # Add Income button - consistent styling
    add_income_btn = create_modern_button(income_card, "➕ Add Income",
                                        command=enter_income,
                                        style='success', width=25)
    add_income_btn.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))

    # Expenses tab with mobile card styling
    expense_tab = create_modern_frame(notebook, MODERN_COLORS['card'])
    notebook.add(expense_tab, text="💸 Expenses")

    # Expense card container - standardized
    expense_card = create_standard_section(expense_tab, MODERN_COLORS['card'])
    expense_card.configure(relief='solid', bd=1)

    # Expense Category field - consistent styling
    tk.Label(expense_card, text="Category",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=padding['element'], 
                                                   pady=(padding['element'], padding['small']))

    # Category dropdown - consistent styling
    categories = ["Food", "Gas", "Maintenance", "Other"]
    cat_menu = ttk.Combobox(expense_card, values=categories, textvariable=category_var,
                           state="readonly", font=adaptive_fonts['body'], width=25)
    cat_menu.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))
    cat_menu.set(categories[0])

    # Custom category entry (hidden by default)
    custom_entry = create_modern_entry(expense_card, width=25)
    custom_entry.config(textvariable=custom_var)

    # Show/hide custom entry based on category selection
    def on_cat_change(e=None):
        if category_var.get() == "Other":
            custom_entry.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))
        else:
            custom_entry.pack_forget()
    cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

    # Expense amount field - consistent styling
    tk.Label(expense_card, text="Amount (₱)",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(anchor='w', 
                                                   padx=padding['element'], 
                                                   pady=(padding['small'], padding['small']))

    expense_amount_entry = create_modern_entry(expense_card, width=25)
    expense_amount_entry.config(textvariable=amount_var)
    expense_amount_entry.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))

    # Add Expense button - consistent styling
    add_expense_btn = create_modern_button(expense_card, "➕ Add Expense",
                                         command=enter_expense,
                                         style='danger', width=25)
    add_expense_btn.pack(fill=tk.X, padx=padding['element'], pady=(0, padding['element']))

    # Display section with tabs - standardized
    display_frame = create_standard_section(scrollable_content, MODERN_COLORS['card'])
    display_frame.pack(fill=tk.X, pady=(0, padding['element']))
    display_frame.configure(relief='solid', bd=1, height=250)

    # Create notebook for display tabs - consistent styling
    display_notebook = ttk.Notebook(display_frame)
    display_notebook.pack(fill=tk.BOTH, expand=True, padx=padding['small'], pady=padding['small'])

    # Add smooth tab transitions
    def on_display_tab_change(event):
        smooth_tab_transition(display_notebook, None, None, duration=200)

    display_notebook.bind("<<NotebookTabChanged>>", on_display_tab_change)

    # Income display tab - consistent styling
    income_display_tab = create_modern_frame(display_notebook, MODERN_COLORS['card'])
    display_notebook.add(income_display_tab, text="💰 Income List")

    # Header for income list - consistent styling
    income_header = create_standard_section(income_display_tab, MODERN_COLORS['card'])
    income_header.pack(fill=tk.X, pady=padding['small'])

    tk.Label(income_header, text="Income Source",
            font=adaptive_fonts['body'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, padx=padding['small'])

    tk.Label(income_header, text="Amount",
            font=adaptive_fonts['body'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.RIGHT, padx=padding['small'])

    # Create income listbox with double-click editing - consistent styling
    income_listbox = tk.Listbox(income_display_tab,
                               font=adaptive_fonts['body'],
                               bg=MODERN_COLORS['white'],
                               fg=MODERN_COLORS['dark'],
                               selectbackground=MODERN_COLORS['primary'],
                               selectforeground=MODERN_COLORS['white'],
                               relief='flat',
                               bd=0,
                               highlightthickness=0,
                               cursor='hand2')
    income_listbox.pack(fill=tk.BOTH, expand=True, padx=padding['small'], pady=(0, padding['small']))

    # Add smooth transitions to listbox
    smooth_listbox_selection(income_listbox)

    # Bind double-click to edit income
    income_listbox.bind('<Double-Button-1>', lambda e: edit_income_selected())

    # Expenses display tab - consistent styling
    expense_display_tab = create_modern_frame(display_notebook, MODERN_COLORS['card'])
    display_notebook.add(expense_display_tab, text="💸 Expense List")

    # Header for expense list - consistent styling
    expense_header = create_standard_section(expense_display_tab, MODERN_COLORS['card'])
    expense_header.pack(fill=tk.X, pady=padding['small'])

    tk.Label(expense_header, text="Expense Category",
            font=adaptive_fonts['body'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, padx=padding['small'])

    tk.Label(expense_header, text="Amount",
            font=adaptive_fonts['body'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.RIGHT, padx=padding['small'])

    # Create expense listbox with double-click editing - consistent styling
    expense_listbox = tk.Listbox(expense_display_tab,
                                font=adaptive_fonts['body'],
                                bg=MODERN_COLORS['white'],
                                fg=MODERN_COLORS['dark'],
                                selectbackground=MODERN_COLORS['primary'],
                                selectforeground=MODERN_COLORS['white'],
                                relief='flat',
                                bd=0,
                                highlightthickness=0,
                                cursor='hand2')
    expense_listbox.pack(fill=tk.BOTH, expand=True, padx=padding['small'], pady=(0, padding['small']))

    # Add smooth transitions to listbox
    smooth_listbox_selection(expense_listbox)

    # Bind double-click to edit expense
    expense_listbox.bind('<Double-Button-1>', lambda e: edit_expense_selected())

    # Populate listboxes with existing data
    for entry in current_entries:
        income_listbox.insert(tk.END, f"{entry[0]:<30} ₱{entry[1]:>10,.2f}")

    for expense in current_expenses:
        expense_listbox.insert(tk.END, f"{expense[0]:<30} ₱{expense[1]:>10,.2f}")

    # === EDIT MODE for income ===
    def edit_income_selected():
        sel = income_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No income selected to edit")
            return
        idx = sel[0]
        old_name, old_amount = current_entries[idx]

        edit_win = tk.Toplevel(inc)
        edit_win.title("Edit Income Entry")
        edit_win.geometry("400x300")
        edit_win.configure(bg=MODERN_COLORS['light'])
        edit_win.resizable(False, False)

        # Center the edit window
        edit_win.update_idletasks()
        x = (edit_win.winfo_screenwidth() // 2) - (400 // 2)
        y = (edit_win.winfo_screenheight() // 2) - (300 // 2)
        edit_win.geometry(f"400x300+{x}+{y}")

        # Main container
        edit_container = create_modern_frame(edit_win, MODERN_COLORS['light'])
        edit_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title
        title_label = tk.Label(edit_container, text="Edit Income Entry",
                             font=adaptive_fonts['subheading'],
                             bg=MODERN_COLORS['light'],
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 20))

        # Income source field
        tk.Label(edit_container, text="Income Source",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))

        e_name = create_modern_entry(edit_container)
        e_name.insert(0, old_name)
        e_name.pack(fill=tk.X, pady=(0, 15))

        # Amount field
        tk.Label(edit_container, text="Amount (₱)",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))

        e_income = create_modern_entry(edit_container)
        e_income.insert(0, str(old_amount))
        e_income.pack(fill=tk.X, pady=(0, 20))

        def save_edit():
            new_name = e_name.get().strip()
            new_income_str = e_income.get().strip()
            if not new_name or not new_income_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_income = float(new_income_str)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
                return
            # Update in-memory entries and listbox
            current_entries[idx] = (new_name, new_income)
            income_listbox.delete(0, tk.END)
            for entry in current_entries:
                income_listbox.insert(tk.END, f"{entry[0]:<30} ₱{entry[1]:>10,.2f}")
            edit_win.destroy()
            save_data(current_date_str)

        # Save button
        save_btn = create_modern_button(edit_container, "Save Changes",
                                      command=save_edit,
                                      style='success', width=20)
        save_btn.pack(pady=10)

    # === EDIT MODE for expense ===
    def edit_expense_selected():
        sel = expense_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to edit")
            return
        idx = sel[0]
        old_desc, old_amount = current_expenses[idx]

        edit_win = tk.Toplevel(inc)
        edit_win.title("Edit Expense Entry")
        edit_win.geometry("420x300")
        edit_win.configure(bg=MODERN_COLORS['light'])
        edit_win.resizable(False, False)

        # Center the edit window
        edit_win.update_idletasks()
        x = (edit_win.winfo_screenwidth() // 2) - (420 // 2)
        y = (edit_win.winfo_screenheight() // 2) - (300 // 2)
        edit_win.geometry(f"420x300+{x}+{y}")

        # Main container
        edit_container = create_modern_frame(edit_win, MODERN_COLORS['light'])
        edit_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title
        title_label = tk.Label(edit_container, text="Edit Expense Entry",
                             font=adaptive_fonts['subheading'],
                             bg=MODERN_COLORS['light'],
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 20))

        # Category field
        tk.Label(edit_container, text="Category",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))

        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(edit_container, values=categories, textvariable=cat_var,
                               state="readonly", font=adaptive_fonts['body'])
        # if old_desc matches one of categories, select it; else select Other and show custom
        if old_desc in categories:
            cat_menu.set(old_desc)
        else:
            cat_menu.set("Other")
        cat_menu.pack(fill=tk.X, pady=(0, 15))

        custom_var = tk.StringVar()
        custom_entry = create_modern_entry(edit_container)
        custom_entry.config(textvariable=custom_var)
        if cat_menu.get() == "Other":
            custom_var.set(old_desc)
            custom_entry.pack(fill=tk.X, pady=(0, 15))

        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(fill=tk.X, pady=(0, 15))
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        # Amount field
        tk.Label(edit_container, text="Amount (₱)",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))

        e_amount = create_modern_entry(edit_container)
        e_amount.insert(0, str(old_amount))
        e_amount.pack(fill=tk.X, pady=(0, 20))

        def save_edit():
            if cat_menu.get() == "Other":
                new_desc = custom_var.get().strip()
            else:
                new_desc = cat_menu.get()
            new_amount_str = e_amount.get().strip()
            if not new_desc or not new_amount_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_amount = float(new_amount_str)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
                return
            current_expenses[idx] = (new_desc, new_amount)
            expense_listbox.delete(0, tk.END)
            for expense in current_expenses:
                expense_listbox.insert(tk.END, f"{expense[0]:<30} ₱{expense[1]:>10,.2f}")
            edit_win.destroy()
            save_data(current_date_str)

        # Save button
        save_btn = create_modern_button(edit_container, "Save Changes",
                                      command=save_edit,
                                      style='success', width=20)
        save_btn.pack(pady=10)

    # Delete selected income with confirmation
    def delete_income_selected():
        sel = income_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "Please select an income entry to delete")
            return
        idx = sel[0]
        entry = current_entries[idx]

        # Show confirmation dialog
        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete this income entry?\n\n"
                                   f"Source: {entry[0]}\n"
                                   f"Amount: ₱{entry[1]:,.2f}")

        if result:
            current_entries.pop(idx)
            income_listbox.delete(idx)
            save_data(current_date_str)
            messagebox.showinfo("Success", "Income entry deleted successfully!")

    # Delete selected expense with confirmation
    def delete_expense_selected():
        sel = expense_listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "Please select an expense entry to delete")
            return
        idx = sel[0]
        expense = current_expenses[idx]

        # Show confirmation dialog
        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete this expense entry?\n\n"
                                   f"Category: {expense[0]}\n"
                                   f"Amount: ₱{expense[1]:,.2f}")

        if result:
            current_expenses.pop(idx)
            expense_listbox.delete(idx)
            save_data(current_date_str)
            messagebox.showinfo("Success", "Expense entry deleted successfully!")

    # Mobile-style button section
    button_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    button_frame.pack(fill=tk.X, pady=10)

    # Undo button (bottom section) - mobile style
    undo_btn = create_modern_button(button_frame, "← Back to Calendar",
                                   command=lambda: [inc.destroy(), navigate_back()],
                                   style='warning', width=18)
    undo_btn.pack(pady=5)

    # Action buttons - standardized card style
    action_card = create_standard_section(button_frame, MODERN_COLORS['light'])
    action_card.configure(relief='solid', bd=1)

    # Income management section - consistent styling
    tk.Label(action_card, text="📊 Manage Income",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['light'],
            fg=MODERN_COLORS['text_primary']).pack(pady=(padding['element'], padding['small']))

    # Instruction label for income - consistent styling
    tk.Label(action_card, text="💡 Double-click an item to edit, or use buttons below",
            font=adaptive_fonts['small'],
            bg=MODERN_COLORS['light'],
            fg=MODERN_COLORS['text_secondary']).pack(pady=(0, padding['small']))

    income_btn_row = create_standard_section(action_card, MODERN_COLORS['light'])
    income_btn_row.pack(fill=tk.X, pady=(0, padding['small']))

    edit_income_btn = create_modern_button(income_btn_row, "✏️ Edit",
                                         command=edit_income_selected,
                                         style='secondary', width=12)
    edit_income_btn.pack(side=tk.LEFT, padx=padding['small'])

    delete_income_btn = create_modern_button(income_btn_row, "🗑️ Delete",
                                           command=delete_income_selected,
                                           style='danger', width=12)
    delete_income_btn.pack(side=tk.LEFT, padx=padding['small'])

    # Expense management section - consistent styling
    tk.Label(action_card, text="💸 Manage Expenses",
            font=adaptive_fonts['subheading'],
            bg=MODERN_COLORS['light'],
            fg=MODERN_COLORS['text_primary']).pack(pady=(padding['element'], padding['small']))

    # Instruction label for expenses - consistent styling
    tk.Label(action_card, text="💡 Double-click an item to edit, or use buttons below",
            font=adaptive_fonts['small'],
            bg=MODERN_COLORS['light'],
            fg=MODERN_COLORS['text_secondary']).pack(pady=(0, padding['small']))

    expense_btn_row = create_standard_section(action_card, MODERN_COLORS['light'])
    expense_btn_row.pack(fill=tk.X, pady=(0, padding['element']))

    edit_expense_btn = create_modern_button(expense_btn_row, "✏️ Edit",
                                          command=edit_expense_selected,
                                          style='secondary', width=12)
    edit_expense_btn.pack(side=tk.LEFT, padx=padding['small'])

    delete_expense_btn = create_modern_button(expense_btn_row, "🗑️ Delete",
                                            command=delete_expense_selected,
                                            style='danger', width=12)
    delete_expense_btn.pack(side=tk.LEFT, padx=padding['small'])

    # Navigation button - consistent styling
    next_btn = create_modern_button(button_frame, "📈 View Summary",
                                  command=lambda:[save_data(current_date_str), inc.destroy(), 
                                                total_screen(day, year, month)],
                                  style='success', width=25)
    next_btn.pack(pady=padding['small'])

    # Sign out button - consistent styling
    signout_btn = create_modern_button(button_frame, "🚪 Sign Out",
                                      command=lambda:[inc.destroy(), login_screen()],
                                      style='danger', width=20)
    signout_btn.pack(pady=padding['small'])

    # Add global undo shortcut
    add_global_undo_shortcut(inc)

    inc.mainloop()

# ---------------- Expenses Screen (Edit/Delete + categories dropdown + Other) ----------------
def expenses_screen(day, year, month):
    # Add to navigation history
    add_to_history('expenses_screen', day, year, month)

    exp = tk.Tk()
    width, height = setup_adaptive_window(exp, "Expense Tracking - Money Rider")

    # Get adaptive fonts for consistent sizing
    adaptive_fonts = get_adaptive_fonts()

    expense_var = tk.StringVar()
    amount_var = tk.StringVar()

    # Store the current date
    current_date_str = f"{year}-{month:02d}-{day:02d}"

    # Main container with scrolling - centered
    main_container = create_scrollable_frame(exp, MODERN_COLORS['background'])
    padding = get_standard_padding()
    main_container.pack(fill=tk.BOTH, expand=True, padx=padding['element'], pady=padding['element'])

    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Configure scrolling properly
    def configure_scroll_region(event=None):
        main_container.canvas.configure(scrollregion=main_container.canvas.bbox("all"))

    scrollable_content.bind("<Configure>", configure_scroll_region)

    # Header section - centered
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(fill=tk.X, pady=(0, 30))

    # Title - centered
    title_label = tk.Label(header_frame, text="Expense Tracking",
                          font=adaptive_fonts['heading'],
                          bg=MODERN_COLORS['background'],
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, 10))

    # Date display - centered
    date_label = tk.Label(header_frame, text=f"{year}-{month:02d}-{day:02d}",
                         font=adaptive_fonts['body'],
                         bg=MODERN_COLORS['background'],
                         fg=MODERN_COLORS['text_primary'])
    date_label.pack()

    # Helper to show Add Expense popup with category dropdown + 'Other' option
    def add_option():
        popup = tk.Toplevel(exp)
        popup.title("Add New Expense")
        popup.geometry("450x400")
        popup.configure(bg=MODERN_COLORS['light'])
        popup.resizable(False, False)

        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (450 // 2)
        y = (popup.winfo_screenheight() // 2) - (400 // 2)
        popup.geometry(f"450x400+{x}+{y}")

        # Main container
        popup_container = create_modern_frame(popup, MODERN_COLORS['light'])
        popup_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title
        title_label = tk.Label(popup_container, text="Add New Expense",
                             font=adaptive_fonts['subheading'],
                             bg=MODERN_COLORS['light'],
                             fg=MODERN_COLORS['dark'])
        title_label.pack(pady=(0, 20))

        # Category selection
        tk.Label(popup_container, text="Category",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))

        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(popup_container, values=categories, textvariable=cat_var,
                               state="readonly", font=adaptive_fonts['body'])
        cat_menu.pack(fill=tk.X, pady=(0, 15))
        cat_menu.set(categories[0])

        # Custom category entry (hidden by default)
        custom_var = tk.StringVar()
        custom_entry = create_modern_entry(popup_container)
        custom_entry.config(textvariable=custom_var)

        # only show when Other selected
        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(fill=tk.X, pady=(0, 15))
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        # Amount field
        tk.Label(popup_container, text="Amount (₱)",
                font=adaptive_fonts['body'],
                bg=MODERN_COLORS['light'],
                fg=MODERN_COLORS['dark']).pack(anchor='w', pady=(10, 5))

        amount_entry = create_modern_entry(popup_container)
        amount_entry.config(textvariable=amount_var)
        amount_entry.pack(fill=tk.X, pady=(0, 20))

        def save_expense():
            category = cat_var.get()
            if category == "Other":
                category = custom_var.get().strip()
            amount = amount_var.get().strip()
            if not category or not amount:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            try:
                amount_val = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number")
                return

            entry = (category, amount_val)
            current_expenses.append(entry)
            # Format with modern styling
            listbox.insert(tk.END, f"{category:<30} ₱{amount_val:>10,.2f}")
            amount_var.set("")
            custom_var.set("")
            popup.destroy()
            save_data(current_date_str)

        # Save button
        save_btn = create_modern_button(popup_container, "Save Expense",
                                      command=save_expense,
                                      style='success', width=20)
        save_btn.pack(pady=10)

    # Display section
    display_frame = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    display_frame.configure(relief='solid', bd=1)

    # Header for the list
    list_header = create_modern_frame(display_frame, MODERN_COLORS['card'])
    list_header.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(list_header, text="Expense Category",
            font=adaptive_fonts['body'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, padx=10)

    tk.Label(list_header, text="Amount",
            font=adaptive_fonts['body'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.RIGHT, padx=10)

    # Instruction label
    instruction_frame = create_modern_frame(display_frame, MODERN_COLORS['card'])
    instruction_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

    tk.Label(instruction_frame, text="💡 Double-click an item to edit it",
            font=adaptive_fonts['small'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack()

    # Create a listbox with modern styling and double-click editing
    listbox = tk.Listbox(display_frame,
                        font=adaptive_fonts['body'],
                        bg=MODERN_COLORS['white'],
                        fg=MODERN_COLORS['dark'],
                        selectbackground=MODERN_COLORS['primary'],
                        selectforeground=MODERN_COLORS['white'],
                        relief='flat',
                        bd=0,
                        highlightthickness=0,
                        cursor='hand2')  # Show hand cursor to indicate clickable
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # Bind double-click to edit expense
    listbox.bind('<Double-Button-1>', lambda e: edit_selected())

    # Populate listbox with existing expenses
    for expense in current_expenses:
        listbox.insert(tk.END, f"{expense[0]:<30} ₱{expense[1]:>10,.2f}")

    # === EDIT MODE for expense ===
    def edit_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to edit")
            return
        idx = sel[0]
        old_desc, old_amount = current_expenses[idx]

        edit_win = tk.Toplevel(exp)
        edit_win.title("Edit Expense")
        edit_win.geometry("420x300")
        edit_win.configure(bg="#1C1C1C")

        tk.Label(edit_win, text="Category", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)
        # show combobox with categories and 'Other' as fallback
        cat_var = tk.StringVar()
        categories = ["Food", "Gas", "Maintenance", "Other"]
        cat_menu = ttk.Combobox(edit_win, values=categories, textvariable=cat_var, 
                               state="readonly", font=("Bubblegum Sans", 12))
        # if old_desc matches one of categories, select it; else select Other and show custom
        if old_desc in categories:
            cat_menu.set(old_desc)
        else:
            cat_menu.set("Other")
        cat_menu.pack(pady=5)

        custom_var = tk.StringVar()
        custom_entry = tk.Entry(edit_win, textvariable=custom_var, font=("Bubblegum Sans", 12))
        if cat_menu.get() == "Other":
            custom_var.set(old_desc)
            custom_entry.pack(pady=5)

        def on_cat_change(e=None):
            if cat_var.get() == "Other":
                custom_entry.pack(pady=5)
            else:
                custom_entry.pack_forget()
        cat_menu.bind("<<ComboboxSelected>>", on_cat_change)

        tk.Label(edit_win, text="Amount", bg="#1C1C1C", fg="white", font=("Bubblegum Sans", 12)).pack(pady=5)
        e_amount = tk.Entry(edit_win, font=("Bubblegum Sans", 12))
        e_amount.insert(0, str(old_amount))
        e_amount.pack(pady=5)

        def save_edit():
            if cat_menu.get() == "Other":
                new_desc = custom_var.get().strip()
            else:
                new_desc = cat_menu.get()
            new_amount_str = e_amount.get().strip()
            if not new_desc or not new_amount_str:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            try:
                new_amount = float(new_amount_str)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return
            current_expenses[idx] = (new_desc, new_amount)
            listbox.delete(0, tk.END)
            for expense in current_expenses:
                listbox.insert(tk.END, f"{expense[0].ljust(30)}{str(expense[1]).rjust(10)}")
            edit_win.destroy()
            save_data(current_date_str)

        save_btn = create_modern_button(edit_win, "💾 Save",
                                       command=save_edit,
                                       style='success', width=15)
        save_btn.pack(pady=10)

    # Delete selected expense with confirmation
    def delete_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Error", "No expense selected to delete")
            return
        idx = sel[0]
        expense = current_expenses[idx]

        # Show confirmation dialog
        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete this expense entry?\n\n"
                                   f"Category: {expense[0]}\n"
                                   f"Amount: ₱{expense[1]:,.2f}")

        if result:
            current_expenses.pop(idx)
            listbox.delete(idx)
            save_data(current_date_str)
            messagebox.showinfo("Success", "Expense entry deleted successfully!")

    # Button section
    button_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    button_frame.pack(fill=tk.X, pady=20)

    # Action buttons - centered
    action_frame = create_modern_frame(button_frame, MODERN_COLORS['background'])
    action_frame.pack(anchor='center')

    # Undo button (left side)
    undo_btn = create_undo_button(action_frame,
                                 command=lambda: [exp.destroy(), navigate_back()],
                                 style='warning', width=10)
    undo_btn.pack(side=tk.LEFT, padx=5)

    add_btn = create_modern_button(action_frame, "Add Expense",
                                 command=add_option,
                                 style='primary', width=15)
    add_btn.pack(side=tk.LEFT, padx=5)

    edit_btn = create_modern_button(action_frame, "Edit",
                                  command=edit_selected,
                                  style='secondary', width=10)
    edit_btn.pack(side=tk.LEFT, padx=5)

    delete_btn = create_modern_button(action_frame, "Delete",
                                    command=delete_selected,
                                    style='danger', width=10)
    delete_btn.pack(side=tk.LEFT, padx=5)

    # Navigation button
    nav_frame = create_modern_frame(button_frame, MODERN_COLORS['background'])
    nav_frame.pack(pady=15)

    next_btn = create_modern_button(nav_frame, "View Summary",
                                  command=lambda:[save_data(current_date_str), exp.destroy(), 
                                                total_screen(day, year, month)],
                                  style='success', width=20)
    next_btn.pack(pady=5)

    # Sign out button - mobile style
    signout_btn = create_modern_button(nav_frame, "🚪 Sign Out",
                                      command=lambda:[exp.destroy(), login_screen()],
                                      style='danger', width=20)
    signout_btn.pack(pady=5)

    # Add global undo shortcut
    add_global_undo_shortcut(exp)

    exp.mainloop()

# ---------------- Save data for the current date (per-user) ----------------
def save_data(date_str):
    global financial_data_manager, current_entries, current_expenses

    # compute totals from buffers and store into user's financial_data
    total_income = sum(float(entry[1]) for entry in current_entries) if current_entries else 0.0
    total_expenses = sum(float(expense[1]) for expense in current_expenses) if current_expenses else 0.0

    # Update new data structures
    transaction_date = datetime.fromisoformat(date_str)

    # Clear existing transactions for this date
    existing_transactions = financial_data_manager.get_transactions_by_date_range(transaction_date, transaction_date)
    for txn in existing_transactions:
        financial_data_manager.transactions.remove_by_id(txn.id)

    # Add income transactions
    for entry in current_entries:
        financial_data_manager.add_transaction(
            description=entry[0],
            amount=float(entry[1]),
            category="Income",
            transaction_type="income",
            date=transaction_date
        )

    # Add expense transactions
    for expense in current_expenses:
        financial_data_manager.add_transaction(
            description=expense[0],
            amount=float(expense[1]),
            category=expense[0],  # Use description as category
            transaction_type="expense",
            date=transaction_date
        )

    # ensure financial_data is a dict for the logged-in user (legacy format)
    financial_data[date_str] = {
        "income": total_income,
        "expenses": total_expenses,
        "entries": [[e[0], e[1]] for e in current_entries],
        "expense_entries": [[e[0], e[1]] for e in current_expenses]
    }

    # persist to current user's file
    if current_user:
        save_user_data(current_user)

# ---------------- Total Screen (keeps original layout) ----------------
def total_screen(day, year, month):
    # Add to navigation history
    add_to_history('total_screen', day, year, month)

    total = tk.Tk()
    width, height = setup_adaptive_window(total, "Financial Summary - Money Rider")

    # Get adaptive fonts for consistent sizing
    adaptive_fonts = get_adaptive_fonts()

    # Main container with mobile padding and scrolling
    main_container = create_scrollable_frame(total, MODERN_COLORS['background'])
    padding = get_standard_padding()
    main_container.pack(fill=tk.BOTH, expand=True, padx=padding['element'], pady=padding['element'])

    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Header section
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(pady=(0, 20))

    # Title - mobile style
    title_label = tk.Label(header_frame, text="Financial Summary",
                          font=adaptive_fonts['title'],
                          bg=MODERN_COLORS['background'],
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, 10))

    # Date display - mobile style
    date_str = f"{year}-{month:02d}-{day:02d}"
    date_label = tk.Label(header_frame, text=f"{date_str}",
                         font=adaptive_fonts['subheading'],
                         bg=MODERN_COLORS['background'],
                         fg=MODERN_COLORS['text_primary'])
    date_label.pack(pady=5)

    # Summary container - mobile card style
    summary_container = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    summary_container.pack(fill=tk.X, pady=20)
    summary_container.configure(relief='solid', bd=2)

    # Income section - mobile style
    income_frame = create_modern_frame(summary_container, MODERN_COLORS['card'])
    income_frame.pack(fill=tk.X, padx=25, pady=20)

    total_income = sum(float(i[1]) for i in current_entries) if current_entries else 0.0
    tk.Label(income_frame, text="Total Income:",
            font=adaptive_fonts['heading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT)
    tk.Label(income_frame, text=f"₱{total_income:,.2f}",
            font=adaptive_fonts['heading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['success']).pack(side=tk.RIGHT)

    # Expenses section - mobile style
    expenses_frame = create_modern_frame(summary_container, MODERN_COLORS['card'])
    expenses_frame.pack(fill=tk.X, padx=25, pady=20)

    total_expenses = sum(float(e[1]) for e in current_expenses) if current_expenses else 0.0
    tk.Label(expenses_frame, text="Total Expenses:",
            font=adaptive_fonts['heading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT)
    tk.Label(expenses_frame, text=f"₱{total_expenses:,.2f}",
            font=adaptive_fonts['heading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['danger']).pack(side=tk.RIGHT)

    # Net total section - mobile style
    net_frame = create_modern_frame(summary_container, MODERN_COLORS['card'])
    net_frame.pack(fill=tk.X, padx=25, pady=25)
    net_frame.configure(relief='solid', bd=3)

    day_total = total_income - total_expenses
    tk.Label(net_frame, text="Net Total:",
            font=adaptive_fonts['heading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['text_primary']).pack(side=tk.LEFT, padx=20, pady=15)
    tk.Label(net_frame, text=f"₱{day_total:,.2f}",
            font=adaptive_fonts['heading'],
            bg=MODERN_COLORS['card'],
            fg=MODERN_COLORS['success'] if day_total >= 0 else MODERN_COLORS['danger']
            ).pack(side=tk.RIGHT, padx=20, pady=15)

    # Navigation buttons - mobile style
    button_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    button_frame.pack(pady=30)

    # Undo button - mobile style
    undo_btn = create_undo_button(button_frame,
                                 command=lambda: [total.destroy(), navigate_back()],
                                 style='warning', width=15)
    undo_btn.pack(pady=10)

    # Back to expenses button - mobile style
    back_btn = create_modern_button(button_frame, "💸 Back to Expenses",
                                  command=lambda:[total.destroy(), expenses_screen(day, year, month)],
                                  style='secondary', width=20)
    back_btn.pack(pady=10)

    # Finish button - mobile style
    finish_btn = create_modern_button(button_frame, "✅ Finish & Return to Calendar",
                                    command=lambda:[total.destroy(), calendar_screen()],
                                    style='primary', width=25)
    finish_btn.pack(pady=10)

    # Sign out button - mobile style
    signout_btn = create_modern_button(button_frame, "🚪 Sign Out",
                                      command=lambda:[total.destroy(), login_screen()],
                                      style='danger', width=20)
    signout_btn.pack(pady=5)

    # Add global undo shortcut
    add_global_undo_shortcut(total)

    total.mainloop()

# ---------------- Advanced Analytics Screen ----------------

# ---------------- Charts and Visualizations Screen ----------------
def charts_screen():
    """Charts and visualizations screen with matplotlib graphs"""
    # Add to navigation history
    add_to_history('charts_screen')

    charts = tk.Tk()
    width, height = setup_adaptive_window(charts, "Charts & Visualizations - Money Rider")

    # Get adaptive fonts and padding for mobile
    adaptive_fonts = get_adaptive_fonts()
    adaptive_padding = get_adaptive_padding()

    # Main container with scrolling
    main_container = create_scrollable_frame(charts, MODERN_COLORS['background'])
    padding = get_standard_padding()
    main_container.pack(fill=tk.BOTH, expand=True, padx=padding['section'], pady=padding['section'])

    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Header section - Mobile optimized
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(fill=tk.X, pady=(0, adaptive_padding['large']))

    # Title - Mobile responsive
    title_label = tk.Label(header_frame, text="Charts & Visualizations",
                          font=adaptive_fonts['title'],
                          bg=MODERN_COLORS['background'],
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, adaptive_padding['medium']))

    subtitle = tk.Label(header_frame, text="Interactive financial data visualization",
                       font=adaptive_fonts['subheading'],
                       bg=MODERN_COLORS['background'],
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=adaptive_padding['small'])

    # Chart buttons section - Mobile optimized
    charts_section = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    charts_section.pack(fill=tk.X, pady=adaptive_padding['medium'])
    charts_section.configure(relief='solid', bd=1)

    charts_title = tk.Label(charts_section, text="📊 Available Charts",
                           font=adaptive_fonts['heading'],
                           bg=MODERN_COLORS['card'],
                           fg=MODERN_COLORS['text_primary'])
    charts_title.pack(pady=(adaptive_padding['large'], adaptive_padding['medium']), padx=adaptive_padding['large'])

    # Chart buttons - Mobile vertical stack
    charts_buttons_frame = create_modern_frame(charts_section, MODERN_COLORS['card'])
    charts_buttons_frame.pack(fill=tk.X, padx=adaptive_padding['large'], pady=(0, adaptive_padding['large']))

    def show_income_expense_chart():
        """Show income vs expense line chart"""
        try:
            fig = financial_analytics.create_income_expense_chart(30)
            show_chart_window(charts, "Income vs Expenses - 30 Days", fig)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart: {str(e)}")

    def show_category_pie_chart():
        """Show category distribution pie charts"""
        try:
            fig = financial_analytics.create_category_pie_chart()
            show_chart_window(charts, "Category Distribution", fig)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart: {str(e)}")

    def show_monthly_trend_chart():
        """Show monthly trend bar chart"""
        try:
            fig = financial_analytics.create_monthly_trend_chart(6)
            show_chart_window(charts, "Monthly Trends - 6 Months", fig)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart: {str(e)}")

    def show_spending_analysis_chart():
        """Show spending analysis chart"""
        try:
            fig = financial_analytics.create_spending_analysis_chart()
            show_chart_window(charts, "Spending Analysis", fig)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart: {str(e)}")

    # Chart buttons - Mobile vertical stack
    income_expense_btn = create_modern_button(charts_buttons_frame, "📈 Income vs Expenses",
                                            command=show_income_expense_chart, style='primary', width=25)
    income_expense_btn.pack(fill=tk.X, padx=adaptive_padding['small'], pady=adaptive_padding['small'])

    category_pie_btn = create_modern_button(charts_buttons_frame, "🥧 Category Distribution",
                                          command=show_category_pie_chart, style='success', width=25)
    category_pie_btn.pack(fill=tk.X, padx=adaptive_padding['small'], pady=adaptive_padding['small'])

    monthly_trend_btn = create_modern_button(charts_buttons_frame, "📊 Monthly Trends",
                                           command=show_monthly_trend_chart, style='info', width=25)
    monthly_trend_btn.pack(fill=tk.X, padx=adaptive_padding['small'], pady=adaptive_padding['small'])

    spending_analysis_btn = create_modern_button(charts_buttons_frame, "💰 Spending Analysis",
                                               command=show_spending_analysis_chart, style='warning', width=25)
    spending_analysis_btn.pack(fill=tk.X, padx=adaptive_padding['small'], pady=adaptive_padding['small'])

    # Navigation buttons - Mobile optimized
    nav_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    nav_frame.pack(pady=adaptive_padding['large'])

    # Back button - Mobile style
    back_btn = create_undo_button(nav_frame,
                                 command=lambda: [charts.destroy(), navigate_back()],
                                 style='warning', width=25)
    back_btn.pack(fill=tk.X, padx=adaptive_padding['medium'], pady=adaptive_padding['medium'])


    # Calendar button - Mobile style
    calendar_btn = create_modern_button(nav_frame, "📅 Back to Calendar",
                                      command=lambda: [charts.destroy(), calendar_screen()],
                                      style='secondary', width=25)
    calendar_btn.pack(fill=tk.X, padx=adaptive_padding['medium'], pady=adaptive_padding['small'])

    # Add global undo shortcut
    add_global_undo_shortcut(charts)

    charts.mainloop()

def show_chart_window(parent, title, figure):
    """Display a matplotlib chart in a new window"""
    chart_window = tk.Toplevel(parent)
    chart_window.title(title)
    chart_window.geometry("1000x700")
    chart_window.configure(bg=MODERN_COLORS['background'])
    chart_window.resizable(True, True)

    # Center the window
    chart_window.update_idletasks()
    x = (chart_window.winfo_screenwidth() // 2) - (1000 // 2)
    y = (chart_window.winfo_screenheight() // 2) - (700 // 2)
    chart_window.geometry(f"1000x700+{x}+{y}")

    # Create canvas for matplotlib
    canvas = FigureCanvasTkAgg(figure, chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add close button
    close_btn = create_modern_button(chart_window, "Close",
                                   command=chart_window.destroy,
                                   style='primary', width=15)
    close_btn.pack(pady=10)

    return chart_window

def create_result_window(parent, title, transactions, info_text=""):
    """Helper function to create result windows for algorithms"""
    result_window = tk.Toplevel(parent)
    result_window.title(title)
    result_window.geometry("600x500")
    result_window.configure(bg=MODERN_COLORS['light'])
    result_window.resizable(False, False)

    # Center the window
    result_window.update_idletasks()
    x = (result_window.winfo_screenwidth() // 2) - (600 // 2)
    y = (result_window.winfo_screenheight() // 2) - (500 // 2)
    result_window.geometry(f"600x500+{x}+{y}")

    # Main container
    result_container = create_modern_frame(result_window, MODERN_COLORS['light'])
    result_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Title
    title_label = tk.Label(result_container, text=title,
                          font=('Segoe UI', 16, 'bold'),
                          bg=MODERN_COLORS['light'],
                          fg=MODERN_COLORS['dark'])
    title_label.pack(pady=(0, 10))

    # Info text
    if info_text:
        info_label = tk.Label(result_container, text=info_text,
                             font=('Segoe UI', 10),
                             bg=MODERN_COLORS['light'],
                             fg=MODERN_COLORS['dark'])
        info_label.pack(pady=(0, 10))

    # Results listbox
    listbox = tk.Listbox(result_container,
                        font=('Courier New', 10),
                        bg=MODERN_COLORS['white'],
                        fg=MODERN_COLORS['dark'],
                        selectbackground=MODERN_COLORS['primary'],
                        selectforeground=MODERN_COLORS['white'],
                        relief='flat',
                        bd=1)
    listbox.pack(fill=tk.BOTH, expand=True, pady=10)

    # Add transactions to listbox
    for i, txn in enumerate(transactions, 1):
        listbox.insert(tk.END, f"{i:2d}. {txn.description:<30} ₱{txn.amount:>10,.2f} ({txn.transaction_type})")

    # Close button
    close_btn = create_modern_button(result_container, "Close",
                                   command=result_window.destroy,
                                   style='primary', width=15)
    close_btn.pack(pady=10)

    return result_window

# ---------------- Settings Screen ----------------
def settings_screen():
    """Settings screen with theme changer and other options - Mobile optimized"""
    # Add to navigation history
    add_to_history('settings_screen')

    settings = tk.Tk()
    width, height = setup_adaptive_window(settings, "Settings - Money Rider")

    # Get adaptive fonts and padding for mobile
    adaptive_fonts = get_adaptive_fonts()
    adaptive_padding = get_adaptive_padding()

    # Main container with scrolling
    main_container = create_scrollable_frame(settings, MODERN_COLORS['background'])
    padding = get_standard_padding()
    main_container.pack(fill=tk.BOTH, expand=True, padx=padding['section'], pady=padding['section'])

    # Get the scrollable frame for adding widgets
    scrollable_content = main_container.scrollable_frame

    # Header section - Mobile optimized
    header_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    header_frame.pack(fill=tk.X, pady=(0, adaptive_padding['large']))

    # Title - Mobile responsive
    title_label = tk.Label(header_frame, text="Settings",
                          font=adaptive_fonts['title'],
                          bg=MODERN_COLORS['background'],
                          fg=MODERN_COLORS['text_primary'])
    title_label.pack(pady=(0, adaptive_padding['medium']))

    subtitle = tk.Label(header_frame, text="Customize your Money Rider experience",
                       font=adaptive_fonts['subheading'],
                       bg=MODERN_COLORS['background'],
                       fg=MODERN_COLORS['text_secondary'])
    subtitle.pack(pady=adaptive_padding['small'])

    # Theme Selection Section - Mobile card style
    theme_section = create_modern_frame(scrollable_content, MODERN_COLORS['card'])
    theme_section.pack(fill=tk.X, pady=adaptive_padding['medium'])
    theme_section.configure(relief='solid', bd=1)

    theme_title = tk.Label(theme_section, text="🎨 Theme Selection",
                          font=adaptive_fonts['heading'],
                          bg=MODERN_COLORS['card'],
                          fg=MODERN_COLORS['text_primary'])
    theme_title.pack(pady=(adaptive_padding['large'], adaptive_padding['medium']), padx=adaptive_padding['large'])

    # Current theme display - Mobile style
    current_theme_label = tk.Label(theme_section, text=f"Current: {THEMES[CURRENT_THEME]['name']}",
                                  font=adaptive_fonts['body'],
                                  bg=MODERN_COLORS['card'],
                                  fg=MODERN_COLORS['text_primary'])
    current_theme_label.pack(pady=(0, adaptive_padding['large']), padx=adaptive_padding['large'])

    # Theme buttons - Mobile single column layout
    theme_buttons_frame = create_modern_frame(theme_section, MODERN_COLORS['card'])
    theme_buttons_frame.pack(fill=tk.X, padx=adaptive_padding['large'], pady=(0, adaptive_padding['large']))

    # Create theme buttons in single column for mobile
    theme_buttons = {}
    for i, (theme_key, theme_data) in enumerate(THEMES.items()):
        # Create theme preview button - Mobile optimized
        theme_btn = tk.Button(theme_buttons_frame,
                             text=f"{theme_data['name']} {'●' * 3}",
                             font=adaptive_fonts['body'],
                             bg=theme_data['primary'],
                             fg=theme_data['text_primary'],
                             relief='flat',
                             bd=2,
                             cursor='hand2',
                             height=2,  # Mobile-friendly height
                             command=lambda t=theme_key: apply_theme(t, settings, current_theme_label))

        # Add hover effect
        def create_theme_hover(btn, theme_key):
            def on_enter(e):
                btn.config(bg=THEMES[theme_key]['primary_dark'])
            def on_leave(e):
                btn.config(bg=THEMES[theme_key]['primary'])
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        create_theme_hover(theme_btn, theme_key)
        theme_btn.pack(fill=tk.X, padx=adaptive_padding['small'], pady=adaptive_padding['small'])
        theme_buttons[theme_key] = theme_btn


    # Navigation buttons - Mobile optimized
    nav_frame = create_modern_frame(scrollable_content, MODERN_COLORS['background'])
    nav_frame.pack(pady=adaptive_padding['large'])

    # Back button - Mobile style
    back_btn = create_undo_button(nav_frame,
                                 command=lambda: [settings.destroy(), navigate_back()],
                                 style='warning', width=25)
    back_btn.pack(fill=tk.X, padx=adaptive_padding['medium'], pady=adaptive_padding['medium'])

    # Calendar button - Mobile style
    calendar_btn = create_modern_button(nav_frame, "📅 Back to Calendar",
                                      command=lambda: [settings.destroy(), calendar_screen()],
                                      style='primary', width=25)
    calendar_btn.pack(fill=tk.X, padx=adaptive_padding['medium'], pady=adaptive_padding['small'])

    # Add global undo shortcut
    add_global_undo_shortcut(settings)

    settings.mainloop()

def apply_theme(theme_key, settings_window, current_theme_label):
    """Apply the selected theme and update the UI"""
    global CURRENT_THEME, MODERN_COLORS

    if change_theme(theme_key):
        # Save theme preference
        save_theme_preference(theme_key)

        # Update current theme label - Mobile friendly text
        current_theme_label.config(text=f"Current: {THEMES[theme_key]['name']}")

        # Show success message
        messagebox.showinfo("Theme Changed", f"Successfully changed to {THEMES[theme_key]['name']} theme!")

        # Note: In a real application, you would need to refresh all UI elements
        # For now, the user needs to restart the application to see the full theme change
        messagebox.showinfo("Restart Required",
                           "Theme changed! Please restart the application to see the full theme change.")
    else:
        messagebox.showerror("Error", "Failed to change theme!")


# ---------------- Start the app ----------------
if __name__ == "__main__":
    # Load theme preference on startup
    load_theme_preference()
    splash_screen()
