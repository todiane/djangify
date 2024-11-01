// src/components/portfolio/ProjectList.tsx
import { PortfolioCard } from './PortfolioCard';

interface Project {
  id: number;
  title: string;
  shortDescription: string;
  slug: string;
  featuredImage: string;
  technologies: Array<{ name: string; slug: string }>;
}

interface PortfolioListProps {
  projects: Project[];
}

export function PortfolioList({ portfolio }: PortfolioListProps) {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {portfolio.map((portfolio) => (
        <PortfolioCard key={portfolio.id} {...project} />
      ))}
    </div>
  );
}