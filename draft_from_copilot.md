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
}

class Food {
  -UUID foodId
  -String name
  -Money price
  -FoodCategory category
  -float popularityRating
  +Food(name: String, price: Money, category: FoodCategory, popularityRating: float)
  +getId() UUID
  +getName() String
  +getPrice() Money
  +getCategory() FoodCategory
  +getPopularityRating() float
  +isValid() bool
}

class FoodCollection {
  -Map~UUID, Food~ foods
  +addFood(food: Food) void
  +removeFood(foodId: UUID) bool
  +getById(foodId: UUID) Food
  +listAll() List~Food~
  +filterByCategory(category: FoodCategory) List~Food~
  +searchByName(term: String) List~Food~
  +topRated(limit: int) List~Food~
}

class Transaction {
  -UUID transactionId
  -UUID userId
  -List~Food~ items
  -DateTime createdAt
  +Transaction(userId: UUID)
  +addItem(food: Food) void
  +removeItem(foodId: UUID) bool
  +getItems() List~Food~
  +calculateTotal() Money
  +isEmpty() bool
  +checkout() Receipt
}

class FoodCategory {
  <<enumeration>>
  BURGERS
  DRINKS
  DESSERTS
  SIDES
  OTHER
}

User "1" --> "0..*" Transaction : places
Transaction "1" o-- "1..*" Food : contains
FoodCollection "1" o-- "0..*" Food : manages
Food --> FoodCategory : categorized as