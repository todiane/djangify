// src/lib/api/blog.ts
import api from '@/lib/api';

export interface Post {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  featured_image: string;
  category: {
    name: string;
    slug: string;
  };
  tags: Array<{
    name: string;
    slug: string;
  }>;
  status: 'draft' | 'published';
  published_date: string;
  created_at: string;
  updated_at: string;
  meta_description: string;
  is_featured: boolean;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PostFilters {
  category?: string;
  tag?: string;
  search?: string;
  page?: number;
  is_featured?: boolean;
}

export const blogApi = {
  // Get paginated list of posts
  getPosts: async (filters?: PostFilters): Promise<PaginatedResponse<Post>> => {
    const params = new URLSearchParams();

    if (filters) {
      if (filters.category) params.append('category__slug', filters.category);
      if (filters.tag) params.append('tags__slug', filters.tag);
      if (filters.search) params.append('search', filters.search);
      if (filters.page) params.append('page', filters.page.toString());
      if (filters.is_featured !== undefined) params.append('is_featured', filters.is_featured.toString());
    }

    const response = await api.get<PaginatedResponse<Post>>(`/blog/posts/?${params}`);
    return response.data;
  },

  // Get featured posts
  getFeaturedPosts: async (): Promise<Post[]> => {
    const response = await api.get<PaginatedResponse<Post>>('/blog/posts/', {
      params: {
        is_featured: true,
        ordering: '-published_date'
      }
    });
    return response.data.results;
  },

  // Get a single post by slug
  getPost: async (slug: string): Promise<Post> => {
    const response = await api.get<Post>(`/blog/posts/${slug}/`);
    return response.data;
  },

  // Get recent posts
  getRecentPosts: async (limit: number = 12): Promise<Post[]> => {
    const response = await api.get<PaginatedResponse<Post>>('/blog/posts/', {
      params: {
        page_size: limit,
        ordering: '-published_date'
      }
    });
    return response.data.results;
  },

  // Get categories
  getCategories: async () => {
    const response = await api.get('/blog/categories/');
    return response.data.results;
  },

  // Get tags
  getTags: async () => {
    const response = await api.get('/blog/tags/');
    return response.data.results;
  }
};
