import { Card } from "@/components/ui/card"

interface Post {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image: string;
  published_date: string;
  reading_time: number;
}

interface FeaturedPostsProps {
  posts: Post[];
}

interface FeaturedPostCardProps {
  post: Post;
  isMain?: boolean;
}

export function FeaturedPosts({ posts }: FeaturedPostsProps) {
  if (!posts?.length) return null;

  const [mainPost, ...secondaryPosts] = posts;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-12">
      {/* Main Featured Post - Larger Size */}
      <div className="lg:col-span-8">
        <FeaturedPostCard post={mainPost} isMain={true} />
      </div>

      {/* Secondary Featured Posts - Smaller Size */}
      <div className="lg:col-span-4 space-y-14">
        {secondaryPosts.slice(0, 2).map((post) => (
          <FeaturedPostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  )
}

export function FeaturedPostCard({ post, isMain = false }: FeaturedPostCardProps) {
  return (
    <Card className="group overflow-hidden">
      <a href={`/blog/${post.slug}`} className="block">
        <div className={`relative ${isMain ? 'aspect-[16/9]' : 'aspect-[2/1]'}`}>
          <img
            src={post.featured_image}
            alt={post.title}
            className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />

          <div className="absolute bottom-0 left-0 right-0 p-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-white/90">
                <time>{new Date(post.published_date).toLocaleDateString()}</time>
                <span>•</span>
                <span>{post.reading_time} min read</span>
              </div>

              <h3 className={`${isMain ? 'text-3xl' : 'text-xl'} font-bold text-white line-clamp-2`}>
                {post.title}
              </h3>

              {isMain && (
                <p className="text-white/90 line-clamp-2 text-lg">
                  {post.excerpt}
                </p>
              )}
            </div>
          </div>
        </div>
      </a>
    </Card>
  )
}
