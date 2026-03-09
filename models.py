from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from uuid import UUID, uuid4

# Allowed food categories
ALLOWED_CATEGORIES = {"Burgers", "Drinks", "Desserts", "Sides", "Other"}


class User:
	# Represents a customer profile and stores prior transactions for verification/history.
	# Private fields: _user_id (UUID), _name (str), _purchase_history (list[Transaction])
	
	def __init__(self, name: str) -> None:
		"""Initialize a new user with a given name (validated and sanitized)."""
		self._user_id: UUID = uuid4()
		self._name: str = self._validate_name(name)
		self._purchase_history: list = []

	@staticmethod
	def _validate_name(name: str) -> str:
		"""Validate and sanitize name: non-empty, trimmed."""
		if not isinstance(name, str):
			raise TypeError("Name must be a string.")
		normalized_name = name.strip()
		if not normalized_name:
			raise ValueError("Name cannot be empty or whitespace only.")
		return normalized_name

	def get_id(self):
		"""Return this user's unique ID (UUID)."""
		return self._user_id

	def get_name(self) -> str:
		"""Return this user's name."""
		return self._name

	def update_name(self, name: str) -> None:
		"""Update user name after validation and sanitization."""
		self._name = self._validate_name(name)

	def add_transaction(self, tx) -> None:
		"""Attach a completed transaction to this user's purchase history."""
		if tx is None:
			raise ValueError("Transaction cannot be None.")
		# Optionally verify transaction belongs to this user if tx has user_id attribute
		if hasattr(tx, "_user_id") and tx._user_id != self._user_id:
			raise ValueError("Transaction does not belong to this user.")
		self._purchase_history.append(tx)

	def get_purchase_history(self) -> list:
		"""Return a defensive copy of the purchase history list."""
		return list(self._purchase_history)

	def has_purchase_history(self) -> bool:
		"""Return True if user has any purchase history."""
		return len(self._purchase_history) > 0

	def is_verified_user(self) -> bool:
		"""Return True if user is verified (e.g., has at least one purchase)."""
		return self.has_purchase_history()


class TransactionStatus(str, Enum):
	"""Enumeration for transaction lifecycle states."""
	PENDING = "PENDING"
	CHECKED_OUT = "CHECKED_OUT"


class Food:
	# Represents a food item with name, price, category, and popularity rating.
	# Private fields: _food_id (UUID), _name (str), _price (Decimal), _category (str), _popularity_rating (float)
	
	def __init__(self, name: str, price, category: str, popularity_rating: float) -> None:
		"""Initialize a new food item with validated name, price (Decimal), category, and popularity rating (0-5)."""
		self._food_id: UUID = uuid4()
		self._name: str = self._validate_name(name)
		self._price: Decimal = self._validate_price(price)
		self._category: str = self._validate_category(category)
		self._popularity_rating: float = self._validate_popularity(popularity_rating)

	@staticmethod
	def _validate_name(name: str) -> str:
		"""Validate name: non-empty, trimmed string."""
		if not isinstance(name, str):
			raise TypeError("Name must be a string.")
		normalized_name = name.strip()
		if not normalized_name:
			raise ValueError("Name cannot be empty or whitespace only.")
		return normalized_name

	@staticmethod
	def _validate_price(price) -> Decimal:
		"""Validate price: convert to Decimal and ensure non-negative."""
		try:
			decimal_price = Decimal(str(price))
		except (InvalidOperation, ValueError, TypeError) as e:
			raise ValueError("Price must be a valid decimal number.") from e
		if decimal_price < 0:
			raise ValueError("Price cannot be negative.")
		return decimal_price

	@staticmethod
	def _validate_category(category: str) -> str:
		"""Validate category: must be in ALLOWED_CATEGORIES set."""
		if not isinstance(category, str):
			raise TypeError("Category must be a string.")
		normalized_category = category.strip().title()
		if normalized_category not in ALLOWED_CATEGORIES:
			raise ValueError(f"Category must be one of: {sorted(ALLOWED_CATEGORIES)}.")
		return normalized_category

	@staticmethod
	def _validate_popularity(rating: float) -> float:
		"""Validate popularity rating: must be a float between 0 and 5 inclusive."""
		try:
			float_rating = float(rating)
		except (TypeError, ValueError) as e:
			raise ValueError("Popularity rating must be a number.") from e
		if float_rating < 0 or float_rating > 5:
			raise ValueError("Popularity rating must be between 0 and 5.")
		return float_rating

	def get_id(self):
		"""Return this food item's unique ID (UUID)."""
		return self._food_id

	def get_name(self) -> str:
		"""Return this food item's name."""
		return self._name

	def get_price(self):
		"""Return this food item's price (Decimal, non-negative)."""
		return self._price

	def get_category(self) -> str:
		"""Return this food item's category (from allowed set)."""
		return self._category

	def get_popularity_rating(self) -> float:
		"""Return this food item's popularity rating (0-5)."""
		return self._popularity_rating

	def is_valid(self) -> bool:
		"""Return True if all fields satisfy validation rules: non-empty name, price>=0, valid category, rating in [0,5]."""
		return (
			bool(self._name)
			and self._price >= 0
			and self._category in ALLOWED_CATEGORIES
			and 0 <= self._popularity_rating <= 5
		)


class FoodCollection:
	# Manages the full catalog of food items and supports category-based filtering.
	# Private field: _foods (dict mapping UUID → Food)
	# Design note: O(1) lookup by ID; filter/search/top_rated are read-only operations.
	
	def __init__(self) -> None:
		"""Initialize an empty food collection with index-based storage."""
		self._foods: dict[UUID, Food] = {}

	def add_food(self, food) -> None:
		"""Insert or replace a food item into the catalog by its ID."""
		if not isinstance(food, Food):
			raise TypeError("food must be an instance of Food.")
		self._foods[food.get_id()] = food

	def remove_food(self, food_id) -> bool:
		"""Remove a food item by ID; return True if removed, False otherwise."""
		if not isinstance(food_id, UUID):
			raise TypeError("food_id must be a UUID.")
		return self._foods.pop(food_id, None) is not None

	def get_by_id(self, food_id):
		"""Fetch a food item by ID; return None if not found."""
		if not isinstance(food_id, UUID):
			raise TypeError("food_id must be a UUID.")
		return self._foods.get(food_id)

	def list_all(self) -> list:
		"""Return all items currently in the catalog."""
		return list(self._foods.values())

	def filter_by_category(self, category: str) -> list:
		"""Return all foods matching the given category (case-insensitive)."""
		if not isinstance(category, str):
			raise TypeError("category must be a string.")
		normalized_category = category.strip().title()
		return [food for food in self._foods.values() if food.get_category() == normalized_category]

	def search_by_name(self, term: str) -> list:
		"""Return foods whose name contains the search term (case-insensitive)."""
		if not isinstance(term, str):
			raise TypeError("term must be a string.")
		normalized_term = term.strip().lower()
		if not normalized_term:
			return []
		return [food for food in self._foods.values() if normalized_term in food.get_name().lower()]

	def top_rated(self, limit: int) -> list:
		"""Return the top 'limit' highest-rated foods, sorted by popularity descending."""
		if not isinstance(limit, int) or limit < 0:
			raise ValueError("limit must be a non-negative integer.")
		if limit == 0:
			return []
		# Sort by popularity rating descending, then by name for stability
		sorted_foods = sorted(
			self._foods.values(),
			key=lambda food: (-food.get_popularity_rating(), food.get_name().lower())
		)
		return sorted_foods[:limit]


class Transaction:
	# Groups selected Food items for one purchase and computes the total cost.
	# Private fields: _transaction_id (UUID), _user_id (UUID), _items (list[Food]), _created_at (datetime), _status (TransactionStatus)
	# Design note: Server-side total calculation; checkout enforces status transition guards.
	
	def __init__(self, user_id) -> None:
		"""Initialize a new transaction for a given user (UUID); status starts as PENDING."""
		if not isinstance(user_id, UUID):
			raise TypeError("user_id must be a UUID.")
		self._transaction_id: UUID = uuid4()
		self._user_id: UUID = user_id
		self._items: list[Food] = []
		self._created_at: datetime = datetime.utcnow()
		self._status: TransactionStatus = TransactionStatus.PENDING

	def add_item(self, food) -> None:
		"""Add a food item to this transaction (only if status is PENDING)."""
		if self._status != TransactionStatus.PENDING:
			raise ValueError("Cannot add item: transaction has already been checked out.")
		if not isinstance(food, Food):
			raise TypeError("food must be an instance of Food.")
		self._items.append(food)

	def remove_item(self, food_id) -> bool:
		"""Remove a food item by ID; return True if removed, False otherwise (only if status is PENDING)."""
		if self._status != TransactionStatus.PENDING:
			return False
		if not isinstance(food_id, UUID):
			raise TypeError("food_id must be a UUID.")
		for index, item in enumerate(self._items):
			if item.get_id() == food_id:
				del self._items[index]
				return True
		return False

	def get_items(self) -> list:
		"""Return a defensive copy of current transaction items."""
		return list(self._items)

	def calculate_total(self):
		"""Compute the total cost (Decimal) using server-side sum of current item prices."""
		return sum((item.get_price() for item in self._items), Decimal("0"))

	def is_empty(self) -> bool:
		"""Return True if this transaction has no items."""
		return len(self._items) == 0

	def checkout(self) -> bool:
		"""Finalize transaction and transition status to CHECKED_OUT if valid; return True if successful."""
		if self._status != TransactionStatus.PENDING:
			return False
		if self.is_empty():
			return False
		self._status = TransactionStatus.CHECKED_OUT
		return True
