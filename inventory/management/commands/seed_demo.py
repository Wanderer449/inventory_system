from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import Category, Product


class Command(BaseCommand):
    help = "Seeds database with 6 realistic categories and 40 products with varied stock levels and INR pricing"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Beginning demo data seeding with Indian Rupee (INR) pricing..."))

        categories_data = [
            {
                "name": "Electronics & Gadgets",
                "description": "High-performance consumer electronics, computer peripherals, and smart accessories.",
            },
            {
                "name": "Office Supplies",
                "description": "Premium workplace essentials, desk organizers, stationery, and ergonomics.",
            },
            {
                "name": "Home & Kitchen",
                "description": "Modern kitchenware, smart home appliances, and durable cookware.",
            },
            {
                "name": "Sports & Fitness",
                "description": "Athletic gear, resistance training equipment, and outdoor fitness tools.",
            },
            {
                "name": "Apparel & Accessories",
                "description": "Ergonomic bags, weather-resistant jackets, and casual utility wear.",
            },
            {
                "name": "Books & Stationery",
                "description": "Technical manuals, luxury journals, fountain pens, and reference guides.",
            },
        ]

        products_data = [
            # 1. Electronics & Gadgets (8 products)
            {
                "category": "Electronics & Gadgets",
                "name": "Sony WH-1000XM5 Wireless Headphones",
                "sku": "ELEC-WH1000",
                "price": Decimal("29990.00"),
                "stock_quantity": 0,  # Low stock test (out of stock)
                "description": "Industry-leading noise cancelling with dual processors and 8 microphones.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "Logitech MX Master 3S Wireless Mouse",
                "sku": "ELEC-MXM3S",
                "price": Decimal("8995.00"),
                "stock_quantity": 2,  # Low stock test
                "description": "Ergonomic quiet click mouse with 8K DPI tracking on glass.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "Keychron Q1 Pro Mechanical Keyboard",
                "sku": "ELEC-KQ1PRO",
                "price": Decimal("16500.00"),
                "stock_quantity": 4,  # Low stock test
                "description": "75% layout custom wireless mechanical keyboard with hot-swappable switches.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "Dell UltraSharp 27 4K USB-C Hub Monitor",
                "sku": "ELEC-U2723QE",
                "price": Decimal("48990.00"),
                "stock_quantity": 8,  # Medium stock
                "description": "IPS Black technology with 2000:1 contrast ratio and 90W power delivery.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "Anker 737 Power Bank (PowerCore 24K)",
                "sku": "ELEC-A737PB",
                "price": Decimal("11499.00"),
                "stock_quantity": 18,  # Medium stock
                "description": "140W ultra-fast two-way charging with smart digital display.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "CalDigit TS4 Thunderbolt 4 Dock",
                "sku": "ELEC-CDTS4",
                "price": Decimal("34990.00"),
                "stock_quantity": 1,  # Low stock test
                "description": "18 ports of extreme connectivity with 98W charging for Mac and PC.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "SanDisk 2TB Extreme Portable SSD",
                "sku": "ELEC-SD2TB",
                "price": Decimal("14499.00"),
                "stock_quantity": 35,  # Healthy stock
                "description": "Up to 1050MB/s read speeds with IP55 water and dust resistance.",
            },
            {
                "category": "Electronics & Gadgets",
                "name": "Elgato Stream Deck MK.2",
                "sku": "ELEC-ESD15",
                "price": Decimal("12999.00"),
                "stock_quantity": 22,  # Healthy stock
                "description": "15 customizable LCD keys for studio controls and shortcut macros.",
            },

            # 2. Office Supplies (7 products)
            {
                "category": "Office Supplies",
                "name": "Herman Miller Aeron Ergonomic Chair",
                "sku": "OFFC-HMAERON",
                "price": Decimal("108500.00"),
                "stock_quantity": 3,  # Low stock test
                "description": "Pellicle suspension breathable mesh with PostureFit SL back support.",
            },
            {
                "category": "Office Supplies",
                "name": "Uplift V2 Commercial Standing Desk 60x30",
                "sku": "OFFC-UPL6030",
                "price": Decimal("62500.00"),
                "stock_quantity": 5,  # Low stock test
                "description": "Dual-motor motorized height adjustable desk with advanced memory keypad.",
            },
            {
                "category": "Office Supplies",
                "name": "Rain Design mStand Aluminum Laptop Stand",
                "sku": "OFFC-RDMS01",
                "price": Decimal("3499.00"),
                "stock_quantity": 14,  # Medium stock
                "description": "Solid aluminum single-piece design brings screen to eye level.",
            },
            {
                "category": "Office Supplies",
                "name": "Fellowes Powershred 99Ci Cross-Cut Shredder",
                "sku": "OFFC-FPS99CI",
                "price": Decimal("21500.00"),
                "stock_quantity": 7,  # Medium stock
                "description": "100% jam-proof system shreds 18 sheets per pass into cross-cut particles.",
            },
            {
                "category": "Office Supplies",
                "name": "BenQ ScreenBar Halo LED Monitor Light",
                "sku": "OFFC-BQHALO",
                "price": Decimal("15990.00"),
                "stock_quantity": 11,  # Medium stock
                "description": "Wireless controller and front/back backlight to reduce eye strain.",
            },
            {
                "category": "Office Supplies",
                "name": "Post-it Super Sticky Notes Cube 400pk",
                "sku": "OFFC-PST400",
                "price": Decimal("499.00"),
                "stock_quantity": 120,  # High stock
                "description": "2x the sticking power for reminders on monitors and whiteboards.",
            },
            {
                "category": "Office Supplies",
                "name": "Swingline Heavy Duty Desktop Stapler",
                "sku": "OFFC-SWHD60",
                "price": Decimal("1850.00"),
                "stock_quantity": 45,  # High stock
                "description": "Durable metal construction easily staples up to 60 sheets.",
            },

            # 3. Home & Kitchen (7 products)
            {
                "category": "Home & Kitchen",
                "name": "Breville Barista Touch Espresso Machine",
                "sku": "HOME-BRV880",
                "price": Decimal("84990.00"),
                "stock_quantity": 1,  # Low stock test
                "description": "Automated touchscreen with ThermoJet heating and auto steam wand.",
            },
            {
                "category": "Home & Kitchen",
                "name": "Fellow Stagg EKG Electric Gooseneck Kettle",
                "sku": "HOME-FSTG09",
                "price": Decimal("14500.00"),
                "stock_quantity": 5,  # Low stock test
                "description": "Precision pour spout with to-the-degree variable temperature control.",
            },
            {
                "category": "Home & Kitchen",
                "name": "Vitamix A3500 Ascent Series Blender",
                "sku": "HOME-VTX3500",
                "price": Decimal("54990.00"),
                "stock_quantity": 9,  # Medium stock
                "description": "Five program settings, touchscreen controls, and variable speed dial.",
            },
            {
                "category": "Home & Kitchen",
                "name": "Le Creuset Enameled Cast Iron Dutch Oven 5.5 Qt",
                "sku": "HOME-LCCDO55",
                "price": Decimal("35500.00"),
                "stock_quantity": 12,  # Medium stock
                "description": "Exceptional heat distribution and retention with chip-resistant enamel.",
            },
            {
                "category": "Home & Kitchen",
                "name": "OXO Good Grips 10-Piece Airtight POP Container Set",
                "sku": "HOME-OXPOP10",
                "price": Decimal("9499.00"),
                "stock_quantity": 28,  # Healthy stock
                "description": "Space-efficient food storage modular pantry organization system.",
            },
            {
                "category": "Home & Kitchen",
                "name": "Zwilling Pro 8-Inch Chef's Knife",
                "sku": "HOME-ZWPRO08",
                "price": Decimal("13500.00"),
                "stock_quantity": 19,  # Medium stock
                "description": "German high-carbon stainless steel blade forged from a single piece.",
            },
            {
                "category": "Home & Kitchen",
                "name": "ThermoPro TP20 Wireless Meat Thermometer",
                "sku": "HOME-TP20WL",
                "price": Decimal("4299.00"),
                "stock_quantity": 50,  # High stock
                "description": "Dual-probe remote digital cooking thermometer for grill and smoker.",
            },

            # 4. Sports & Fitness (6 products)
            {
                "category": "Sports & Fitness",
                "name": "Bowflex SelectTech 552 Adjustable Dumbbells",
                "sku": "SPRT-BF552",
                "price": Decimal("36500.00"),
                "stock_quantity": 2,  # Low stock test
                "description": "Adjusts from 5 to 52.5 lbs with intuitive turn-of-a-dial mechanism.",
            },
            {
                "category": "Sports & Fitness",
                "name": "Concept2 RowErg Indoor Rower",
                "sku": "SPRT-C2ROW",
                "price": Decimal("85000.00"),
                "stock_quantity": 3,  # Low stock test
                "description": "Air-resistance flywheel with PM5 performance monitor and device cradle.",
            },
            {
                "category": "Sports & Fitness",
                "name": "Theragun PRO Gen 5 Percussive Massager",
                "sku": "SPRT-THPRO5",
                "price": Decimal("42990.00"),
                "stock_quantity": 0,  # Low stock test (out of stock)
                "description": "QuietForce motor delivers deep 16mm muscle treatment with OLED display.",
            },
            {
                "category": "Sports & Fitness",
                "name": "Manduka PRO Yoga Mat 6mm",
                "sku": "SPRT-MNPRO71",
                "price": Decimal("11500.00"),
                "stock_quantity": 16,  # Medium stock
                "description": "Ultra-dense cushioning provides joint protection on carpet or hardwood.",
            },
            {
                "category": "Sports & Fitness",
                "name": "Hydro Flask 32 oz Wide Mouth with Straw Lid",
                "sku": "SPRT-HF32OZ",
                "price": Decimal("3799.00"),
                "stock_quantity": 64,  # High stock
                "description": "TempShield double-wall vacuum insulation keeps liquids cold 24 hours.",
            },
            {
                "category": "Sports & Fitness",
                "name": "Garmin Forerunner 265 GPS Running Watch",
                "sku": "SPRT-GFR265",
                "price": Decimal("38990.00"),
                "stock_quantity": 8,  # Medium stock
                "description": "Bright AMOLED touchscreen with advanced training metrics and recovery insights.",
            },

            # 5. Apparel & Accessories (6 products)
            {
                "category": "Apparel & Accessories",
                "name": "Peak Design Everyday Backpack 20L V2",
                "sku": "APPR-PDBP20",
                "price": Decimal("23990.00"),
                "stock_quantity": 4,  # Low stock test
                "description": "Weatherproof 100% recycled 400D nylon canvas with MagLatch hardware.",
            },
            {
                "category": "Apparel & Accessories",
                "name": "Patagonia Nano Puff Insulated Jacket",
                "sku": "APPR-PTNPJK",
                "price": Decimal("19990.00"),
                "stock_quantity": 15,  # Medium stock
                "description": "Warm, windproof, water-resistant PrimaLoft Gold Insulation Eco.",
            },
            {
                "category": "Apparel & Accessories",
                "name": "Bellroy Slim Sleeve Leather Wallet",
                "sku": "APPR-BRSLIM",
                "price": Decimal("6799.00"),
                "stock_quantity": 38,  # High stock
                "description": "Environmentally certified leather with quick-draw slots and pull-tab pocket.",
            },
            {
                "category": "Apparel & Accessories",
                "name": "Ray-Ban Classic Polarized Wayfarer Sunglasses",
                "sku": "APPR-RB2140",
                "price": Decimal("17490.00"),
                "stock_quantity": 5,  # Low stock test
                "description": "Timeless G-15 green polarized lenses with acetate frame construction.",
            },
            {
                "category": "Apparel & Accessories",
                "name": "Darn Tough Hiker Boot Full Cushion Socks",
                "sku": "APPR-DTHIKER",
                "price": Decimal("2299.00"),
                "stock_quantity": 85,  # High stock
                "description": "Merino wool performance fit unconditionally guaranteed for life.",
            },
            {
                "category": "Apparel & Accessories",
                "name": "Aer Travel Pack 3 35L Carry-On",
                "sku": "APPR-AERTP3",
                "price": Decimal("21500.00"),
                "stock_quantity": 10,  # Medium stock
                "description": "1680D Cordura ballistic nylon with lay-flat main compartment.",
            },

            # 6. Books & Stationery (6 products)
            {
                "category": "Books & Stationery",
                "name": "Designing Data-Intensive Applications (Kleppmann)",
                "sku": "BOOK-DDIA01",
                "price": Decimal("3299.00"),
                "stock_quantity": 3,  # Low stock test
                "description": "Comprehensive guide to data architecture, consensus, and storage engines.",
            },
            {
                "category": "Books & Stationery",
                "name": "Two Scoops of Django 3.x / 4.x Best Practices",
                "sku": "BOOK-TSD4X",
                "price": Decimal("3650.00"),
                "stock_quantity": 12,  # Medium stock
                "description": "Industry best practices and code organization recipes for Django developers.",
            },
            {
                "category": "Books & Stationery",
                "name": "Leuchtturm1917 Hardcover Medium A5 Dotted Notebook",
                "sku": "BOOK-LT1917",
                "price": Decimal("1999.00"),
                "stock_quantity": 72,  # High stock
                "description": "Numbered pages, table of contents, 80 g/sqm acid-free ink-proof paper.",
            },
            {
                "category": "Books & Stationery",
                "name": "Lamy 2000 Makrolon Fountain Pen - Fine Nib",
                "sku": "BOOK-LM2000",
                "price": Decimal("16990.00"),
                "stock_quantity": 2,  # Low stock test
                "description": "Iconic Bauhaus design with 14K gold platinum-plated semi-hooded nib.",
            },
            {
                "category": "Books & Stationery",
                "name": "Iroshizuku Bottled Fountain Pen Ink (Kon-Peki 50ml)",
                "sku": "BOOK-PILOTKP",
                "price": Decimal("2150.00"),
                "stock_quantity": 25,  # Healthy stock
                "description": "Deep celestial blue shading ink manufactured in Japan by Pilot.",
            },
            {
                "category": "Books & Stationery",
                "name": "Midori Brass Bullet Pencil & Refills",
                "sku": "BOOK-MDRB01",
                "price": Decimal("2499.00"),
                "stock_quantity": 18,  # Medium stock
                "description": "Solid aging brass body designed to travel comfortably inside pockets.",
            },
        ]

        with transaction.atomic():
            # 1. Create or update Categories
            category_instances = {}
            for c_data in categories_data:
                cat, created = Category.objects.update_or_create(
                    name=c_data["name"],
                    defaults={"description": c_data["description"]},
                )
                category_instances[c_data["name"]] = cat
                action = "Created" if created else "Updated"
                self.stdout.write(f"  [{action}] Category: {cat.name}")

            # 2. Create or update Products
            created_count = 0
            updated_count = 0
            low_stock_seeded = 0

            for p_data in products_data:
                cat_obj = category_instances[p_data["category"]]
                prod, created = Product.objects.update_or_create(
                    sku=p_data["sku"],
                    defaults={
                        "name": p_data["name"],
                        "category": cat_obj,
                        "price": p_data["price"],
                        "stock_quantity": p_data["stock_quantity"],
                        "description": p_data["description"],
                    },
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

                if prod.stock_quantity <= 5:
                    low_stock_seeded += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully seeded demo data in Indian Rupees (INR / Rs.)!\n"
                f" - Total Categories: {len(category_instances)}\n"
                f" - Total Products: {created_count + updated_count} ({created_count} created, {updated_count} updated)\n"
                f" - Low-stock products (qty <= 5): {low_stock_seeded}\n"
            )
        )
