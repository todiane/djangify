// src/components/blog/PostGrid.tsx
import { Card, CardContent } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export function PostGrid() {
  // This would normally fetch from your API
  const posts = Array(12).fill({
    title: "Sample Blog Post Title",
    image: "/api/placeholder/400/300",
    slug: "sample-post",
    date: "Oct 28, 2024"
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {posts.map((post, index) => (
        <Card key={index} className="overflow-hidden">
          <div className="aspect-[16/9] relative">
            <Image
              src={post.image}
              alt={post.title}
              fill
              className="object-cover"
            />
          </div>
          <CardContent className="p-4">
            <time className="text-sm text-slate-500">{post.date}</time>
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
  );
}
