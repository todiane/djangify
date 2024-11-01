// src/components/blog/FeaturedPostCard.tsx
import { Card } from "@/components/ui/card";
import type { Post } from "@/lib/api/blog";

interface FeaturedPostCardProps {
  post: Post & {
    reading_time: number;
    word_count: number;
  };
  isMain?: boolean;
}

export function FeaturedPostCard({ post, isMain = false }: FeaturedPostCardProps) {
  return (
    <Card className={`overflow-hidden group ${isMain ? 'aspect-[16/9]' : 'aspect-[2/1]'}`}>
      <div className="relative h-full">
        <img
          src={post.featured_image}
          alt={post.title}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-6">
          <div className="flex items-center gap-2 text-sm text-white/90 mb-2">
            <time>{new Date(post.published_date).toLocaleDateString()}</time>
            <span>•</span>
            <span>{post.reading_time} min read</span>
            <span>•</span>
            <span>{post.word_count} words</span>
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">
            <a href={`/blog/${post.slug}`} className="hover:underline">
              {post.title}
            </a>
          </h3>
          {isMain && (
            <p className="text-white/90 line-clamp-2">{post.excerpt}</p>
          )}
        </div>
      </div>
    </Card>
  );
}
