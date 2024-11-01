// src/lib/api/blog.ts
import api from '@/lib/api';


// Export all interfaces
export interface Comment {
  id: number;
  name: string;
  email: string;
  content: string;
  created_at: string;
  is_approved: boolean;
  post: number;
}

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
  comments: Comment[];
  reading_time?: number;
  word_count?: number;
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
  page_size?: number;
}

// Helper functions
const calculateReadingTime = (content: string | undefined): number => {
  if (!content) return 0;
  const wordsPerMinute = 200;
  const wordCount = content.trim().split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
};

const calculateWordCount = (content: string | undefined): number => {
  if (!content) return 0;
  return content.trim().split(/\s+/).length;
};

const enhancePost = (post: Post): Post => {
  return {
    ...post,
    reading_time: calculateReadingTime(post.content),
    word_count: calculateWordCount(post.content)
  };
};

export interface BlogPostResponse {
  status: string;
  data: Post;
  message: string;
}

// Blog API methods
export const blogApi = {
  getPosts: async (filters?: PostFilters): Promise<PaginatedResponse<Post>> => {
    try {
      const params = new URLSearchParams();

      if (filters) {
        if (filters.category) params.append('category__slug', filters.category);
        if (filters.tag) params.append('tags__slug', filters.tag);
        if (filters.search) params.append('search', filters.search);
        if (filters.page) params.append('page', filters.page.toString());
        if (filters.is_featured !== undefined) params.append('is_featured', filters.is_featured.toString());
        if (filters.page_size) params.append('page_size', filters.page_size.toString());
      }

      const response = await api.get<PaginatedResponse<Post>>(`/blog/posts/?${params}`);
      return {
        ...response.data,
        results: response.data.results.map(enhancePost)
      };
    } catch (error) {
      console.error('Error fetching posts:', error);
      throw error;
    }
  },

  getPost: async (slug: string): Promise<BlogPostResponse> => {
    try {
      console.log('Making API request to:', `/blog/posts/${slug}/`);
      const response = await api.get<BlogPostResponse>(`/blog/posts/${slug}/`);
      console.log('API response:', response.data);
      return response.data;
    } catch (error) {
      console.error(`Error fetching post with slug ${slug}:`, error);
      throw error;
    }
  },

  getFeaturedPosts: async (): Promise<Post[]> => {
    try {
      const response = await api.get<PaginatedResponse<Post>>('/blog/posts/', {
        params: {
          is_featured: true,
          ordering: '-published_date'
        }
      });
      return response.data.results.map(enhancePost);
    } catch (error) {
      console.error('Error fetching featured posts:', error);
      throw error;
    }
  },

  getRecentPosts: async (limit: number = 12): Promise<Post[]> => {
    try {
      const response = await api.get<PaginatedResponse<Post>>('/blog/posts/', {
        params: {
          page_size: limit,
          ordering: '-published_date'
        }
      });
      return response.data.results.map(enhancePost);
    } catch (error) {
      console.error('Error fetching recent posts:', error);
      throw error;
    }
  },

  getCategories: async () => {
    try {
      const response = await api.get('/blog/categories/');
      return response.data.results;
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  },

  getTags: async () => {
    try {
      const response = await api.get('/blog/tags/');
      return response.data.results;
    } catch (error) {
      console.error('Error fetching tags:', error);
      throw error;
    }
  },

  createComment: async (postSlug: string, comment: {
    name: string;
    email: string;
    content: string;
  }): Promise<Comment> => {
    try {
      const response = await api.post<Comment>(`/blog/posts/${postSlug}/comments/`, comment);
      return response.data;
    } catch (error) {
      console.error('Error creating comment:', error);
      throw error;
    }
  }
};
