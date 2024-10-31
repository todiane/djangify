// src/components/blog/SecondaryPost.tsx
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";

interface SecondaryPostProps {
  title: string;
  image: string;
  slug: string;
  date: string;
}

export function SecondaryPost({ title, image, slug, date }: SecondaryPostProps) {
  return (
    <Card className="overflow-hidden">
      <div className="aspect-[16/9] relative">
        <Image
          src={image}
          alt={title}
          fill
          className="object-cover"
        />
      </div>
      <CardContent className="p-4">
        <time className="text-sm text-slate-500">{date}</time>
        <h3 className="text-lg font-semibold mt-2 mb-3 line-clamp-2">
          <Link href={`/blog/${slug}`} className="hover:text-blue-600">
            {title}
          </Link>
        </h3>
        <Button asChild variant="outline" size="sm">
          <Link href={`/blog/${slug}`}>Read More</Link>
        </Button>
      </CardContent>
    </Card>
  );
}
