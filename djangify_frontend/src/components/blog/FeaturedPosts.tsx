import Link from "next/link";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface Post {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image: string;
  published_date: string;
}

interface FeaturedPostsProps {
  posts: Post[];
}

export function FeaturedPosts({ posts }: FeaturedPostsProps) {
  if (posts.length === 0) return null;

  const [mainPost, ...secondaryPosts] = posts;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      {/* Main Featured Post */}
      <div className="lg:col-span-8">
        <Link href={`/blog/${mainPost.slug}`}>
          <Card className="group relative overflow-hidden">
            <div className="aspect-[16/10]">
              <img
                src={mainPost.featured_image}
                alt={mainPost.title}
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent" />
              <div className="absolute bottom-0 left-0 right-0 p-6">
                <p className="text-sm text-white/80 mb-2">
                  {new Date(mainPost.published_date).toLocaleDateString()}
                </p>
                <h2 className="text-2xl font-bold text-white mb-2">
                  {mainPost.title}
                </h2>
                <p className="text-white/90 line-clamp-2">{mainPost.excerpt}</p>
              </div>
            </div>
          </Card>
        </Link>
      </div>

      {/* Secondary Featured Posts */}
      <div className="lg:col-span-4 grid grid-cols-1 gap-6">
        {secondaryPosts.slice(0, 2).map((post) => (
          <Link key={post.id} href={`/blog/${post.slug}`}>
            <Card className="group relative overflow-hidden">
              <div className="aspect-[16/9]">
                <img
                  src={post.featured_image}
                  alt={post.title}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent" />
                <div className="absolute bottom-0 left-0 right-0 p-4">
                  <p className="text-sm text-white/80 mb-1">
                    {new Date(post.published_date).toLocaleDateString()}
                  </p>
                  <h3 className="text-lg font-bold text-white line-clamp-2">
                    {post.title}
                  </h3>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
