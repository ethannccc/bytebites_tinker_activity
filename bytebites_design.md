classDiagram
direction LR

class User {
  -UUID userId
  -String name
  -List~Transaction~ purchaseHistory
  +User(name: String)
  +getId() UUID
  +getName() String
  +updateName(name: String) void
  +addTransaction(tx: Transaction) void
  +getPurchaseHistory() List~Transaction~
  +hasPurchaseHistory() bool
  +isVerifiedUser() bool
}

class Food {
  -UUID foodId
  -String name
  -Decimal price
  -String category
  -float popularityRating
  +Food(name: String, price: Decimal, category: String, popularityRating: float)
  +getId() UUID
  +getName() String
  +getPrice() Decimal
  +getCategory() String
  +getPopularityRating() float
  +isValid() bool
}

class FoodCollection {
  -Map~UUID, Food~ foods
  +addFood(food: Food) void
  +removeFood(foodId: UUID) bool
  +getById(foodId: UUID) Food
  +listAll() List~Food~
  +filterByCategory(category: String) List~Food~
  +searchByName(term: String) List~Food~
  +topRated(limit: int) List~Food~
}

class Transaction {
  -UUID transactionId
  -UUID userId
  -List~Food~ items
  -DateTime createdAt
  -TransactionStatus status
  +Transaction(userId: UUID)
  +addItem(food: Food) void
  +removeItem(foodId: UUID) bool
  +getItems() List~Food~
  +calculateTotal() Decimal
  +isEmpty() bool
  +checkout() bool
}

User "1" --> "0..*" Transaction : places
Transaction "1" o-- "0..*" Food : contains
FoodCollection "1" o-- "0..*" Food : manages

note for User "Security: validate/sanitize name input; return defensive copy of purchase history"
note for Food "Validation: price >= 0, popularityRating in [0,5], category from allowed set"
note for FoodCollection "Scalability: Map index for O(1) lookup by id; filter/search are read-only"
note for Transaction "Integrity: server-side total calculation; status transition guards at checkout"