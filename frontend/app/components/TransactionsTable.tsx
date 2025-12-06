"use client";

import { SalesItem } from "../../lib/types";

interface Props {
  items?: SalesItem[];
}

export function TransactionsTable({ items }: Props) {
  if (!items || items.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-ink-200 bg-white p-8 text-center text-ink-700">
        No results found.
      </div>
    );
  }

  const columns = Object.keys(items[0]);

  return (
    <div className="overflow-auto rounded-2xl">
      <table className="min-w-full text-sm text-ink-900">
        <thead className="bg-ink-100 text-left font-semibold">
          <tr>
            {columns.map((col) => (
              <th key={col} className="px-4 py-3 capitalize text-ink-700">
                {col.replace(/_/g, " ")}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((row, idx) => (
            <tr key={idx} className="table-row-hover">
              {columns.map((col) => (
                <td key={col} className="border-t border-ink-50 px-4 py-3 text-ink-900">
                  {String(row[col] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
