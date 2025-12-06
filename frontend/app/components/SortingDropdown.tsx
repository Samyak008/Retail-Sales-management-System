"use client";

import { SortBy, SortOrder } from "../../lib/types";

interface Props {
  sortBy?: SortBy;
  order?: SortOrder;
  onChange: (value: { sort_by: SortBy; order: SortOrder }) => void;
}

export function SortingDropdown({ sortBy = "date", order = "desc", onChange }: Props) {
  return (
    <div className="flex flex-wrap items-center gap-3 text-sm text-ink-700">
      <label className="font-medium">Sort</label>
      <select
        className="rounded-xl border border-ink-200 bg-white px-3 py-2 shadow-sm focus:border-ink-500 focus:outline-none"
        value={sortBy}
        onChange={(e) => onChange({ sort_by: e.target.value as SortBy, order })}
      >
        <option value="date">Date</option>
        <option value="quantity">Quantity</option>
        <option value="customer_name">Customer Name</option>
      </select>
      <select
        className="rounded-xl border border-ink-200 bg-white px-3 py-2 shadow-sm focus:border-ink-500 focus:outline-none"
        value={order}
        onChange={(e) => onChange({ sort_by: sortBy, order: e.target.value as SortOrder })}
      >
        <option value="desc">Desc</option>
        <option value="asc">Asc</option>
      </select>
    </div>
  );
}
