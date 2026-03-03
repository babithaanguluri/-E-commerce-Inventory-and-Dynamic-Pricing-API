# 🚀 E-commerce Inventory & Smart Pricing

Welcome to your new e-commerce heartbeat! This isn't just another backend; it's a smart system designed to handle the two most stressful parts of running an online store: **Inventory** and **Pricing**.

Whether you're selling custom-built laptops or trendy sneakers, this API ensures your stock levels stay accurate and your prices stay competitive—automatically.

---

## ✨ What does this project do for you?

### 🛒 Never Oversell Again
Ever had a customer buy an item only for you to realize it was out of stock? We solved that. 
- When a customer adds an item to their cart, we **reserve** it for 15 minutes. 
- If they don't buy it, the stock automatically returns to the shelf.
- If they do buy it, the stock is permanently updated. No more awkward "oops, out of stock" emails!

### 💰 Pricing that Reacts
Fixed prices are a thing of the past. Our **Dynamic Pricing Engine** works while you sleep:
- **Bulk Rewards**: Want to give a 10% discount if someone buys 5 items? Just set a rule.
- **Flash Sales**: Running a winter sale? Set the dates, and the API handles the price drops.
- **VIP Treatment**: (Ready for you to use!) Give your "Gold" members better prices than everyone else.

### 🛡️ Secure & Reliable
- **Safe Login**: Built with modern security (JWT) to keep user data private.
- **Scalable**: Built with Docker, so it runs the same on your laptop as it does on a massive server.
- **Automated**: Background workers (using Redis/Celery) handle all the boring cleanup tasks so you don't have to.

---

## 🛠️ The Tech Behind the Magic

- **FastAPI**: For a lightning-fast web server.
- **PostgreSQL**: A rock-solid database for your orders and products.
- **Redis & Celery**: The "brains" behind the automated tasks.
- **Docker**: For a "one-click" setup experience.

---

## 🚀 Get Started in 5 Minutes

### 1. The Setup
Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.

```bash
# Clone the heart of your store
git clone https://github.com/babithaanguluri/-E-commerce-Inventory-and-Dynamic-Pricing-API.git
cd -E-commerce-Inventory-and-Dynamic-Pricing-API

# Start the engines
docker-compose up --build
```

### 2. Add Some Life (Seed Data)
Once it's running, run this one command to populate your store with a sample MacBook Pro and some pricing rules:
```bash
docker-compose exec api python -m app.db.seed
```

### 3. Explore
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to see your interactive API playground!

---

## ✅ The Journey So Far

- [x] **Phase 1**: Built the core product and stock system.
- [x] **Phase 2**: Taught the system how to calculate complex discounts.
- [x] **Phase 3**: Added the "15-minute hold" reservation logic.
- [x] **Phase 4**: Built analytics so you can see your top-selling items.
- [x] **Phase 5**: Secured everything with professional login and roles.

---
*Ready to scale your business? This API is your foundation.*
