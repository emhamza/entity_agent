from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["productcetalog"]
collection = db["products"]

product_id_str = "684e5bff8a341cd5f0d4cd17"

product_id_obj = ObjectId(product_id_str)

product_data = collection.find_one({"_id": product_id_obj})

# product_data = list(collection.find({}))

# if product_data:
#     print("Document found:")
#     print(product_data)
# else:
#     print(f"Document not found with product _id: {product_id_str}")

client.close()
