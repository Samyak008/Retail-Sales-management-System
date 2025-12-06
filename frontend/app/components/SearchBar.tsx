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
      <div className="flex flex-col gap-1.5">
        <label htmlFor="customer-name" className="text-sm font-medium text-ink-700">
          Customer Name
        </label>
        <div className="relative">
          <input
            id="customer-name"
            type="text"
            className="w-full rounded-xl border border-sand-300 bg-white px-4 py-2.5 text-sm text-ink-900 placeholder:text-ink-400 shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            placeholder="Search by name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="phone-number" className="text-sm font-medium text-ink-700">
          Phone Number
        </label>
        <div className="relative">
          <input
            id="phone-number"
            type="text"
            className="w-full rounded-xl border border-sand-300 bg-white px-4 py-2.5 text-sm text-ink-900 placeholder:text-ink-400 shadow-sm transition-all focus:border-ink-500 focus:ring-2 focus:ring-ink-100 focus:outline-none"
            placeholder="Search by phone"
            value={phoneVal}
            onChange={(e) => setPhoneVal(e.target.value)}
          />
        </div>
      </div>
      <div className="flex justify-end md:justify-center">
        <button
          type="submit"
          className="h-[42px] rounded-xl bg-ink-900 px-6 text-sm font-semibold text-white shadow-sm transition-all hover:bg-ink-700 hover:shadow-md focus:ring-2 focus:ring-ink-500 focus:ring-offset-2"
        >
          Search
        </button>
      </div>
    </form>
  );
}
