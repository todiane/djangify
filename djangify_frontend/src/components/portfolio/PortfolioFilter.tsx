// src/components/portfolio/PortfolioFilter.tsx
import { Button } from '@/components/ui/button';
import { Check } from 'lucide-react';

interface Technology {
  name: string;
  slug: string;
}

interface PortfolioFilterProps {
  technologies: Technology[];
  selectedTech: string | null;
  onSelectTech: (slug: string | null) => void;
}

export function PortfolioFilter({
  technologies,
  selectedTech,
  onSelectTech,
}: PortfolioFilterProps) {
  return (
    <div className="flex flex-wrap gap-2 mb-8">
      <Button
        variant={selectedTech === null ? "default" : "outline"}
        onClick={() => onSelectTech(null)}
        className="h-8"
      >
        All
        {selectedTech === null && <Check className="ml-2 h-4 w-4" />}
      </Button>
      {technologies.map((tech) => (
        <Button
          key={tech.slug}
          variant={selectedTech === tech.slug ? "default" : "outline"}
          onClick={() => onSelectTech(tech.slug)}
          className="h-8"
        >
          {tech.name}
          {selectedTech === tech.slug && <Check className="ml-2 h-4 w-4" />}
        </Button>
      ))}
    </div>
  );
}
