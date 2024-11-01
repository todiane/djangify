import { Suspense } from 'react';
import { notFound } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Github, ExternalLink } from "lucide-react";
import Image from 'next/image';
import { PortfolioLightbox } from "@/components/portfolio/PortfolioLightbox";
import { portfolioApi } from '@/lib/api/portfolio';
import type { Technology } from '@/lib/api/portfolio';

interface PageProps {
  params: {
    slug: string;
  };
}

export const metadata = {
  title: 'Project Details | Djangify',
  description: 'Detailed information about this project',
};

export default async function PortfolioProjectPage({ params }: PageProps) {
  try {
    const project = await portfolioApi.getPortfolioItem(params.slug);

    if (!project) {
      notFound();
    }

    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-8">
          <div className="space-y-4">
            <h1 className="text-4xl font-bold tracking-tight">{project.title}</h1>
            <p className="text-xl text-muted-foreground">{project.short_description}</p>
          </div>

          <div className="aspect-video relative rounded-lg overflow-hidden">
            <Image
              src={project.featured_image}
              alt={project.title}
              fill
              className="object-cover"
              priority
            />
          </div>

          <div className="flex flex-wrap gap-4">
            {project.github_url && (
              <Button asChild>
                <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                  <Github className="mr-2 h-4 w-4" />
                  View Source
                </a>
              </Button>
            )}
            {project.project_url && (
              <Button asChild>
                <a href={project.project_url} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Live Demo
                </a>
              </Button>
            )}
          </div>

          <div className="prose max-w-none dark:prose-invert">
            <div dangerouslySetInnerHTML={{ __html: project.description }} />
          </div>

          {project.technologies.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold">Technologies Used</h2>
              <div className="flex flex-wrap gap-2">
                {project.technologies.map((tech: Technology) => (
                  <span
                    key={tech.id}
                    className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                  >
                    {tech.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error fetching project:', error);
    notFound();
  }
}
