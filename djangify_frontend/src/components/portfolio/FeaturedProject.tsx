import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

interface FeaturedProjectProps {
  title: string;
  description: string;
  slug: string;
  imageSrc: string;
  technologies: string[];
}

export function FeaturedProject({
  title,
  description,
  slug,
  imageSrc,
  technologies
}: FeaturedProjectProps) {
  return (
    <Card className="overflow-hidden h-full">
      <div className="relative aspect-video">
        <img
          src={imageSrc}
          alt={title}
          className="object-cover w-full h-full"
        />
      </div>
      <CardContent className="p-6">
        <div className="flex flex-wrap gap-2 mb-3">
          {technologies.map((tech) => (
            <span
              key={tech}
              className="px-2 py-1 text-xs rounded-full bg-primary/10 text-primary"
            >
              {tech}
            </span>
          ))}
        </div>
        <h3 className="text-2xl font-semibold mb-2">{title}</h3>
        <p className="text-muted-foreground line-clamp-2">{description}</p>
      </CardContent>
      <CardFooter className="p-6 pt-0">
        <Link href={`/projects/${slug}`} className="w-full">
          <Button className="w-full">
            Read More <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
}

// src/components/portfolio/ProjectCard.tsx
export function ProjectCard({
  title,
  description,
  slug,
  imageSrc,
  technologies
}: FeaturedProjectProps) {
  return (
    <Card className="overflow-hidden h-full">
      <div className="relative aspect-video">
        <img
          src={imageSrc}
          alt={title}
          className="object-cover w-full h-full"
        />
      </div>
      <CardContent className="p-4">
        <div className="flex flex-wrap gap-1 mb-2">
          {technologies.slice(0, 3).map((tech) => (
            <span
              key={tech}
              className="px-2 py-0.5 text-xs rounded-full bg-primary/10 text-primary"
            >
              {tech}
            </span>
          ))}
        </div>
        <h3 className="text-lg font-semibold mb-1">{title}</h3>
        <p className="text-muted-foreground text-sm line-clamp-2">{description}</p>
      </CardContent>
      <CardFooter className="p-4 pt-0">
        <Link href={`/projects/${slug}`} className="w-full">
          <Button variant="ghost" className="w-full">
            Read More <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
}

// src/components/portfolio/NewsletterForm.tsx
export function NewsletterForm() {
  return (
    <Card className="bg-primary/5 border-0">
      <CardContent className="p-6">
        <div className="text-center mb-4">
          <h3 className="text-xl font-semibold mb-2">Stay Updated</h3>
          <p className="text-muted-foreground">
            Get notified about new projects and updates.
          </p>
        </div>
        <form className="flex gap-2">
          <input
            type="email"
            placeholder="Enter your email"
            className="flex-1 px-4 py-2 rounded-md border focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <Button>Subscribe</Button>
        </form>
      </CardContent>
    </Card>
  );
}

// src/components/portfolio/RelatedProjects.tsx
interface RelatedProjectProps {
  projects: Array<{
    title: string;
    slug: string;
    imageSrc: string;
  }>;
}

export function RelatedProjects({ projects }: RelatedProjectProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {projects.map((project) => (
        <Link
          key={project.slug}
          href={`/projects/${project.slug}`}
          className="group relative aspect-video rounded-lg overflow-hidden"
        >
          <img
            src={project.imageSrc}
            alt={project.title}
            className="object-cover w-full h-full transition-transform group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <p className="text-white font-medium">Read More</p>
          </div>
        </Link>
      ))}
    </div>
  );
}
