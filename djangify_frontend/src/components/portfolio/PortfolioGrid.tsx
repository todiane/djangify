// src/components/portfolio/ProjectGrid.tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Github, ExternalLink } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';
import { Project, Technology, portfolioApi } from '@/lib/api/portfolio';
import { LoadingProjects } from "@/components/ui/LoadingPortfolio";
import { ErrorMessage } from "@/components/ui/ErrorMessage";

interface ProjectGridProps {
  initialProjects: Project[];
  technologies: Technology[];
}

export function ProjectGrid({ initialProjects, technologies }: ProjectGridProps) {
  const [selectedTech, setSelectedTech] = useState<string | null>(null);
  const [projects, setProjects] = useState(initialProjects);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const loaderRef = useRef<HTMLDivElement>(null);

  // Filter projects based on selected technology
  const filteredProjects = selectedTech
    ? projects.filter(project =>
      project.technologies.some(tech => tech.slug === selectedTech)
    )
    : projects;

  // Reset state when technology filter changes
  useEffect(() => {
    setProjects(initialProjects);
    setPage(1);
    setHasMore(true);
    setError(null);
  }, [selectedTech, initialProjects]);

  // Set up intersection observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const first = entries[0];
        if (first.isIntersecting && hasMore && !loading) {
          loadMoreProjects();
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

  // Load more projects
  const loadMoreProjects = async () => {
    try {
      setLoading(true);
      setError(null);

      const nextPage = page + 1;
      const response = await portfolioApi.getProjects({
        page: nextPage,
        technology: selectedTech || undefined,
      });

      setProjects(prev => [...prev, ...response.results]);
      setPage(nextPage);
      setHasMore(!!response.next);
    } catch (err) {
      setError('Failed to load more projects. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Retry loading on error
  const handleRetry = () => {
    setError(null);
    loadMoreProjects();
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

      {/* Projects Grid */}
      <div className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => (
            <Card key={project.id} className="flex flex-col">
              <div className="aspect-video relative">
                <Image
                  src={project.featured_image}
                  alt={project.title}
                  fill
                  className="object-cover rounded-t-lg"
                />
              </div>
              <CardContent className="flex-1 p-6">
                <h3 className="text-xl font-semibold mb-2">{project.title}</h3>
                <p className="text-muted-foreground mb-4 line-clamp-2">
                  {project.short_description}
                </p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.technologies.map((tech) => (
                    <Badge key={tech.slug} variant="secondary">
                      {tech.name}
                    </Badge>
                  ))}
                </div>
              </CardContent>
              <CardFooter className="p-6 pt-0 gap-4">
                <Button asChild variant="outline" size="sm">
                  <Link href={`/projects/${project.slug}`}>
                    View Details
                  </Link>
                </Button>
                <div className="flex gap-2 ml-auto">
                  {project.github_url && (
                    <Button asChild size="icon" variant="ghost">
                      <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                        <Github className="h-4 w-4" />
                      </a>
                    </Button>
                  )}
                  {project.project_url && (
                    <Button asChild size="icon" variant="ghost">
                      <a href={project.project_url} target="_blank" rel="noopener noreferrer">
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
          {loading && <LoadingProjects />}
          {error && (
            <ErrorMessage
              message={error}
              retry={handleRetry}
            />
          )}
          {!hasMore && !loading && !error && filteredProjects.length > 0 && (
            <p className="text-center text-muted-foreground">
              No more projects to load
            </p>
          )}
          {!loading && !error && filteredProjects.length === 0 && (
            <p className="text-center text-muted-foreground">
              No projects found for the selected technology
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
