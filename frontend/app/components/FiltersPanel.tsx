"use client";

import { MetaResponse, SalesQueryParams } from "../../lib/types";

interface Props {
  meta?: MetaResponse;
  values: SalesQueryParams;
  onChange: (partial: SalesQueryParams) => void;
}

export function FiltersPanel({ meta, values, onChange }: Props) {
  const handle = (key: keyof SalesQueryParams, value: string | number | undefined) => {
    onChange({ [key]: value === "" ? undefined : value });
  };

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-region" className="text-sm font-medium text-ink-700">Region</label>
        <select
          id="filter-region"
          className="rounded-xl border border-sand-300 bg-white px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
          value={values.region ?? ""}
          onChange={(e) => handle("region", e.target.value || undefined)}
        >
          <option value="">All Regions</option>
          {meta?.regions.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-gender" className="text-sm font-medium text-ink-700">Gender</label>
        <select
          id="filter-gender"
          className="rounded-xl border border-sand-300 bg-white px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
          value={values.gender ?? ""}
          onChange={(e) => handle("gender", e.target.value || undefined)}
        >
          <option value="">All Genders</option>
          {meta?.genders.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-age-min" className="text-sm font-medium text-ink-700">Age Min</label>
          <input
            id="filter-age-min"
            type="number"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.age_min ?? ""}
            onChange={(e) => handle("age_min", e.target.value ? Number(e.target.value) : undefined)}
          />
        </div>
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-age-max" className="text-sm font-medium text-ink-700">Age Max</label>
          <input
            id="filter-age-max"
            type="number"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.age_max ?? ""}
            onChange={(e) => handle("age_max", e.target.value ? Number(e.target.value) : undefined)}
          />
        </div>
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-category" className="text-sm font-medium text-ink-700">Product Category</label>
        <select
          id="filter-category"
          className="rounded-xl border border-sand-300 bg-white px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
          value={values.product_category ?? ""}
          onChange={(e) => handle("product_category", e.target.value || undefined)}
        >
          <option value="">All Categories</option>
          {meta?.product_categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-tag" className="text-sm font-medium text-ink-700">Tag</label>
        <input
          id="filter-tag"
          type="text"
          className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
          placeholder="Contains tag"
          value={values.tag ?? ""}
          onChange={(e) => handle("tag", e.target.value || undefined)}
        />
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-payment" className="text-sm font-medium text-ink-700">Payment Method</label>
        <select
          id="filter-payment"
          className="rounded-xl border border-sand-300 bg-white px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
          value={values.payment_method ?? ""}
          onChange={(e) => handle("payment_method", e.target.value || undefined)}
        >
          <option value="">All Methods</option>
          {meta?.payment_methods.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-date-from" className="text-sm font-medium text-ink-700">Date From</label>
          <input
            id="filter-date-from"
            type="date"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.date_from ?? ""}
            onChange={(e) => handle("date_from", e.target.value || undefined)}
          />
        </div>
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-date-to" className="text-sm font-medium text-ink-700">Date To</label>
          <input
            id="filter-date-to"
            type="date"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.date_to ?? ""}
            onChange={(e) => handle("date_to", e.target.value || undefined)}
          />
        </div>
      </div>
    </div>
  );
}
