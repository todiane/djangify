import { FeaturedPosts } from "@/components/blog/FeaturedPosts";
import { BlogPostCard } from "@/components/blog/BlogPostCard";
import { blogApi } from "@/lib/api/blog";
import type { Post } from "@/lib/api/blog";

export const revalidate = 3600; // Revalidate every hour

// Utility functions for calculating reading time and word count
function calculateReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const wordCount = content.trim().split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
}

function calculateWordCount(content: string): number {
  return content.trim().split(/\s+/).length;
}

export default async function BlogPage() {
  try {
    // Fetch all posts
    const data = await blogApi.getPosts({
      page_size: 12 // Adjust based on how many posts you want to show
    });

    // Add computed properties to posts
    const posts = data.results.map(post => ({
      ...post,
      reading_time: calculateReadingTime(post.content),
      word_count: calculateWordCount(post.content)
    }));

    // Separate featured and recent posts
    const featuredPosts = posts.filter(post => post.is_featured);
    const recentPosts = posts.filter(post => !post.is_featured);

    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Blog Header */}
        <div className="space-y-4 mb-8">
          <h1 className="text-4xl font-bold tracking-tight">Blog</h1>
          <p className="text-lg text-muted-foreground">
            Welcome to my blog where I share insights and experiences about web
            development, coding tutorials, and tech industry perspectives.
          </p>
        </div>

        {/* Featured Posts Section */}
        {featuredPosts.length > 0 && (
          <div className="mb-16">
            <FeaturedPosts posts={featuredPosts.slice(0, 3)} />
          </div>
        )}

        {/* Recent Posts Grid */}
        <div className="space-y-8">
          <h2 className="text-2xl font-bold">Recent Posts</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentPosts.map((post) => (
              <BlogPostCard
                key={post.id}
                post={{
                  ...post,
                  reading_time: post.reading_time || 0,
                  word_count: post.word_count || 0
                }}
              />
            ))}
          </div>
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error fetching blog posts:', error);
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <div className="rounded-lg bg-red-50 p-4">
          <p className="text-red-700">Failed to load blog posts</p>
        </div>
      </div>
    );
  }
}
