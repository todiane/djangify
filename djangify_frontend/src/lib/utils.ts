// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import api from "./api";


export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Add to src/lib/api/blog.ts
export const blogApi = {
  // ... existing methods ...

  createComment: async (postSlug: string, comment: {
    name: string;
    email: string;
    content: string;
  }) => {
    const response = await api.post(`/blog/posts/${postSlug}/comments/`, comment);
    return response.data;
  },
};

