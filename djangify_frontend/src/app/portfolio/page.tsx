import { Suspense } from 'react';
import { PortfolioGrid } from "@/components/portfolio/PortfolioGrid";
import { LoadingPortfolio } from "@/components/ui/LoadingPortfolio";
import { ErrorMessage } from "@/components/ui/ErrorMessage";
import { portfolioApi } from '@/lib/api/portfolio';

export const metadata = {
  title: 'Portfolio | Djangify',
  description: 'Explore my portfolio of web development projects and applications',
};

export default async function PortfolioPage() {
  try {
    // Fetch initial data
    const [portfolioItems, technologies] = await Promise.all([
      portfolioApi.getPortfolioItems(),
      portfolioApi.getTechnologies(),
    ]);

    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-6">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">Portfolio</h1>
            <p className="text-muted-foreground">
              Explore my latest web development work and projects.
            </p>
          </div>

          <Suspense fallback={<LoadingPortfolio />}>
            <PortfolioGrid
              initialItems={portfolioItems.results}
              technologies={technologies}
            />
          </Suspense>
        </div>
      </div>
    );
  } catch (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <ErrorMessage
          title="Failed to load portfolio"
          message="There was an error loading the portfolio items. Please try again later."
        />
      </div>
    );
  }
}
