// src/components/blog/BlogPostCard.tsx
import { Card } from "@/components/ui/card";
import type { Post } from "@/lib/api/blog";
import Link from "next/link";

function formatDate(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
}

function formatReadingTime(minutes: number | undefined) {
  return `Read time: ${minutes ?? 0} min`;
}

function formatWordCount(count: number | undefined) {
  return `Word Count: ${count ?? 0}`;
}

interface BlogPostCardProps {
  post: Post;
  isMain?: boolean;
}



export function BlogPostCard({ post }: BlogPostCardProps): JSX.Element {
  return (
    <Card className="overflow-hidden group">
      <Link href={`/blog/${post.slug}`}>
        <div className="aspect-[16/9] relative">
          <img
            src={post.featured_image}
            alt={post.title}
            className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      </Link>
      <div className="p-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
          <time>{formatDate(post.published_date)}</time>
          <span>•</span>
          <span>{post.reading_time} min read</span>
          <span>•</span>
          <span>{post.word_count} words</span>
        </div>
        <h3 className="text-xl font-semibold mb-2 line-clamp-2">
          <Link href={`/blog/${post.slug}`} className="hover:text-primary">
            {post.title}
          </Link>
        </h3>
        <p className="text-muted-foreground line-clamp-2 mb-4">
          {post.excerpt}
        </p>
        <Link
          href={`/blog/${post.slug}`}
          className="inline-flex items-center text-sm font-medium text-primary hover:underline"
        >
          Read More
        </Link>
      </div>
    </Card>
  );
}

