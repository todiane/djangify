// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { format, parseISO } from 'date-fns';
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date) {
  const parsedDate = typeof date === 'string' ? parseISO(date) : date;
  return format(parsedDate, 'MMMM d, yyyy');
}

export function formatReadingTime(minutes: number): string {
  return `Read time: ${minutes} min`
}

export function formatWordCount(count: number): string {
  return `Word Count: ${count}`
}