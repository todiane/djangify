// src/components/blog/BlogHeader.tsx
import Image from "next/image";
import Link from "next/link";
import { formatDate } from "@/lib/utils";
import { MessageCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface BlogHeaderProps {
  title: string;
  image: string;
  category: {
    name: string;
    slug: string;
  };
  publishedDate: string;
  commentCount: number;
}

export function BlogHeader({
  title,
  image,
  category,
  publishedDate,
  commentCount,
}: BlogHeaderProps) {
  return (
    <header className="space-y-8 mb-12">
      <div className="aspect-[2/1] relative rounded-lg overflow-hidden">
        <Image
          src={image}
          alt={title}
          fill
          className="object-cover"
          priority
        />
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <Link href={`/blog/category/${category.slug}`}>
            <Badge variant="secondary" className="hover:bg-secondary/80">
              {category.name}
            </Badge>
          </Link>
          <h1 className="text-4xl font-bold tracking-tight">{title}</h1>
        </div>

        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <time dateTime={publishedDate}>{formatDate(publishedDate)}</time>
          <span>•</span>
          <div className="flex items-center gap-1">
            <MessageCircle className="h-4 w-4" />
            <span>{commentCount} comments</span>
          </div>
        </div>
      </div>
    </header>
  );
}
