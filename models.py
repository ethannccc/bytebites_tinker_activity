class User:
	# Represents a customer profile and stores prior transactions for verification/history.
	# Private fields: _user_id (UUID), _name (str), _purchase_history (list[Transaction])
	
	def __init__(self, name: str) -> None:
		"""Initialize a new user with a given name (validated and sanitized)."""
		raise NotImplementedError

	def get_id(self):
		"""Return this user's unique ID (UUID)."""
		raise NotImplementedError

	def get_name(self) -> str:
		"""Return this user's name."""
		raise NotImplementedError

	def update_name(self, name: str) -> None:
		"""Update user name after validation and sanitization."""
		raise NotImplementedError

	def add_transaction(self, tx) -> None:
		"""Attach a completed transaction to this user's purchase history."""
		raise NotImplementedError

	def get_purchase_history(self) -> list:
		"""Return a defensive copy of the purchase history list."""
		raise NotImplementedError

	def has_purchase_history(self) -> bool:
		"""Return True if user has any purchase history."""
		raise NotImplementedError

	def is_verified_user(self) -> bool:
		"""Return True if user is verified (e.g., has at least one purchase)."""
		raise NotImplementedError

class Food:
	# Represents a food item with name, price, category, and popularity rating.
	# Private fields: _food_id (UUID), _name (str), _price (Decimal), _category (str), _popularity_rating (float)
	
	def __init__(self, name: str, price, category: str, popularity_rating: float) -> None:
		"""Initialize a new food item with validated name, price (Decimal), category, and popularity rating (0-5)."""
		raise NotImplementedError

	def get_id(self):
		"""Return this food item's unique ID (UUID)."""
		raise NotImplementedError

	def get_name(self) -> str:
		"""Return this food item's name."""
		raise NotImplementedError

	def get_price(self):
		"""Return this food item's price (Decimal, non-negative)."""
		raise NotImplementedError

	def get_category(self) -> str:
		"""Return this food item's category (from allowed set)."""
		raise NotImplementedError

	def get_popularity_rating(self) -> float:
		"""Return this food item's popularity rating (0-5)."""
		raise NotImplementedError

	def is_valid(self) -> bool:
		"""Return True if all fields satisfy validation rules: non-empty name, price>=0, valid category, rating in [0,5]."""
		raise NotImplementedError


class FoodCollection:
	# Manages the full catalog of food items and supports category-based filtering.
	# Private field: _foods (dict mapping UUID → Food)
	# Design note: O(1) lookup by ID; filter/search/top_rated are read-only operations.
	
	def __init__(self) -> None:
		"""Initialize an empty food collection with index-based storage."""
		raise NotImplementedError

	def add_food(self, food) -> None:
		"""Insert or replace a food item into the catalog by its ID."""
		raise NotImplementedError

	def remove_food(self, food_id) -> bool:
		"""Remove a food item by ID; return True if removed, False otherwise."""
		raise NotImplementedError

	def get_by_id(self, food_id):
		"""Fetch a food item by ID; return None if not found."""
		raise NotImplementedError

	def list_all(self) -> list:
		"""Return all items currently in the catalog."""
		raise NotImplementedError

	def filter_by_category(self, category: str) -> list:
		"""Return all foods matching the given category (case-insensitive)."""
		raise NotImplementedError

	def search_by_name(self, term: str) -> list:
		"""Return foods whose name contains the search term (case-insensitive)."""
		raise NotImplementedError

	def top_rated(self, limit: int) -> list:
		"""Return the top 'limit' highest-rated foods, sorted by popularity descending."""
		raise NotImplementedError


class Transaction:
	# Groups selected Food items for one purchase and computes the total cost.
	# Private fields: _transaction_id (UUID), _user_id (UUID), _items (list[Food]), _created_at (datetime), _status (TransactionStatus)
	# Design note: Server-side total calculation; checkout enforces status transition guards.
	
	def __init__(self, user_id) -> None:
		"""Initialize a new transaction for a given user (UUID); status starts as PENDING."""
		raise NotImplementedError

	def add_item(self, food) -> None:
		"""Add a food item to this transaction (only if status is PENDING)."""
		raise NotImplementedError

	def remove_item(self, food_id) -> bool:
		"""Remove a food item by ID; return True if removed, False otherwise (only if status is PENDING)."""
		raise NotImplementedError

	def get_items(self) -> list:
		"""Return a defensive copy of current transaction items."""
		raise NotImplementedError

	def calculate_total(self):
		"""Compute the total cost (Decimal) using server-side sum of current item prices."""
		raise NotImplementedError

	def is_empty(self) -> bool:
		"""Return True if this transaction has no items."""
		raise NotImplementedError

	def checkout(self) -> bool:
		"""Finalize transaction and transition status to CHECKED_OUT if valid; return True if successful."""
		raise NotImplementedError
