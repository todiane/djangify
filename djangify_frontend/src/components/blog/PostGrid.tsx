// src/components/blog/PostGrid.tsx
'use client';

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loading } from "@/components/ui/Loading";
import { ErrorBoundary } from "@/components/ui/ErrorBoundary";
import Image from "next/image";
import Link from "next/link";
import type { Post } from "@/lib/api/blog";
import { blogApi } from "@/lib/api/blog";

interface PostGridProps {
  initialPosts: Post[];
}

export function PostGrid({ initialPosts }: PostGridProps) {
  const [posts, setPosts] = useState<Post[]>(initialPosts);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [hasMore, setHasMore] = useState(true);

  const loadMorePosts = async () => {
    try {
      setLoading(true);
      setError(null);
      const nextPage = page + 1;
      const response = await blogApi.getPosts({ page: nextPage });

      setPosts(currentPosts => [...currentPosts, ...response.results]);
      setPage(nextPage);
      setHasMore(!!response.next);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to load posts'));
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return <ErrorBoundary error={error} reset={() => setError(null)} />;
  }

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <Card key={post.id} className="overflow-hidden">
            <div className="aspect-[16/9] relative">
              <Image
                src={post.featured_image}
                alt={post.title}
                fill
                className="object-cover"
              />
            </div>
            <CardContent className="p-4">
              <time className="text-sm text-slate-500">
                {new Date(post.published_date).toLocaleDateString()}
              </time>
              <h3 className="text-lg font-semibold mt-2 mb-3 line-clamp-2">
                <Link href={`/blog/${post.slug}`} className="hover:text-blue-600">
                  {post.title}
                </Link>
              </h3>
              <Button asChild variant="outline" size="sm">
                <Link href={`/blog/${post.slug}`}>Read More</Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Loading and Load More */}
      <div className="flex justify-center">
        {loading ? (
          <Loading />
        ) : hasMore ? (
          <Button
            onClick={loadMorePosts}
            variant="outline"
            className="min-w-[200px]"
          >
            Load More Posts
          </Button>
        ) : (
          <p className="text-slate-500">No more posts to load</p>
        )}
      </div>
    </div>
  );
}
