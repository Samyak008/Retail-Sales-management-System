"use client";

import { useState, useCallback } from "react";

import { FiltersPanel } from "./components/FiltersPanel";
import { PaginationControls } from "./components/PaginationControls";
import { SearchBar } from "./components/SearchBar";
import { SortingDropdown } from "./components/SortingDropdown";
import { TransactionsTable } from "./components/TransactionsTable";
import { useMeta, useSales } from "@/lib/hooks";
import { SalesQueryParams, SortBy, SortOrder } from "@/lib/types";

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
    <main className="min-h-screen bg-sand-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header Section */}
        <header className="mb-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-ink-900 sm:text-4xl">
                Retail Sales Management
              </h1>
              <p className="mt-2 text-lg text-ink-500">
                Manage and analyze your sales transactions efficiently.
              </p>
            </div>
            <div className="flex items-center gap-2">
              {isFetching && (
                <span className="inline-flex items-center rounded-full bg-ink-100 px-3 py-1 text-xs font-medium text-ink-700">
                  Updating...
                </span>
              )}
            </div>
          </div>
        </header>

        {/* Controls Section */}
        <section aria-label="Search and Filters" className="mb-8 space-y-6">
          <div className="rounded-2xl bg-white p-6 shadow-card">
            <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div className="w-full lg:max-w-2xl">
                <SearchBar
                  customerName={params.customer_name}
                  phone={params.phone}
                  onSubmit={submitSearch}
                />
              </div>
              <div className="flex items-center justify-end">
                <SortingDropdown
                  sortBy={params.sort_by}
                  order={params.order}
                  onChange={changeSort}
                />
              </div>
            </div>
            
            <div className="border-t border-sand-100 pt-6">
              <FiltersPanel
                meta={meta}
                values={params}
                onChange={updateParams}
              />
            </div>
          </div>
        </section>

        {/* Data Section */}
        <section aria-label="Transactions Data" className="space-y-4">
          {isError ? (
            <div role="alert" className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-800">
              <p className="font-medium">Error loading data</p>
              <p className="text-sm">{(error as Error).message}</p>
            </div>
          ) : (
            <>
              <div className="relative min-h-[400px] rounded-2xl bg-white shadow-card">
                {isLoading ? (
                  <div className="flex h-64 items-center justify-center text-ink-500">
                    <div className="flex flex-col items-center gap-2">
                      <div className="h-8 w-8 animate-spin rounded-full border-4 border-ink-200 border-t-ink-500"></div>
                      <p>Loading transactions...</p>
                    </div>
                  </div>
                ) : (
                  <TransactionsTable items={data?.items} />
                )}
              </div>

              {data && (
                <div className="mt-6">
                  <PaginationControls
                    page={data.page}
                    totalPages={data.total_pages}
                    onPageChange={changePage}
                  />
                </div>
              )}
            </>
          )}
        </section>
      </div>
    </main>
  );
}
