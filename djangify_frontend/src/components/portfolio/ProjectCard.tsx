import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import type { Project } from './types';

interface ProjectCardProps extends Project { }

export function ProjectCard({
  title,
  shortDescription,
  slug,
  featuredImage,
  technologies,
}: ProjectCardProps) {
  return (
    <Card className="overflow-hidden h-full">
      <div className="relative aspect-video">
        <img
          src={featuredImage}
          alt={title}
          className="object-cover w-full h-full"
        />
      </div>
      <CardContent className="p-4">
        <div className="flex flex-wrap gap-1 mb-2">
          {technologies.slice(0, 3).map((tech) => (
            <span
              key={tech.id}
              className="px-2 py-0.5 text-xs rounded-full bg-primary/10 text-primary"
            >
              {tech.name}
            </span>
          ))}
        </div>
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <p className="text-muted-foreground text-sm line-clamp-2">
          {shortDescription}
        </p>
        <Link href={`/projects/${slug}`} className="mt-4 block">
          <Button variant="ghost" className="w-full">
            Read More <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
