// src/components/blog/BlogCard.tsx
import Link from 'next/link';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

interface BlogCardProps {
  title: string;
  excerpt: string;
  slug: string;
  featuredImage: string;
  publishedDate: string;
  category?: string;
  tags?: string[];
}

export function BlogCard({
  title,
  excerpt,
  slug,
  featuredImage,
  publishedDate,
  category,
  tags
}: BlogCardProps) {
  return (
    <Card className="overflow-hidden h-full flex flex-col">
      <div className="relative aspect-video">
        <img
          src={featuredImage}
          alt={title}
          className="object-cover w-full h-full"
        />
      </div>
      <CardContent className="p-4 flex-grow">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
          {category && (
            <span className="px-2 py-1 bg-primary/10 rounded-full text-primary text-xs">
              {category}
            </span>
          )}
          <time>{new Date(publishedDate).toLocaleDateString()}</time>
        </div>
        <h3 className="text-lg font-semibold mb-2 line-clamp-2">
          <Link href={`/blog/${slug}`} className="hover:text-primary">
            {title}
          </Link>
        </h3>
        <p className="text-muted-foreground text-sm line-clamp-2">{excerpt}</p>
      </CardContent>
      <CardFooter className="p-4 pt-0">
        <Link href={`/blog/${slug}`} className="w-full">
          <Button variant="ghost" className="w-full">
            Read More <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
}
