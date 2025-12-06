export type SortBy = "date" | "quantity" | "customer_name";
export type SortOrder = "asc" | "desc";

export interface SalesQueryParams {
  customer_name?: string;
  phone?: string;
  region?: string;
  gender?: string;
  age_min?: number;
  age_max?: number;
  product_category?: string;
  tag?: string;
  payment_method?: string;
  date_from?: string; // ISO date string
  date_to?: string; // ISO date string
  sort_by?: SortBy;
  order?: SortOrder;
  page?: number;
  page_size?: number;
}

export interface SalesItem {
  // Customer Fields
  customer_id: string;
  customer_name: string;
  phone_number: string;
  gender: string;
  age: number;
  customer_region: string;
  customer_type: string;

  // Product Fields
  product_id: string;
  product_name: string;
  brand: string;
  product_category: string;
  tags: string;

  // Sales Fields
  quantity: number;
  price_per_unit: number;
  discount_percentage: number;
  total_amount: number;
  final_amount: number;

  // Operational Fields
  date: string;
  payment_method: string;
  order_status: string;
  delivery_type: string;
  store_id: string;
  store_location: string;
  salesperson_id: string;
  employee_name: string;

  [key: string]: string | number | boolean | null | undefined;
}

export interface SalesResponse {
  items: SalesItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface MetaResponse {
  regions: string[];
  genders: string[];
  product_categories: string[];
  tags: string[];
  payment_methods: string[];
}
