// src/components/portfolio/types.ts
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
  shortDescription: string;
  description: string;
  featuredImage: string;
  projectUrl?: string;
  githubUrl?: string;
  isFeatured: boolean;
  technologies: Technology[];
  images: { id: number; image: string; caption: string }[];
}
