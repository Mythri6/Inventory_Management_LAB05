"""Inventory Management System
Author: Myth (2025)
Description: A clean, type-safe, and fully logged inventory manager.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class Inventory:
    """A classy inventory management system."""

    def __init__(self, file: str = "inventory.json") -> None:
        self.file: Path = Path(file)
        self.stock_data: Dict[str, int] = {}
        self.logs: List[str] = []
        self.load_data()

    def _log(self, message: str) -> None:
        """Add a timestamped log entry and print it."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} - {message}"
        self.logs.append(entry)
        print(entry)

    def _validate_item(self, item: str) -> bool:
        """Validate that an item name is a non-empty string."""
        if not isinstance(item, str) or not item.strip():
            self._log(f"Invalid item name: {item!r}")
            return False
        return True

    def _validate_qty(self, qty: int) -> bool:
        """Validate that a quantity is a positive integer."""
        if not isinstance(qty, int) or qty <= 0:
            self._log(f"Invalid quantity: {qty!r}. Must be a positive integer.")
            return False
        return True

    def add_item(self, item: str, qty: int) -> None:
        """Add quantity of an item to the inventory."""
        if not (self._validate_item(item) and self._validate_qty(qty)):
            return
        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        self._log(f"Added {qty} of '{item}'. Total: {self.stock_data[item]}")

    def remove_item(self, item: str, qty: int) -> None:
        """Remove quantity of an item from inventory."""
        if not (self._validate_item(item) and self._validate_qty(qty)):
            return
        if item not in self.stock_data:
            self._log(f"Item '{item}' not found in inventory.")
            return
        self.stock_data[item] -= qty
        if self.stock_data[item] <= 0:
            del self.stock_data[item]
            self._log(f"'{item}' removed from inventory (out of stock).")
        else:
            self._log(f"Removed {qty} of '{item}'. Remaining: {self.stock_data[item]}")

    def get_qty(self, item: str) -> int:
        """Return the quantity of an item."""
        return self.stock_data.get(item, 0)

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """Return items with quantity below a given threshold."""
        low_items = [item for item, qty in self.stock_data.items() if qty < threshold]
        if low_items:
            self._log(f"Low stock items: {', '.join(low_items)}")
        else:
            self._log("No low-stock items detected.")
        return low_items

    def print_data(self) -> None:
        """Print a formatted inventory report."""
        print("\n--- Inventory Report ---")
        if not self.stock_data:
            print("No items in stock.")
            return
        for item, qty in sorted(self.stock_data.items()):
            print(f"{item}: {qty}")

    def save_data(self) -> None:
        """Save stock data to a JSON file."""
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.stock_data, f, indent=4, sort_keys=True)
            self._log(f"Inventory saved to {self.file}")
        except (OSError, json.JSONDecodeError) as exc:
            self._log(f"Error saving inventory: {exc}")

    def load_data(self) -> None:
        """Load stock data from a JSON file."""
        if not self.file.exists():
            self._log("No inventory file found. Starting fresh.")
            return
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                self.stock_data = json.load(f)
            self._log(f"Loaded inventory from {self.file}")
        except (OSError, json.JSONDecodeError) as exc:
            self._log(f"Error loading file: {exc}")

    def __enter__(self) -> "Inventory":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit context manager and auto-save."""
        self.save_data()
        if exc_value:
            self._log(f"Error occurred: {exc_value}")


def main() -> None:
    """Run demo inventory operations."""
    with Inventory() as inv:
        inv.add_item("apple", 10)
        inv.add_item("banana", 5)
        inv.add_item("pear", 2)
        inv.remove_item("apple", 3)
        inv.remove_item("orange", 1)
        print(f"\nApple stock: {inv.get_qty('apple')}")
        inv.check_low_items()
        inv.print_data()


if __name__ == "__main__":
    main()
