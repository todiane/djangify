import { cn } from "@/lib/utils";

interface FilteredLoadingProjectsProps {
  columns?: number;
}

export function FilteredLoadingProjects({ columns = 3 }: FilteredLoadingProjectsProps) {
  return (
    <div
      className={cn(
        "grid gap-6 animate-in fade-in-0",
        columns === 3 && "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
        columns === 2 && "grid-cols-1 md:grid-cols-2",
      )}
    >
      {[...Array(columns)].map((_, i) => (
        <div
          key={i}
          className="rounded-lg border bg-card text-card-foreground shadow-sm overflow-hidden"
        >
          <div className="aspect-video bg-muted animate-pulse" />
          <div className="p-6 space-y-4">
            {/* Title skeleton */}
            <div className="h-7 bg-muted animate-pulse rounded w-3/4" />

            {/* Description skeleton */}
            <div className="space-y-2">
              <div className="h-4 bg-muted animate-pulse rounded w-full" />
              <div className="h-4 bg-muted animate-pulse rounded w-2/3" />
            </div>

            {/* Technology badges skeleton */}
            <div className="flex flex-wrap gap-2">
              <div className="h-6 w-16 bg-muted animate-pulse rounded" />
              <div className="h-6 w-20 bg-muted animate-pulse rounded" />
              <div className="h-6 w-14 bg-muted animate-pulse rounded" />
            </div>

            {/* Buttons skeleton */}
            <div className="flex justify-between items-center pt-4">
              <div className="h-9 w-24 bg-muted animate-pulse rounded" />
              <div className="flex gap-2">
                <div className="h-8 w-8 bg-muted animate-pulse rounded" />
                <div className="h-8 w-8 bg-muted animate-pulse rounded" />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
