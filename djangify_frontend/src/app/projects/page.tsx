// src/app/projects/page.tsx
import { FeaturedProject, ProjectCard } from '../../components/portfolio';
import { NewsletterForm } from '../../components/blog/NewsletterForm';
import type { Project } from '../../components/portfolio/types';

async function getProjects() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/projects/`);
  if (!res.ok) throw new Error('Failed to fetch projects');
  const data = await res.json();
  return data;
}

export default async function ProjectsPage() {
  const data = await getProjects();
  const allProjects = data.results as Project[];

  // Filter featured projects
  const featuredProjects = allProjects.filter(project => project.isFeatured);
  const otherProjects = allProjects.filter(project => !project.isFeatured);

  const mainFeature = featuredProjects[0];
  const secondaryFeatures = featuredProjects.slice(1, 3);

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4">My Projects</h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Explore my latest work and side projects. Each project is crafted with attention to detail and modern technologies.
        </p>
      </div>

      {/* Featured Projects Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-12">
        {/* Main Featured Project */}
        <div className="md:row-span-2">
          {mainFeature && <FeaturedProject {...mainFeature} />}
        </div>

        {/* Secondary Featured Projects */}
        <div className="grid gap-6">
          {secondaryFeatures.map((project) => (
            <ProjectCard key={project.id} {...project} />
          ))}
        </div>
      </div>

      {/* Newsletter Section */}
      <div className="mb-12">
        <NewsletterForm />
      </div>

      {/* Project Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {otherProjects.map((project) => (
          <ProjectCard key={project.id} {...project} />
        ))}
      </div>
    </div>
  );
}
