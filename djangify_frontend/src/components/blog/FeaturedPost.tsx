// src/components/blog/FeaturedPost.tsx
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";

interface FeaturedPostProps {
  title: string;
  excerpt: string;
  image: string;
  slug: string;
  date: string;
}

export function FeaturedPost({ title, excerpt, image, slug, date }: FeaturedPostProps) {
  return (
    <Card className="overflow-hidden h-full">
      <div className="aspect-[16/9] relative">
        <Image
          src={image}
          alt={title}
          fill
          className="object-cover"
          priority
        />
      </div>
      <CardContent className="p-6">
        <time className="text-sm text-slate-500">{date}</time>
        <h2 className="text-2xl font-bold mt-2 mb-3 line-clamp-2">
          <Link href={`/blog/${slug}`} className="hover:text-blue-600">
            {title}
          </Link>
        </h2>
        <p className="text-slate-600 mb-4 line-clamp-3">{excerpt}</p>
        <Button asChild variant="outline">
          <Link href={`/blog/${slug}`}>Read More</Link>
        </Button>
      </CardContent>
    </Card>
  );
}
