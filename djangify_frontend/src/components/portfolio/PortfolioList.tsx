// src/components/portfolio/ProjectList.tsx
import { PortfolioCard } from './PortfolioCard';
import type { Portfolio } from './types';

interface PortfolioListProps {
  id: number;
  title: string;
  shortDescription: string;
  slug: string;
  featuredImage: string;
  technologies: Array<{ name: string; slug: string }>;
}

interface PortfolioListProps {
  portfolios: Portfolio[];  // Changed from projects
}


export function PortfolioList({ portfolios }: PortfolioListProps) {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {portfolios.map((portfolio) => (
        <PortfolioCard key={portfolio.id} {...portfolio} />
      ))}
    </div>
  );
}