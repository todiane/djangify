// src/app/blog/[slug]/loading.tsx
import { Skeleton } from "@/components/ui/skeleton";

export default function BlogPostLoading() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
      <div className="space-y-8">
        {/* Title Skeleton */}
        <div className="space-y-4">
          <Skeleton className="h-12 w-3/4" />
          <Skeleton className="h-4 w-48" />
        </div>

        {/* Featured Image Skeleton */}
        <Skeleton className="w-full aspect-[16/9] rounded-lg" />

        {/* Content Skeletons */}
        <div className="space-y-4">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-4/6" />
        </div>
      </div>
    </div>
  );
}
