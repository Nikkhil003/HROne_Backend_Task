import os
import motor.motor_asyncio
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Establish a connection to the MongoDB database
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.hron_ecommerce