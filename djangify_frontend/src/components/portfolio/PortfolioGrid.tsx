// src/components/portfolio/PortfolioGrid.tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Github, ExternalLink } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';
import type { Portfolio, Technology } from './types';
import { LoadingPortfolio } from "@/components/ui/LoadingPortfolio";
import { ErrorMessage } from "@/components/ui/ErrorMessage";

interface PortfolioGridProps {
  initialPortfolios: Portfolio[];
  technologies: Technology[];
}

export function PortfolioGrid({ initialPortfolios, technologies }: PortfolioGridProps) {
  const [selectedTech, setSelectedTech] = useState<string | null>(null);
  const [portfolios, setPortfolios] = useState(initialPortfolios);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const loaderRef = useRef<HTMLDivElement>(null);

  // Filter portfolios based on selected technology
  const filteredPortfolios = selectedTech
    ? portfolios.filter(portfolio =>
      portfolio.technologies.some(tech => tech.slug === selectedTech)
    )
    : portfolios;

  // Reset state when technology filter changes
  useEffect(() => {
    setPortfolios(initialPortfolios);
    setPage(1);
    setHasMore(true);
    setError(null);
  }, [selectedTech, initialPortfolios]);

  // Set up intersection observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const first = entries[0];
        if (first.isIntersecting && hasMore && !loading) {
          loadMorePortfolios();
        }
      },
      { threshold: 0.1 }
    );

    const currentLoader = loaderRef.current;
    if (currentLoader) {
      observer.observe(currentLoader);
    }

    return () => {
      if (currentLoader) {
        observer.unobserve(currentLoader);
      }
    };
  }, [hasMore, loading, selectedTech]);

  // Load more portfolios
  const loadMorePortfolios = async () => {
    try {
      setLoading(true);
      setError(null);

      const nextPage = page + 1;
      const response = await fetch(`/api/portfolio?page=${nextPage}${selectedTech ? `&technology=${selectedTech}` : ''}`);
      const data = await response.json();

      if (!response.ok) throw new Error(data.message || 'Failed to load more items');

      setPortfolios(prev => [...prev, ...data.results]);
      setPage(nextPage);
      setHasMore(!!data.next);
    } catch (err) {
      setError('Failed to load more items. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Retry loading on error
  const handleRetry = () => {
    setError(null);
    loadMorePortfolios();
  };

  return (
    <div className="space-y-8">
      {/* Technology Filter */}
      <div className="flex flex-wrap gap-2">
        <Badge
          variant={selectedTech === null ? "default" : "outline"}
          className="cursor-pointer"
          onClick={() => setSelectedTech(null)}
        >
          All
        </Badge>
        {technologies.map((tech) => (
          <Badge
            key={tech.slug}
            variant={selectedTech === tech.slug ? "default" : "outline"}
            className="cursor-pointer"
            onClick={() => setSelectedTech(tech.slug)}
          >
            {tech.name}
          </Badge>
        ))}
      </div>

      {/* Portfolio Grid */}
      <div className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPortfolios.map((portfolio) => (
            <Card key={portfolio.id} className="flex flex-col">
              <div className="aspect-video relative">
                <Image
                  src={portfolio.featuredImage}
                  alt={portfolio.title}
                  fill
                  className="object-cover rounded-t-lg"
                />
              </div>
              <CardContent className="flex-1 p-6">
                <h3 className="text-xl font-semibold mb-2">{portfolio.title}</h3>
                <p className="text-muted-foreground mb-4 line-clamp-2">
                  {portfolio.shortDescription}
                </p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {portfolio.technologies.map((tech) => (
                    <Badge key={tech.slug} variant="secondary">
                      {tech.name}
                    </Badge>
                  ))}
                </div>
              </CardContent>
              <CardFooter className="p-6 pt-0 gap-4">
                <Button asChild variant="outline" size="sm">
                  <Link href={`/portfolio/${portfolio.slug}`}>
                    View Details
                  </Link>
                </Button>
                <div className="flex gap-2 ml-auto">
                  {portfolio.githubUrl && (
                    <Button asChild size="icon" variant="ghost">
                      <a href={portfolio.githubUrl} target="_blank" rel="noopener noreferrer">
                        <Github className="h-4 w-4" />
                      </a>
                    </Button>
                  )}
                  {portfolio.projectUrl && (
                    <Button asChild size="icon" variant="ghost">
                      <a href={portfolio.projectUrl} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </Button>
                  )}
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Loading and Error States */}
        <div ref={loaderRef} className="mt-8">
          {loading && <LoadingPortfolio />}
          {error && (
            <ErrorMessage
              message={error}
              retry={handleRetry}
            />
          )}
          {!hasMore && !loading && !error && filteredPortfolios.length > 0 && (
            <p className="text-center text-muted-foreground">
              No more items to load
            </p>
          )}
          {!loading && !error && filteredPortfolios.length === 0 && (
            <p className="text-center text-muted-foreground">
              No items found for the selected technology
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
