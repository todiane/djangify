// src/app/projects/[slug]/page.tsx
'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Github, ExternalLink } from 'lucide-react';
import { ProjectLightbox } from "@/components/portfolio/ProjectLightbox";
import { portfolioApi } from '@/lib/api/portfolio';
import type { Project } from '@/lib/api/portfolio';

interface ProjectPageProps {
  params: {
    slug: string;
  };
}

export default function ProjectPage({ params }: ProjectPageProps) {
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxIndex, setLightboxIndex] = useState(0);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const projectData = await portfolioApi.getProject(params.slug);
        setProject(projectData);
      } catch {
        notFound();
      } finally {
        setLoading(false);
      }
    };
    fetchProject();
  }, [params.slug]);

  if (loading) {
    return <div>Loading...</div>; // You can replace this with a proper loading skeleton
  }

  if (!project) {
    return notFound();
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="space-y-8">
        {/* Project Header */}
        <div className="space-y-4">
          <h1 className="text-4xl font-bold">{project.title}</h1>
          <div className="flex flex-wrap gap-2">
            {project.technologies.map((tech) => (
              <Badge key={tech.slug} variant="secondary">
                {tech.name}
              </Badge>
            ))}
          </div>
          <div className="flex gap-4">
            {project.github_url && (
              <Button asChild variant="outline">
                <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                  <Github className="mr-2 h-4 w-4" /> View Source
                </a>
              </Button>
            )}
            {project.project_url && (
              <Button asChild>
                <a href={project.project_url} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="mr-2 h-4 w-4" /> Live Demo
                </a>
              </Button>
            )}
          </div>
        </div>

        {/* Featured Image */}
        <div className="aspect-video relative rounded-lg overflow-hidden">
          <Image
            src={project.featured_image}
            alt={project.title}
            fill
            className="object-cover"
            priority
          />
        </div>

        {/* Project Images Grid */}
        {project.images.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {project.images.map((image, index) => (
              <Card
                key={image.id}
                className="overflow-hidden cursor-pointer transition-transform hover:scale-[1.02]"
                onClick={() => {
                  setLightboxIndex(index);
                  setLightboxOpen(true);
                }}
              >
                <div className="aspect-video relative">
                  <Image
                    src={image.image}
                    alt={image.caption}
                    fill
                    className="object-cover"
                  />
                </div>
                <CardContent className="p-2">
                  <p className="text-sm text-muted-foreground">{image.caption}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Project Description */}
        <div className="prose max-w-none">
          <div dangerouslySetInnerHTML={{ __html: project.description }} />
        </div>

        {/* Lightbox Component */}
        <ProjectLightbox
          images={project.images}
          initialIndex={lightboxIndex}
          isOpen={lightboxOpen}
          onClose={() => setLightboxOpen(false)}
        />
      </div>
    </div>
  );
}
// Compare this snippet from djangify_frontend/src/components/portfolio/ProjectLightbox.tsx: