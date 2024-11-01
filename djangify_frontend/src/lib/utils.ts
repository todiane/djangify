// src/lib/utils.ts
import { format } from "date-fns";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | undefined): string {
  if (!date) return '';

  try {
    // Parse the date string into a Date object
    const parsedDate = new Date(date);

    // Check if the date is valid
    if (isNaN(parsedDate.getTime())) {
      return '';
    }

    return format(parsedDate, 'MMMM d, yyyy');
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
}
