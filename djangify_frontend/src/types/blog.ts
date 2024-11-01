// src/types/blog.ts
export interface Category {
  name: string;
  slug: string;
}

export interface Tag {
  name: string;
  slug: string;
}

export interface Comment {
  id: number;
  name: string;
  email: string;
  content: string;
  created_at: string;
  is_approved: boolean;
}

export interface Post {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  featured_image: string;
  category: Category;
  tags: Tag[];
  status: 'draft' | 'published';
  published_date: string;
  created_at: string;
  updated_at: string;
  is_featured: boolean;
  comments?: Comment[];
  reading_time?: number;
  word_count?: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
