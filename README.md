# Retail Sales Management System

A high-performance, full-stack application designed to manage and analyze retail sales transactions efficiently. Developed as part of the **TruEstate SDE Intern Assignment**.

##  Live Demo

- **Frontend (Vercel):** [https://retail-sales-management-system.vercel.app/](https://retail-sales-management-system.vercel.app/)
- **Backend API (Render):** [https://retail-sales-api-3gyu.onrender.com/docs](https://retail-sales-api-3gyu.onrender.com/docs)

---

## Key Features

###  Advanced Search & Filtering
- **Fuzzy Search:** Instantly search by **Customer Name** or **Phone Number** (powered by PostgreSQL `pg_trgm` & GIN indexes).
- **Multi-Faceted Filters:** Drill down data by:
  - Customer Region
  - Gender & Age Range
  - Product Category & Tags
  - Payment Method
  - Date Range

###  Data Management
- **Sorting:** Sort results by **Date** (Newest/Oldest), **Quantity**, or **Customer Name**.
- **Pagination:** Efficient server-side pagination handling large datasets.
- **Real-time Metadata:** Dynamic filter options fetched directly from the database.

###  Performance Optimizations
- **Sub-second Queries:** Optimized SQL queries using `count="planned"` for instant total counts.
- **Database Indexing:**
  - **GIN Indexes:** For fast text search (`ILIKE '%term%'`).
  - **Composite Indexes:** For efficient "Filter + Sort" operations (e.g., Filter by Gender + Sort by Date).
- **Keep-Alive Mechanism:** Automated GitHub Action to prevent Render cold starts.

---

##  Tech Stack

### Frontend
- **Framework:** [Next.js 14](https://nextjs.org/) (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** TanStack Query (React Query)
- **Deployment:** Vercel

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Language:** Python 3.10+
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Render

---

##  Repository Structure

```bash
root/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── models.py       # Pydantic models
│   │   ├── repository.py   # Database logic
│   │   └── main.py         # Entry point
│   └── requirements.txt
├── frontend/                # Next.js application
│   ├── app/                # Pages & components
│   ├── lib/                # API hooks & types
│   └── public/
└── .github/workflows/       # CI/CD pipelines  
```

---

## 🔧 Local Setup Instructions

### Prerequisites
- Node.js & npm
- Python 3.10+
- Supabase Account (or local PostgreSQL)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# Create a .env file with:
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_anon_key

# Run server
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
# Create a .env.local file with:
# NEXT_PUBLIC_API_BASE=http://localhost:8000/api

# Run development server
npm run dev
```

---

##  Database Schema

The system uses a robust PostgreSQL schema optimized for read-heavy operations.

```sql
CREATE TABLE sales (
    transaction_id TEXT PRIMARY KEY,
    date DATE,
    customer_name TEXT,
    phone_number TEXT,
    customer_region TEXT,
    product_category TEXT,
    tags TEXT,
    quantity INTEGER,
    total_amount NUMERIC,
    -- ... other fields
);

-- Indexes for Performance
CREATE INDEX idx_sales_customer_name_trgm ON sales USING gin (customer_name gin_trgm_ops);
CREATE INDEX idx_sales_gender_date ON sales(gender, date DESC);
```

---

##  API Documentation

The backend provides auto-generated Swagger UI documentation.

- **GET** `/api/sales`: Fetch paginated sales data with filters.
- **GET** `/api/meta`: Fetch unique values for filter dropdowns.
- **GET** `/api/health`: Health check endpoint.



