"use client";

import { useState, useCallback } from "react";

import { FiltersPanel } from "./components/FiltersPanel";
import { PaginationControls } from "./components/PaginationControls";
import { SearchBar } from "./components/SearchBar";
import { SortingDropdown } from "./components/SortingDropdown";
import { TransactionsTable } from "./components/TransactionsTable";
import { useMeta, useSales } from "../lib/hooks";
import { SalesQueryParams, SortBy, SortOrder } from "../lib/types";

export default function Page() {
  const [params, setParams] = useState<SalesQueryParams>({
    sort_by: "date",
    order: "desc",
    page: 1,
    page_size: 10,
  });

  const { data: meta, isLoading: isMetaLoading } = useMeta();
  const { data, isLoading, isError, error, isFetching } = useSales(params);

  const updateParams = useCallback(
    (partial: SalesQueryParams) => {
      setParams((prev) => ({ ...prev, ...partial, page: 1 }));
    },
    [setParams]
  );

  const submitSearch = (value: { customer_name?: string; phone?: string }) => {
    setParams((prev) => ({ ...prev, ...value, page: 1 }));
  };

  const changeSort = (value: { sort_by: SortBy; order: SortOrder }) => {
    setParams((prev) => ({ ...prev, ...value, page: 1 }));
  };

  const changePage = (page: number) => {
    setParams((prev) => ({ ...prev, page }));
  };

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 md:px-8">
      <header className="mb-8 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-ink-500">Dashboard</p>
          <h1 className="text-3xl font-semibold text-ink-900">Retail Sales Management</h1>
          <p className="text-sm text-ink-600">Search, filter, sort, and paginate transactions.</p>
        </div>
        <div className="flex items-center gap-3 text-sm text-ink-600">
          {isFetching ? (
            <span className="rounded-full bg-ink-100 px-3 py-1 text-ink-700">Refreshing...</span>
          ) : (
            <span className="rounded-full bg-ink-100 px-3 py-1 text-ink-700">Live</span>
          )}
        </div>
      </header>

      <div className="grid items-start gap-6 lg:grid-cols-[1.25fr_0.75fr]">
        <section className="space-y-4">
          <div className="rounded-2xl border border-ink-200 bg-white p-5 shadow-card">
            <SearchBar
              customerName={params.customer_name}
              phone={params.phone}
              onSubmit={(v) => submitSearch(v)}
            />
          </div>

          <div className="rounded-2xl border border-ink-200 bg-white p-5 shadow-card">
            <div className="mb-3 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-ink-900">Filters</h2>
                <p className="text-sm text-ink-600">Narrow down by customer, product, payment, and dates.</p>
              </div>
              {isMetaLoading && <span className="text-sm text-ink-600">Loading options...</span>}
            </div>
            <FiltersPanel meta={meta} values={params} onChange={updateParams} />
          </div>

          <div className="rounded-2xl border border-ink-200 bg-white p-4 shadow-card">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <SortingDropdown sortBy={params.sort_by} order={params.order} onChange={changeSort} />
              <PaginationControls page={params.page ?? 1} totalPages={data?.total_pages ?? 0} onPageChange={changePage} />
            </div>
          </div>

          <div className="rounded-2xl border border-ink-200 bg-white p-0 shadow-card">
            {isLoading ? (
              <div className="p-6 text-center text-ink-700">Loading...</div>
            ) : isError ? (
              <div className="p-6 text-center text-red-700">{(error as Error).message || "Something went wrong"}</div>
            ) : (
              <TransactionsTable items={data?.items} />
            )}
          </div>

          <div className="flex items-center justify-between text-sm text-ink-700">
            <div>
              Showing {(data?.items.length ?? 0)} of {data?.total ?? 0} records
            </div>
            <PaginationControls page={params.page ?? 1} totalPages={data?.total_pages ?? 0} onPageChange={changePage} />
          </div>
        </section>

        <section className="space-y-4">
          <div className="rounded-2xl border border-ink-200 bg-white p-5 shadow-card">
            <h2 className="text-lg font-semibold text-ink-900">Tips</h2>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink-700">
              <li>Use name/phone search together for precise lookup.</li>
              <li>Combine date range with payment method to audit transactions.</li>
              <li>Sort by quantity to spot large orders quickly.</li>
            </ul>
          </div>

          <div className="rounded-2xl border border-ink-200 bg-white p-5 shadow-card">
            <h2 className="text-lg font-semibold text-ink-900">Status</h2>
            <div className="mt-2 space-y-2 text-sm text-ink-700">
              <div className="flex items-center justify-between">
                <span>Filters applied</span>
                <span className="rounded-full bg-ink-100 px-2 py-1 text-xs text-ink-700">
                  {Object.values(params).filter((v) => v !== undefined && v !== "" && v !== null && v !== 1 && v !== 10).length}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Total records</span>
                <span className="font-semibold text-ink-900">{data?.total ?? "-"}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Page</span>
                <span className="font-semibold text-ink-900">{params.page ?? 1}</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
