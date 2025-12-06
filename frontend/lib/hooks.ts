"use client";

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { fetchMeta, fetchSales } from "./api";
import { MetaResponse, SalesQueryParams, SalesResponse } from "./types";

const defaultSalesParams: SalesQueryParams = {
  sort_by: "date",
  order: "desc",
  page: 1,
  page_size: 10,
};

const stableKey = (params: SalesQueryParams): string => {
  const sortedEntries = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== "")
    .sort(([a], [b]) => a.localeCompare(b));
  return JSON.stringify(sortedEntries);
};

export const useSales = (params: SalesQueryParams) => {
  const merged = useMemo(() => ({ ...defaultSalesParams, ...params }), [params]);
  const key = useMemo(() => stableKey(merged), [merged]);

  return useQuery<SalesResponse>({
    queryKey: ["sales", key],
    queryFn: ({ signal }) => fetchSales(merged, signal),
    keepPreviousData: true,
    staleTime: 30_000,
  });
};

export const useMeta = () => {
  return useQuery<MetaResponse>({
    queryKey: ["meta"],
    queryFn: ({ signal }) => fetchMeta(signal),
    staleTime: 5 * 60_000,
  });
};
