// src/components/ui/LoadingProjects.tsx
export function LoadingProjects() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <div
          key={i}
          className="rounded-lg border bg-card text-card-foreground shadow-sm"
        >
          <div className="aspect-video bg-muted animate-pulse" />
          <div className="p-6 space-y-4">
            <div className="h-6 bg-muted animate-pulse rounded" />
            <div className="space-y-2">
              <div className="h-4 bg-muted animate-pulse rounded w-3/4" />
              <div className="h-4 bg-muted animate-pulse rounded w-1/2" />
            </div>
            <div className="flex gap-2">
              <div className="h-6 w-16 bg-muted animate-pulse rounded" />
              <div className="h-6 w-16 bg-muted animate-pulse rounded" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
