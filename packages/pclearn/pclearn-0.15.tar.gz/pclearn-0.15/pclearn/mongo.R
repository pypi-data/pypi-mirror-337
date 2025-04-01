# Create and Use Database
use Library  
# Create Collection and Insert Multiple Documents  
db.books.insertMany([
  { ISBNNO: 10101, Title: "MongoDB Basics", Publisher: "Pearsons", Author: "John Doe", Category: "Database", Price: 1200 },])
# List Selected Fields (Title, ISBN, Author)  
db.books.find({}, { Title: 1, ISBNNO: 1, Author: 1, _id: 0 })  
# Find Books with Price Greater Than 1500  
db.books.find({ Price: { $gt: 1500 } })  
# Remove a Book by ISBN  
db.books.deleteOne({ ISBNNO: 10201 })  
# Find Books Published by "Pearsons"  
db.books.find({ Publisher: "Pearsons" })  
# Find Books of a Specific Category (Database)  
db.books.find({ Category: "Database" })  
# Find Books by a Specific Author ("John Doe")  
db.books.find({ Author: "John Doe" })  
# Update Price of a Book by ISBN  
db.books.updateOne({ ISBNNO: 10301 }, { $set: { Price: 2000 } })  
# Count Total Books in Collection  
db.books.countDocuments()  
# Sort Books by Price in Descending Order  
db.books.find().sort({ Price: -1 })  
# Find the Most Expensive Book  
db.books.find().sort({ Price: -1 }).limit(1)  
# Find Books with Price Between 1000 and 2000  
db.books.find({ Price: { $gte: 1000, $lte: 2000 } })  
# Add a New Field "Stock" to All Books  
db.books.updateMany({}, { $set: { Stock: 50 } })  
# Remove All Books in the "AI" Category  
db.books.deleteMany({ Category: "AI" })  
# Find Books Where Title Contains "MongoDB"  
db.books.find({ Title: /MongoDB/ })  
# Find Books Published After a Specific Year (e.g., 2020)  
db.books.find({ Year: { $gt: 2020 } })  
# Find Books with Price Less Than 1000  
db.books.find({ Price: { $lt: 1000 } })  
# Find the Cheapest Book  
db.books.find().sort({ Price: 1 }).limit(1)  
# Update Publisher Name by ISBN  
db.books.updateOne({ ISBNNO: 10501 }, { $set: { Publisher: "MCC" } })  
# Remove Books with Price Above 5000  
db.books.deleteMany({ Price: { $gt: 5000 } })  
# Group Books by Category and Count  
db.books.aggregate([
  { $group: { _id: "$Category", count: { $sum: 1 } } }])  
# Get a List of Distinct Publishers  
db.books.distinct("Publisher")  
# Check if a Book Exists by ISBN  
db.books.findOne({ ISBNNO: 10301 })  
# Find Books with Price Greater Than the Average Price  
db.books.aggregate([
  { $group: { _id: null, avgPrice: { $avg: "$Price" } } },
  { $match: { Price: { $gt: "$avgPrice" } } }])  
# Find Books Not Belonging to a Specific Category (e.g., Cloud)  
db.books.find({ Category: { $ne: "Cloud" } })  
