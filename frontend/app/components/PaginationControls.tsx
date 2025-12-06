"use client";

interface Props {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function PaginationControls({ page, totalPages, onPageChange }: Props) {
  return (
    <nav aria-label="Pagination" className="flex items-center justify-end gap-3 text-sm text-ink-700">
      <button
        aria-label="Go to previous page"
        className="rounded-lg border border-sand-300 bg-white px-4 py-2 font-medium shadow-sm transition-all hover:bg-sand-50 hover:text-ink-900 focus:ring-2 focus:ring-ink-500 focus:ring-offset-2 disabled:opacity-50 disabled:hover:bg-white"
        onClick={() => onPageChange(Math.max(1, page - 1))}
        disabled={page <= 1}
      >
        Previous
      </button>
      <span className="rounded-lg bg-ink-50 px-4 py-2 font-medium text-ink-900">
        Page {page} of {Math.max(totalPages, 1)}
      </span>
      <button
        aria-label="Go to next page"
        className="rounded-lg border border-sand-300 bg-white px-4 py-2 font-medium shadow-sm transition-all hover:bg-sand-50 hover:text-ink-900 focus:ring-2 focus:ring-ink-500 focus:ring-offset-2 disabled:opacity-50 disabled:hover:bg-white"
        onClick={() => onPageChange(Math.min(totalPages || page + 1, page + 1))}
        disabled={page >= totalPages && totalPages !== 0}
      >
        Next
      </button>
    </nav>
  );
}
