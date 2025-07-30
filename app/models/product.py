from datetime import datetime
from .database import get_db

class Product:
    """Product model class"""
    
    def __init__(self, id=None, name=None, description=None, price=None, image_path=None, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.image_path = image_path
        self.created_at = created_at
    
    @staticmethod
    def get_all():
        """Get all products ordered by creation date"""
        db = get_db()
        products = db.execute('''
        SELECT p.*, u.username as seller_name 
        FROM products p 
        JOIN users u ON p.seller_id = u.id 
        ORDER BY p.created_at DESC
         ''').fetchall()    
        db.close()
        return [Product(**dict(product)) for product in products]
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        db = get_db()
        product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        return Product(**dict(product)) if product else None
    
    def save(self):
        """Save product to database"""
        db = get_db()
        if self.id:
            # Update existing product
            db.execute(
                'UPDATE products SET name = ?, description = ?, price = ?, image_path = ? WHERE id = ?',
                (self.name, self.description, self.price, self.image_path, self.id)
            )
        else:
            # Insert new product
            cursor = db.execute(
                'INSERT INTO products (name, description, price, image_path) VALUES (?, ?, ?, ?)',
                (self.name, self.description, self.price, self.image_path)
            )
            self.id = cursor.lastrowid
        db.commit()
        return self
    
    def delete(self):
        """Delete product from database"""
        if self.id:
            db = get_db()
            db.execute('DELETE FROM products WHERE id = ?', (self.id,))
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_stats():
        """Get product statistics"""
        db = get_db()
        total_products = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        total_value = db.execute('SELECT SUM(price) FROM products').fetchone()[0] or 0
        products_with_images = db.execute('SELECT COUNT(*) FROM products WHERE image_path IS NOT NULL').fetchone()[0]
        
        return {
            'total_products': total_products,
            'total_value': total_value,
            'products_with_images': products_with_images
        } 