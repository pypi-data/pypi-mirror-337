import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
from datetime import datetime
from decimal import Decimal


class DynamoDBService:
    """A class to handle all interactions with DynamoDB for an e-commerce system."""

    def __init__(self, region_name="us-east-1", s3_bucket="ecommerce-11032025"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.s3_bucket = s3_bucket  # ✅ Fix: Define s3_bucket properly

        # ✅ Define tables
        self.customer_table = self.dynamodb.Table("Customer")
        self.product_table = self.dynamodb.Table("Product")
        self.order_table = self.dynamodb.Table("Order")
        self.order_item_table = self.dynamodb.Table("OrderItem")
        self.shipping_table = self.dynamodb.Table("ShippingAddress")

    def create_customer(self, name, email):
        """Creates a new customer in DynamoDB if they do not already exist."""
        try:
            # ✅ Use scan() instead of get_item() to check if email exists
            existing_customer = self.customer_table.scan(
                FilterExpression=Attr("email").eq(email)
            ).get("Items", [])
    
            if existing_customer:
                print(f"⚠️ Customer with email {email} already exists.")
                return existing_customer[0]["customer_id"]
    
            # ✅ Generate a new unique customer_id
            customer_id = str(uuid.uuid4())
    
            # ✅ Insert new customer into the table
            self.customer_table.put_item(
                Item={
                    "customer_id": customer_id,  # Primary Key
                    "name": name,
                    "email": email
                }
            )
            print(f"✅ Customer {name} ({email}) stored in DynamoDB.")
            return customer_id
    
        except Exception as e:
            print(f"❌ Error storing customer in DynamoDB: {e}")
            return None


    def get_customer(self, customer_id):
        """Retrieves a customer by their ID from the DynamoDB table."""
        try:
            response = self.customer_table.get_item(Key={"customer_id": customer_id})
            customer = response.get("Item")

            if not customer:
                print(f"⚠️ No customer found with ID {customer_id}")
                return None

            return customer

        except Exception as e:
            print(f"❌ Error retrieving customer from DynamoDB: {e}")
            return None
            
            
    def create_product(self, name, price, digital, image_url=None):
        """Creates a new product in the DynamoDB Product table."""
        product_id = str(uuid.uuid4())

        try:
            self.product_table.put_item(
                Item={
                    "product_id": product_id,
                    "name": name,
                    "price": Decimal(str(price)),  # Convert price to Decimal for DynamoDB
                    "digital": digital,
                    "image": image_url
                }
            )
            print(f"✅ Product '{name}' created successfully with ID: {product_id}")
            return product_id

        except Exception as e:
            print(f"❌ Error creating product in DynamoDB: {e}")
            return None


    def get_product(self, product_id):
        """Retrieves a product from the DynamoDB Product table by product_id."""
        try:
            response = self.product_table.get_item(Key={"product_id": product_id})
            product = response.get("Item")

            if product:
                print(f"✅ Product found: {product}")
                return product
            else:
                print(f"⚠️ Product with ID {product_id} not found.")
                return None

        except Exception as e:
            print(f"❌ Error retrieving product: {e}")
            return None


    def update_product(self, product_id, name=None, price=None, digital=None, image_url=None):
        """
        Updates an existing product in the DynamoDB Product table.
        """
        update_expr = []
        expr_attr_vals = {}
        expr_attr_names = {}
    
        if name is not None:
            update_expr.append("#n = :n")
            expr_attr_vals[":n"] = name
            expr_attr_names["#n"] = "name"  
    
        if price is not None:
            update_expr.append("price = :p")
            expr_attr_vals[":p"] = Decimal(str(price))
    
        if digital is not None:
            update_expr.append("digital = :d")
            expr_attr_vals[":d"] = digital
    
        if image_url is not None:
            update_expr.append("image = :img")
            expr_attr_vals[":img"] = image_url
    
        if not update_expr:
            print("⚠️ No fields provided to update.")
            return None
    
        update_expr_str = "SET " + ", ".join(update_expr)
    
        try:
            response = self.product_table.update_item(
                Key={"product_id": product_id},
                UpdateExpression=update_expr_str,
                ExpressionAttributeValues=expr_attr_vals,
                ExpressionAttributeNames=expr_attr_names if expr_attr_names else None,
                ReturnValues="ALL_NEW"
            )
    
            updated_item = response.get("Attributes")
            
            if updated_item is None:
                print(f"⚠️ Warning: No attributes returned for product {product_id}. Check if the item exists.")
                return None
            
            print(f"✅ Product {product_id} updated successfully.")
            return updated_item
    
        except Exception as e:
            print(f"❌ Error updating product: {e}")
            return None
    


    def delete_product(self, product_id):
        """
        Deletes a product from the DynamoDB Product table.
        """
        try:
            response = self.product_table.delete_item(
                Key={"product_id": product_id}
            )
            print(f"✅ Product {product_id} deleted successfully.")
            return response

        except Exception as e:
            print(f"❌ Error deleting product: {e}")
            return None


    def create_order(self, customer_id):
        """
        Creates a new order for a customer in DynamoDB.
        """
        order_id = str(uuid.uuid4())

        try:
            self.order_table.put_item(
                Item={
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "date_ordered": datetime.utcnow().isoformat(),
                    "complete": False,
                    "transaction_id": str(uuid.uuid4()),
                }
            )
            print(f"✅ Order {order_id} created successfully for customer {customer_id}.")
            return order_id

        except Exception as e:
            print(f"❌ Error creating order: {e}")
            return None
            
    
    def get_order(self, order_id):
        """
        Retrieves an order from DynamoDB by order_id.
        """
        try:
            response = self.order_table.get_item(Key={"order_id": order_id})
            order = response.get("Item")

            if not order:
                print(f"⚠️ Order {order_id} not found in DynamoDB.")
                return None

            print(f"✅ Order {order_id} retrieved successfully.")
            return order

        except Exception as e:
            print(f"❌ Error retrieving order: {e}")
            return None

    def get_orders_by_customer(self, customer_id):
        """Retrieves all orders for a given customer using a GSI."""
        try:
            response = self.order_table.query(
                IndexName="customer_id-index",  # ✅ Make sure index exists
                KeyConditionExpression=Key("customer_id").eq(customer_id)
            )
    
            orders = response.get("Items", [])
            if not orders:
                print(f"⚠️ No orders found for customer {customer_id}.")
                return []
    
            return orders
    
        except Exception as e:
            print(f"❌ Error retrieving orders for customer {customer_id}: {e}")
            return []


    def add_order_item(self, order_id, product_id, quantity):
        """
        Adds an item to an existing order.
        """
        try:
            order_item_id = str(uuid.uuid4())

            self.order_item_table.put_item(
                Item={
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "date_added": datetime.utcnow().isoformat(),
                }
            )

            print(f"✅ Order item {order_item_id} added to order {order_id}.")
            return order_item_id

        except Exception as e:
            print(f"❌ Error adding order item: {e}")
            return None
            
            
    def remove_order_item(self, order_item_id):
        """
        Removes an item from an order in the DynamoDB OrderItem table.
        
        :param order_item_id: The ID of the order item to be removed
        :return: Response from DynamoDB
        """
        try:
            response = self.order_item_table.delete_item(
                Key={"order_item_id": order_item_id}
            )
            print(f"✅ Order item {order_item_id} removed successfully.")
            return response
        except Exception as e:
            print(f"❌ Error removing order item: {e}")
            return None



    def create_shipping_address(self, customer_id, order_id, address, city, state, zipcode):
        """
        Creates a new shipping address for an order in the DynamoDB ShippingAddress table.
        """
        shipping_id = str(uuid.uuid4())  # Generate unique shipping ID

        try:
            self.shipping_table.put_item(
                Item={
                    "shipping_id": shipping_id,
                    "customer_id": customer_id,
                    "order_id": order_id,
                    "address": address,
                    "city": city,
                    "state": state,
                    "zipcode": zipcode,
                    "date_added": datetime.utcnow().isoformat(),
                }
            )

            print(f"✅ Shipping address {shipping_id} created for order {order_id}.")
            return shipping_id

        except Exception as e:
            print(f"❌ Error creating shipping address for order {order_id}: {e}")
            return None

    def get_shipping_address(self, order_id):
        """
        Retrieves the shipping address for a given order from the DynamoDB ShippingAddress table.
        """
        try:
            response = self.shipping_table.query(
                KeyConditionExpression=Key("order_id").eq(order_id)
            )

            shipping_addresses = response.get("Items", [])
            
            if not shipping_addresses:
                print(f"⚠️ No shipping address found for order {order_id}.")
                return None

            print(f"✅ Retrieved shipping address for order {order_id}.")
            return shipping_addresses

        except Exception as e:
            print(f"❌ Error retrieving shipping address for order {order_id}: {e}")
            return None

    def upload_image_to_s3(self, file_path, bucket_name=None, object_name=None):
        """
        Uploads an image to an S3 bucket and returns the URL.
    
        :param file_path: Path to the file being uploaded
        :param bucket_name: (Optional) S3 bucket name, defaults to self.s3_bucket
        :param object_name: (Optional) S3 object name, defaults to the file name
        :return: URL of the uploaded image or None if upload fails
        """
        bucket_name = bucket_name or self.s3_bucket  # ✅ Default to self.s3_bucket
    
        if object_name is None:
            object_name = os.path.basename(file_path)
    
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
            print(f"✅ Image uploaded successfully: {url}")
            return url
        except Exception as e:
            print(f"❌ Error uploading file to S3: {e}")
            return None

