import { useState, useCallback } from 'react';

export interface PaginatedResponse<T> {
  count: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  next: string | null;
  previous: string | null;
  first: string | null;
  last: string | null;
  results: T[];
}

interface UsePaginationOptions<T> {
  initialData?: PaginatedResponse<T>;
  fetchFunction: (page: number) => Promise<PaginatedResponse<T>>;
  onError?: (error: Error) => void;
}

export function usePagination<T>({
  initialData,
  fetchFunction,
  onError
}: UsePaginationOptions<T>) {
  const [data, setData] = useState<PaginatedResponse<T> | undefined>(initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchPage = useCallback(async (page: number) => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await fetchFunction(page);
      setData(response);
    } catch (e) {
      const error = e instanceof Error ? e : new Error('Failed to fetch data');
      setError(error);
      onError?.(error);
    } finally {
      setIsLoading(false);
    }
  }, [fetchFunction, onError]);

  const goToPage = useCallback((page: number) => {
    if (!data) return;
    if (page < 1 || page > data.total_pages) return;
    fetchPage(page);
  }, [data, fetchPage]);

  const goToNextPage = useCallback(() => {
    if (!data || !data.next) return;
    goToPage(data.current_page + 1);
  }, [data, goToPage]);

  const goToPreviousPage = useCallback(() => {
    if (!data || !data.previous) return;
    goToPage(data.current_page - 1);
  }, [data, goToPage]);

  const goToFirstPage = useCallback(() => {
    if (!data || data.current_page === 1) return;
    goToPage(1);
  }, [data, goToPage]);

  const goToLastPage = useCallback(() => {
    if (!data || data.current_page === data.total_pages) return;
    goToPage(data.total_pages);
  }, [data, goToPage]);

  return {
    data,
    isLoading,
    error,
    goToPage,
    goToNextPage,
    goToPreviousPage,
    goToFirstPage,
    goToLastPage,
    hasNextPage: !!data?.next,
    hasPreviousPage: !!data?.previous,
    currentPage: data?.current_page ?? 1,
    totalPages: data?.total_pages ?? 1,
    pageSize: data?.page_size ?? 12,
    totalItems: data?.count ?? 0
  };
}
