"use client";

import { SalesItem } from "@/lib/types";

interface Props {
  items?: SalesItem[];
}

const COLUMN_GROUPS = [
  {
    title: "Customer Fields",
    columns: [
      { key: "customer_id", label: "Customer ID" },
      { key: "customer_name", label: "Customer Name" },
      { key: "phone_number", label: "Phone Number" },
      { key: "gender", label: "Gender" },
      { key: "age", label: "Age" },
      { key: "customer_region", label: "Customer Region" },
      { key: "customer_type", label: "Customer Type" },
    ],
  },
  {
    title: "Product Fields",
    columns: [
      { key: "product_id", label: "Product ID" },
      { key: "product_name", label: "Product Name" },
      { key: "brand", label: "Brand" },
      { key: "product_category", label: "Product Category" },
      { key: "tags", label: "Tags" },
    ],
  },
  {
    title: "Sales Fields",
    columns: [
      { key: "quantity", label: "Quantity" },
      { key: "price_per_unit", label: "Price per Unit" },
      { key: "discount_percentage", label: "Discount %" },
      { key: "total_amount", label: "Total Amount" },
      { key: "final_amount", label: "Final Amount" },
    ],
  },
  {
    title: "Operational Fields",
    columns: [
      { key: "date", label: "Date" },
      { key: "payment_method", label: "Payment Method" },
      { key: "order_status", label: "Order Status" },
      { key: "delivery_type", label: "Delivery Type" },
      { key: "store_id", label: "Store ID" },
      { key: "store_location", label: "Store Location" },
      { key: "salesperson_id", label: "Salesperson ID" },
      { key: "employee_name", label: "Employee Name" },
    ],
  },
];

export function TransactionsTable({ items }: Props) {
  if (!items || items.length === 0) {
    return (
      <div className="flex h-64 flex-col items-center justify-center rounded-2xl border border-dashed border-sand-300 bg-white p-8 text-center text-ink-500">
        <p className="text-lg font-medium">No results found</p>
        <p className="text-sm">Try adjusting your filters or search terms.</p>
      </div>
    );
  }

  return (
    <div className="overflow-auto rounded-2xl border border-sand-200 shadow-sm">
      <table className="min-w-full text-sm text-ink-900">
        <thead className="bg-sand-50 text-left font-semibold">
          {/* Group Headers */}
          <tr>
            {COLUMN_GROUPS.map((group) => (
              <th
                key={group.title}
                colSpan={group.columns.length}
                scope="colgroup"
                className="border-b border-sand-200 px-4 py-2 text-center text-xs uppercase tracking-wider text-ink-500 bg-sand-100"
              >
                {group.title}
              </th>
            ))}
          </tr>
          {/* Column Headers */}
          <tr>
            {COLUMN_GROUPS.flatMap((group) =>
              group.columns.map((col) => (
                <th
                  key={col.key}
                  scope="col"
                  className="whitespace-nowrap border-b border-sand-200 px-4 py-3 text-ink-700"
                >
                  {col.label}
                </th>
              ))
            )}
          </tr>
        </thead>
        <tbody className="divide-y divide-sand-100 bg-white">
          {items.map((row, idx) => (
            <tr key={idx} className="hover:bg-sand-50 transition-colors">
              {COLUMN_GROUPS.flatMap((group) =>
                group.columns.map((col) => (
                  <td key={col.key} className="whitespace-nowrap px-4 py-3 text-ink-900">
                    {String(row[col.key] ?? "")}
                  </td>
                ))
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
