import random

from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Populate the products table with nearly 100 random sample records.'

    def handle(self, *args, **options):
        categories = [
            'Electronics',
            'Fashion',
            'Home',
            'Sports',
            'Beauty',
            'Toys',
            'Books',
            'Grocery',
        ]

        adjectives = [
            'Smart', 'Premium', 'Classic', 'Pro', 'Ultra', 'Eco', 'Sport', 'Deluxe', 'Compact', 'Wireless',
            'Portable', 'Advanced', 'Elegant', 'Modern', 'Power', 'Fresh', 'Bright', 'Cozy', 'Bold', 'Vintage',
        ]

        items = [
            'Phone', 'Laptop', 'Headphones', 'Speaker', 'Camera', 'Watch', 'Jacket', 'Sneakers', 'Bag', 'Desk Lamp',
            'Mixer', 'Backpack', 'Sunglasses', 'Book', 'Notebook', 'Chair', 'Water Bottle', 'Tablet', 'Gloves', 'Pillow',
        ]

        Category.objects.all().delete()
        Product.objects.all().delete()

        category_objects = []
        for name in categories:
            category_objects.append(Category.objects.create(name=name))

        total_records = 100
        image_map = {
            'Phone': 'product_images/phone.jpg',
            'Tablet': 'product_images/phone.jpg',
            'Camera': 'product_images/phone.jpg',
            'Laptop': 'product_images/laptop.jpg',
            'Desk Lamp': 'product_images/laptop.jpg',
            'Chair': 'product_images/laptop.jpg',
            'Book': 'product_images/laptop.jpg',
            'Notebook': 'product_images/laptop.jpg',
            'Headphones': 'product_images/headphones.jpg',
            'Speaker': 'product_images/headphones.jpg',
            'Watch': 'product_images/watch.jpg',
            'Sneakers': 'product_images/sneakers.jpg',
            'Jacket': 'product_images/sneakers.jpg',
            'Gloves': 'product_images/sneakers.jpg',
            'Sunglasses': 'product_images/sneakers.jpg',
            'Backpack': 'product_images/backpack.jpg',
            'Bag': 'product_images/backpack.jpg',
            'Mixer': 'product_images/backpack.jpg',
            'Water Bottle': 'product_images/backpack.jpg',
            'Pillow': 'product_images/backpack.jpg'
        }

        for i in range(total_records):
            item_type = random.choice(items)
            name = f"{random.choice(adjectives)} {item_type}"
            description = (
                f"{name} with high-quality build, reliable performance, and modern styling. "
                f"Perfect for daily use and great value at this price point."
            )
            price = round(random.uniform(299.0, 99999.0), 2)
            stock = random.randint(0, 200)
            category = random.choice(category_objects)
            
            selected_image = image_map.get(item_type, 'product_images/laptop.jpg')

            Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                stock=stock,
                image=selected_image
            )

        self.stdout.write(self.style.SUCCESS(f'Created {total_records} products and {len(category_objects)} categories.'))

