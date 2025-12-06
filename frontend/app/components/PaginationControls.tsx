"use client";

interface Props {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function PaginationControls({ page, totalPages, onPageChange }: Props) {
  return (
    <div className="flex items-center justify-end gap-3 text-sm text-ink-700">
      <button
        className="rounded-full border border-ink-200 bg-white px-3 py-2 shadow-sm transition hover:-translate-y-0.5 hover:border-ink-400 disabled:translate-y-0 disabled:opacity-50"
        onClick={() => onPageChange(Math.max(1, page - 1))}
        disabled={page <= 1}
      >
        Previous
      </button>
      <span className="rounded-full bg-ink-100 px-3 py-2 font-medium text-ink-800">
        Page {page} of {Math.max(totalPages, 1)}
      </span>
      <button
        className="rounded-full border border-ink-200 bg-white px-3 py-2 shadow-sm transition hover:-translate-y-0.5 hover:border-ink-400 disabled:translate-y-0 disabled:opacity-50"
        onClick={() => onPageChange(Math.min(totalPages || page + 1, page + 1))}
        disabled={page >= totalPages && totalPages !== 0}
      >
        Next
      </button>
    </div>
  );
}
