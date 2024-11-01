import api from '@/lib/api';

export interface Technology {
  id: number;
  name: string;
  slug: string;
  icon: string;
}

export interface Portfolio {
  id: number;
  title: string;
  slug: string;
  description: string;
  short_description: string;
  featured_image: string;
  technologies: Technology[];
  project_url?: string;
  github_url?: string;
  is_featured: boolean;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PortfolioFilters {
  technology?: string;
  search?: string;
  page?: number;
  is_featured?: boolean;
}

export const portfolioApi = {
  getPortfolioItems: async (filters?: PortfolioFilters): Promise<PaginatedResponse<Portfolio>> => {
    const params = new URLSearchParams();
    
    if (filters) {
      if (filters.technology) params.append('technology__slug', filters.technology);
      if (filters.search) params.append('search', filters.search);
      if (filters.page) params.append('page', filters.page.toString());
      if (filters.is_featured !== undefined) params.append('is_featured', filters.is_featured.toString());
    }

    const response = await api.get<PaginatedResponse<Portfolio>>(`/portfolio/projects/?${params}`);
    return response.data;
  },

  getPortfolioItem: async (slug: string): Promise<Portfolio> => {
    const response = await api.get<Portfolio>(`/portfolio/projects/${slug}/`);
    return response.data;
  },

  getTechnologies: async (): Promise<Technology[]> => {
    const response = await api.get<PaginatedResponse<Technology>>('/portfolio/technologies/');
    return response.data.results;
  },

  getFeaturedItems: async (): Promise<Portfolio[]> => {
    const response = await api.get<PaginatedResponse<Portfolio>>('/portfolio/projects/', {
      params: { is_featured: true }
    });
    return response.data.results;
  }
};
