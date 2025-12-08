"use client";

import { MetaResponse, SalesQueryParams } from "../../lib/types";

interface Props {
  meta?: MetaResponse;
  values: SalesQueryParams;
  onChange: (partial: SalesQueryParams) => void;
}

interface MultiSelectProps {
  id: string;
  label: string;
  options?: string[];
  values: string[];
  placeholder: string;
  onChange: (next: string[]) => void;
}

const MultiSelect = ({ id, label, options = [], values, placeholder, onChange }: MultiSelectProps) => {
  const toggle = (option: string) => {
    const next = values.includes(option)
      ? values.filter((v) => v !== option)
      : [...values, option];
    onChange(next);
  };

  const clear = () => onChange([]);

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between gap-2">
        <label htmlFor={id} className="text-sm font-medium text-ink-700">{label}</label>
        <button
          type="button"
          onClick={clear}
          className="text-xs font-semibold text-ink-500 underline-offset-2 hover:text-ink-700 focus:outline-none"
        >
          Clear
        </button>
      </div>

      <div className="rounded-xl border border-sand-300 bg-white shadow-sm">
        {options.length === 0 ? (
          <div className="px-3 py-2 text-sm text-ink-400">No options available</div>
        ) : (
          <div id={id} className="max-h-40 overflow-y-auto divide-y divide-sand-100">
            {options.map((option) => (
              <label key={option} className="flex cursor-pointer items-center gap-3 px-3 py-2 hover:bg-sand-50">
                <input
                  type="checkbox"
                  className="h-4 w-4 rounded border-sand-400 text-ink-600 focus:ring-ink-500"
                  checked={values.includes(option)}
                  onChange={() => toggle(option)}
                />
                <span className="text-sm text-ink-800">{option}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-2 text-xs text-ink-600">
        {values.length ? (
          values.map((v) => (
            <span key={v} className="inline-flex items-center gap-1 rounded-full bg-ink-50 px-2 py-1">
              {v}
            </span>
          ))
        ) : (
          <span className="text-ink-400">{placeholder}</span>
        )}
      </div>
    </div>
  );
};

export function FiltersPanel({ meta, values, onChange }: Props) {
  const handlePrimitive = (key: keyof SalesQueryParams, value: string | number | undefined) => {
    onChange({ [key]: value === "" ? undefined : value });
  };

  const handleMulti = (key: keyof SalesQueryParams, next: string[]) => {
    onChange({ [key]: next.length ? next : undefined });
  };

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      <MultiSelect
        id="filter-region"
        label="Region"
        options={meta?.regions}
        values={values.region ?? []}
        placeholder="All regions"
        onChange={(next) => handleMulti("region", next)}
      />

      <MultiSelect
        id="filter-gender"
        label="Gender"
        options={meta?.genders}
        values={values.gender ?? []}
        placeholder="All genders"
        onChange={(next) => handleMulti("gender", next)}
      />

      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-age-min" className="text-sm font-medium text-ink-700">Age Min</label>
          <input
            id="filter-age-min"
            type="number"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.age_min ?? ""}
            onChange={(e) => handlePrimitive("age_min", e.target.value ? Number(e.target.value) : undefined)}
          />
        </div>
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-age-max" className="text-sm font-medium text-ink-700">Age Max</label>
          <input
            id="filter-age-max"
            type="number"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.age_max ?? ""}
            onChange={(e) => handlePrimitive("age_max", e.target.value ? Number(e.target.value) : undefined)}
          />
        </div>
      </div>

      <MultiSelect
        id="filter-category"
        label="Product Category"
        options={meta?.product_categories}
        values={values.product_category ?? []}
        placeholder="All categories"
        onChange={(next) => handleMulti("product_category", next)}
      />

      <MultiSelect
        id="filter-tag"
        label="Tag"
        options={meta?.tags}
        values={values.tag ?? []}
        placeholder="All tags"
        onChange={(next) => handleMulti("tag", next)}
      />

      <MultiSelect
        id="filter-payment"
        label="Payment Method"
        options={meta?.payment_methods}
        values={values.payment_method ?? []}
        placeholder="All methods"
        onChange={(next) => handleMulti("payment_method", next)}
      />

      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-date-from" className="text-sm font-medium text-ink-700">Date From</label>
          <input
            id="filter-date-from"
            type="date"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.date_from ?? ""}
            onChange={(e) => handlePrimitive("date_from", e.target.value || undefined)}
          />
        </div>
        <div className="flex flex-col gap-1.5">
          <label htmlFor="filter-date-to" className="text-sm font-medium text-ink-700">Date To</label>
          <input
            id="filter-date-to"
            type="date"
            className="rounded-xl border border-sand-300 px-3 py-2 text-sm shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            value={values.date_to ?? ""}
            onChange={(e) => handlePrimitive("date_to", e.target.value || undefined)}
          />
        </div>
      </div>
    </div>
  );
}
