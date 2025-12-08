import { MetaResponse, SalesQueryParams, SalesResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

const toSearchParams = (params: SalesQueryParams): string => {
  const search = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null) return;

    if (Array.isArray(value)) {
      const cleaned = value.filter((v) => v !== undefined && v !== null && v !== "");
      if (cleaned.length === 0) return;
      cleaned.forEach((v) => search.append(key, String(v)));
      return;
    }

    if (value === "") return;
    search.append(key, String(value));
  });

  return search.toString();
};

const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
};

export const fetchSales = async (
  params: SalesQueryParams,
  signal?: AbortSignal
): Promise<SalesResponse> => {
  const query = toSearchParams(params);
  const url = `${API_BASE}/sales${query ? `?${query}` : ""}`;
  const res = await fetch(url, { signal });
  return handleResponse<SalesResponse>(res);
};

export const fetchMeta = async (signal?: AbortSignal): Promise<MetaResponse> => {
  const res = await fetch(`${API_BASE}/meta`, { signal });
  return handleResponse<MetaResponse>(res);
};
