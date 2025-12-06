"use client";

import { FormEvent, useState } from "react";

interface Props {
  customerName?: string;
  phone?: string;
  onSubmit: (value: { customer_name?: string; phone?: string }) => void;
}

export function SearchBar({ customerName = "", phone = "", onSubmit }: Props) {
  const [name, setName] = useState(customerName);
  const [phoneVal, setPhoneVal] = useState(phone);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit({ customer_name: name || undefined, phone: phoneVal || undefined });
  };

  return (
    <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-[1fr_1fr_auto] md:items-end">
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-ink-700">Customer Name</label>
        <div className="relative">
          <input
            type="text"
            className="w-full rounded-xl border border-ink-200 bg-white px-4 py-3 text-sm shadow-sm focus:border-ink-500 focus:outline-none"
            placeholder="Search by name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
      </div>
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-ink-700">Phone Number</label>
        <div className="relative">
          <input
            type="text"
            className="w-full rounded-xl border border-ink-200 bg-white px-4 py-3 text-sm shadow-sm focus:border-ink-500 focus:outline-none"
            placeholder="Search by phone"
            value={phoneVal}
            onChange={(e) => setPhoneVal(e.target.value)}
          />
        </div>
      </div>
      <div className="flex justify-end md:justify-center">
        <button
          type="submit"
          className="h-[48px] rounded-xl bg-ink-700 px-6 text-sm font-semibold text-white shadow-sm transition hover:bg-ink-900"
        >
          Search
        </button>
      </div>
    </form>
  );
}
