// src/components/blog/BlogPostCard.tsx
import { Card } from "@/components/ui/card";
import type { Post } from "@/lib/api/blog";

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

export function BlogPostCard({ post, isMain = false }: BlogPostCardProps) {
  return (
    <Card className="overflow-hidden group">
      <div className={`aspect-[16/9] relative ${isMain ? 'aspect-[16/9]' : 'aspect-[2/1]'}`}>
        <img
          src={post.featured_image}
          alt={post.title}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      <div className="p-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
          <time>{formatDate(post.published_date)}</time>
          <span>•</span>
          <span>{formatReadingTime(post.reading_time)}</span>
          <span>•</span>
          <span>{formatWordCount(post.word_count)}</span>
        </div>
        <h3 className="text-xl font-semibold mb-2 line-clamp-2">
          <a href={`/blog/${post.slug}`} className="hover:text-primary">
            {post.title}
          </a>
        </h3>
        <p className="text-muted-foreground line-clamp-2 mb-4">
          {post.excerpt}
        </p>
        <a
          href={`/blog/${post.slug}`}
          className="inline-flex items-center text-sm font-medium text-primary hover:underline"
        >
          Read More
        </a>
      </div>
    </Card>
  );
}
