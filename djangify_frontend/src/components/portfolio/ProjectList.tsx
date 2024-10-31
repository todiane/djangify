// src/components/portfolio/ProjectList.tsx
import { ProjectCard } from './ProjectCard';

interface Project {
  id: number;
  title: string;
  shortDescription: string;
  slug: string;
  featuredImage: string;
  technologies: Array<{ name: string; slug: string }>;
}

interface ProjectListProps {
  projects: Project[];
}

export function ProjectList({ projects }: ProjectListProps) {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {projects.map((project) => (
        <ProjectCard key={project.id} {...project} />
      ))}
    </div>
  );
}