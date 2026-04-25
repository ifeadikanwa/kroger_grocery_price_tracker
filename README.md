# Grocery Price Tracker

👉 [Open App](https://grocery-price-tracker.streamlit.app/)

A full-stack data-driven application that allows users to track grocery items, monitor real-time prices from Kroger, and analyze price changes over time.

---

## Overview

Grocery Price Tracker helps users answer a simple question:

> “When is the best time to buy my groceries?”

The application allows users to:
- create a personal grocery list
- search real products from Kroger’s API
- track specific products for each grocery item
- view real-time pricing data
- analyze historical price trends

This project combines **application development + data engineering concepts** into a single end-to-end system.

---

## Features

### Current (MVP)
- Add and delete grocery items
- Search real Kroger products using their API
- Track specific products per grocery item
- Prevent duplicate tracking (data integrity)
- Display live product prices (store-specific)
- Remove tracked products
- Multi-page UI (Home, Search, Overview)
- Clean layered architecture (UI → Service → Data)

### In Progress / Planned
- Price refresh pipeline (update all tracked products)
- Historical price tracking (`price_history`)
- Price trend visualization
- Smart alerts (e.g., “price dropped below threshold”)
- Store selection (location-aware pricing)
- Product comparison across brands

---

## Architecture

The app follows a clean layered structure:

```
UI (Streamlit)
↓
Service Layer (business logic)
↓
Data Layer
├── SQLite (persistence)
└── Kroger API (external data)

```

### Key Design Decisions

- **Separation of concerns**: UI never touches raw database or API
- **Domain models**: consistent data representation across layers
- **Idempotent tracking**: prevents duplicate product tracking
- **Soft deletes**: preserves historical data
- **Store-specific pricing**: uses Kroger `locationId` for accurate prices

---

## Tech Stack

- Python
- Streamlit (frontend + app framework)
- SQLite (local database)
- Kroger Public API (product + pricing data)
- Requests (HTTP client)

---

## Data Model

### grocery_items
Stores user-defined grocery categories

### products
Stores normalized product data from Kroger

### tracked_products
Links grocery items to specific products

### price_history (planned)
Stores time-based price snapshots for trend analysis

---

## How It Works

1. User creates a grocery item (e.g., “milk”)
2. User searches products from Kroger
3. User selects a product to track
4. App stores product + tracking relationship
5. App displays real-time price data
6. (future) Background process captures price history over time

---

## Setup

### 1. Clone repo

```bash
git clone <your-repo-url>
cd grocery_price_tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add environment variables

Create `.env`:

```env
KROGER_CLIENT_ID=your_client_id
KROGER_CLIENT_SECRET=your_client_secret
KROGER_LOCATION_ID=your_store_location_id
```

### 4. Run app

```bash
streamlit run app.py
```

---

## Deployment

Deployed using Streamlit Community Cloud.

Secrets are stored securely via Streamlit’s secrets manager.

---

## Why This Project Matters

This project demonstrates:

* Building an end-to-end data application
* Designing scalable data models
* Integrating external APIs into a pipeline
* Managing state and user interactions
* Applying data engineering principles in a real-world scenario

---

## Future Direction

The long-term goal is to evolve this into a **data pipeline-driven system** that:

* continuously ingests pricing data
* stores historical trends
* enables analytics and insights
* helps users optimize grocery spending

```


