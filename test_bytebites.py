from decimal import Decimal

import pytest

from models import Food, FoodCollection, Transaction, TransactionStatus, User


def test_user_name_is_trimmed_and_verified_after_purchase_history_update():
	user = User("  Alice  ")
	assert user.get_name() == "Alice"
	assert user.has_purchase_history() is False
	assert user.is_verified_user() is False

	user.add_transaction(object())
	assert user.has_purchase_history() is True
	assert user.is_verified_user() is True


def test_user_rejects_invalid_names():
	with pytest.raises(ValueError):
		User("   ")

	user = User("Bob")
	with pytest.raises(TypeError):
		user.update_name(123)


def test_food_valid_construction_and_fields():
	food = Food("Spicy Burger", "12.99", "burgers", 4.5)
	assert food.get_name() == "Spicy Burger"
	assert food.get_price() == Decimal("12.99")
	assert food.get_category() == "Burgers"
	assert food.get_popularity_rating() == 4.5
	assert food.is_valid() is True


def test_food_rejects_invalid_values():
	with pytest.raises(ValueError):
		Food("Soda", "-1.00", "Drinks", 3.0)

	with pytest.raises(ValueError):
		Food("Soda", "2.00", "Unknown", 3.0)

	with pytest.raises(ValueError):
		Food("Soda", "2.00", "Drinks", 6.0)


def test_food_collection_add_get_filter_search_and_remove():
	collection = FoodCollection()
	burger = Food("Spicy Burger", "10.00", "Burgers", 4.7)
	soda = Food("Large Soda", "2.50", "Drinks", 4.1)

	collection.add_food(burger)
	collection.add_food(soda)

	assert collection.get_by_id(burger.get_id()) == burger
	assert len(collection.list_all()) == 2
	assert collection.filter_by_category("drinks") == [soda]
	assert collection.search_by_name("burger") == [burger]

	assert collection.remove_food(burger.get_id()) is True
	assert collection.get_by_id(burger.get_id()) is None
	assert collection.remove_food(burger.get_id()) is False


def test_food_collection_top_rated_orders_descending_then_name():
	collection = FoodCollection()
	a = Food("Alpha", "5.00", "Sides", 4.8)
	b = Food("Beta", "6.00", "Sides", 4.8)
	c = Food("Gamma", "7.00", "Sides", 4.2)
	collection.add_food(c)
	collection.add_food(b)
	collection.add_food(a)

	top_two = collection.top_rated(2)
	assert [item.get_name() for item in top_two] == ["Alpha", "Beta"]


def test_transaction_total_checkout_and_post_checkout_guard():
	user = User("Charlie")
	tx = Transaction(user.get_id())
	burger = Food("Spicy Burger", "10.00", "Burgers", 4.7)
	soda = Food("Large Soda", "2.50", "Drinks", 4.1)

	assert tx.is_empty() is True
	tx.add_item(burger)
	tx.add_item(soda)
	assert tx.is_empty() is False
	assert tx.calculate_total() == Decimal("12.50")

	assert tx.checkout() is True
	assert tx.checkout() is False
	assert tx.remove_item(burger.get_id()) is False
	with pytest.raises(ValueError):
		tx.add_item(burger)


def test_transaction_rejects_invalid_constructor_and_item_type():
	with pytest.raises(TypeError):
		Transaction("not-a-uuid")

	user = User("Dana")
	tx = Transaction(user.get_id())
	with pytest.raises(TypeError):
		tx.add_item("not-food")


def test_checkout_empty_transaction_fails_and_status_stays_pending():
	user = User("Evan")
	tx = Transaction(user.get_id())
	assert tx.checkout() is False
	assert tx._status == TransactionStatus.PENDING

