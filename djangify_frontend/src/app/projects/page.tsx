import { FeaturedProject, ProjectCard, NewsletterForm } from '@/components/portfolio';

async function getProjects() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/projects/`);
  const data = await res.json();
  return data.data; // Assuming your API follows the standard response format
}

export default async function PortfolioPage() {
  const projects = await getProjects();
  const [featured, ...rest] = projects;
  const [secondProject, thirdProject, ...otherProjects] = rest;

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
          <FeaturedProject {...featured} />
        </div>

        {/* Secondary Featured Projects */}
        <div className="grid gap-6">
          <ProjectCard {...secondProject} />
          <ProjectCard {...thirdProject} />
        </div>
      </div>

      {/* Newsletter Section */}
      <div className="mb-12">
        <NewsletterForm />
      </div>

      {/* Other Projects Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {otherProjects.map((project: any) => (
          <ProjectCard key={project.slug} {...project} />
        ))}
      </div>
    </div>
  );
}
