# Supabase Migration Guide

This guide will help you migrate your CSV data to Supabase for faster performance.

## Benefits
- ⚡ **Instant cold starts** (no 50+ second delays)
- 🚀 **Fast queries** with database indexing
- 💾 **Low memory usage** (no need to load full CSV)
- 📊 **Scalable** to millions of rows

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up
2. Click **New Project**
3. Name it `retail-sales-db`
4. Set a strong database password
5. Choose a region close to your Render deployment
6. Wait for project to be created (~2 minutes)

## Step 2: Create Database Table

1. In your Supabase project, go to **SQL Editor**
2. Click **New Query**
3. Paste this SQL:

```sql
CREATE TABLE IF NOT EXISTS sales (
    transaction_id TEXT PRIMARY KEY,
    date DATE,
    customer_id TEXT,
    customer_name TEXT,
    phone_number TEXT,
    gender TEXT,
    age INTEGER,
    customer_region TEXT,
    customer_type TEXT,
    product_id TEXT,
    product_name TEXT,
    brand TEXT,
    product_category TEXT,
    tags TEXT,
    quantity INTEGER,
    price_per_unit NUMERIC,
    discount_percentage NUMERIC,
    total_amount NUMERIC,
    final_amount NUMERIC,
    payment_method TEXT,
    order_status TEXT,
    delivery_type TEXT,
    store_id TEXT,
    store_location TEXT,
    salesperson_id TEXT,
    employee_name TEXT
);

-- Create indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date);
CREATE INDEX IF NOT EXISTS idx_sales_customer_region ON sales(customer_region);
CREATE INDEX IF NOT EXISTS idx_sales_product_category ON sales(product_category);
CREATE INDEX IF NOT EXISTS idx_sales_customer_name ON sales(customer_name);
CREATE INDEX IF NOT EXISTS idx_sales_gender ON sales(gender);
CREATE INDEX IF NOT EXISTS idx_sales_payment_method ON sales(payment_method);
```

4. Click **Run** (or press F5)

## Step 3: Get Supabase Credentials

1. In Supabase, go to **Settings** → **API**
2. Copy your **Project URL** (e.g., `https://xxxxx.supabase.co`)
3. Copy your **service_role key** (under "Project API keys")
   - ⚠️ Keep this secret! Don't commit it to git

## Step 4: Run Migration Script Locally

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables:
```bash
# Windows PowerShell
$env:SUPABASE_URL="https://xxxxx.supabase.co"
$env:SUPABASE_KEY="your_service_role_key"

# Linux/Mac
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="your_service_role_key"
```

3. Run the migration:
```bash
cd ..
python -m backend.scripts.migrate_to_supabase
```

This will upload all CSV data to Supabase in batches. It may take 5-10 minutes depending on your connection speed.

## Step 5: Update Render Environment Variables

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your `retail-sales-api` service
3. Go to **Environment**
4. **Remove** the `DATA_CSV_URL` variable (no longer needed!)
5. **Remove** the `DATA_MAX_ROWS` variable (no longer needed!)
6. **Add** two new variables:
   - `SUPABASE_URL` = `https://xxxxx.supabase.co` (your Project URL)
   - `SUPABASE_KEY` = `your_service_role_key`
7. Click **Save**

Render will automatically redeploy. The new deployment will:
- Start up in seconds (not minutes!)
- Query Supabase directly for data
- Be much faster and more efficient

## Step 6: Test the API

After deployment completes:

```bash
curl "https://retail-sales-api-3gyu.onrender.com/api/sales?page=1&page_size=10"
```

You should get instant results! 🎉

## Rollback (if needed)

If something goes wrong, you can rollback:

1. In Render, remove `SUPABASE_URL` and `SUPABASE_KEY`
2. Re-add `DATA_CSV_URL` with the GitHub release URL
3. The backend will automatically fall back to CSV loading

## Performance Comparison

| Method | Cold Start | Query Time | Memory |
|--------|-----------|------------|--------|
| CSV from URL | 50-60s | 1-2s | 500MB+ |
| **Supabase** | **2-3s** | **50-200ms** | **50MB** |

**10-20x faster!** 🚀
