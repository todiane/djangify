import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import type { Project } from './types';

interface FeaturedProjectProps extends Project { }

export function FeaturedProject({
  title,
  shortDescription,
  slug,
  featuredImage,
  technologies,
}: FeaturedProjectProps) {
  return (
    <Card className="overflow-hidden h-full">
      <div className="relative aspect-video">
        <img
          src={featuredImage}
          alt={title}
          className="object-cover w-full h-full"
        />
      </div>
      <CardContent className="p-6">
        <div className="flex flex-wrap gap-2 mb-3">
          {technologies.map((tech) => (
            <span
              key={tech.id}
              className="px-2 py-1 text-xs rounded-full bg-primary/10 text-primary"
            >
              {tech.name}
            </span>
          ))}
        </div>
        <h3 className="text-2xl font-semibold mb-2">{title}</h3>
        <p className="text-muted-foreground line-clamp-2">{shortDescription}</p>
        <Link href={`/projects/${slug}`} className="mt-4 block">
          <Button className="w-full">
            Read More <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
