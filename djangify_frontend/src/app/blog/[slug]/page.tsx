// src/app/blog/[slug]/page.tsx
import { notFound } from "next/navigation";
import { blogApi, Post } from "@/lib/api/blog";
import { Card } from "@/components/ui/card";
import { formatDate } from "@/lib/utils";

interface BlogPostPageProps {
  params: {
    slug: string;
  };
}

interface BlogPostResponse {
  status: string;
  data: Post;
  message: string;
}

export default async function BlogPostPage({ params }: BlogPostPageProps) {
  if (!params.slug) {
    notFound();
  }

  try {
    // Explicitly type the response

    // Add this to see the exact API call being made
    console.log('Fetching post with URL:', `/blog/posts/${params.slug}/`);

    const response = await blogApi.getPost(params.slug) as BlogPostResponse;
    const post = response.data;

    // Add this to verify the post data received
    console.log('Received post data:', post);

    if (!post) {
      notFound();
    }

    const formattedDate = formatDate(post.published_date);

    return (
      <article className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
        {/* Post Header */}
        <header className="space-y-4 mb-8">
          <h1 className="text-4xl font-bold tracking-tight">
            {post.title}
          </h1>

          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            {formattedDate && (
              <>
                <time dateTime={post.published_date}>
                  {formattedDate}
                </time>
                <span>•</span>
              </>
            )}
            <span>{post.reading_time} min read</span>
            <span>•</span>
            <span>{post.word_count} words</span>
          </div>
        </header>

        {/* Featured Image */}
        {post.featured_image && (
          <div className="relative aspect-video mb-8">
            <img
              src={post.featured_image}
              alt={post.title}
              className="rounded-lg object-cover w-full h-full"
            />
          </div>
        )}

        {/* Post Content */}
        <div
          className="prose prose-lg max-w-none prose-img:rounded-lg prose-a:text-primary"
          dangerouslySetInnerHTML={{ __html: post.content }}
        />

        {/* Tags and Category */}
        <footer className="mt-8 pt-8 border-t">
          {post.tags && post.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {post.tags.map((tag) => (
                <Card key={tag.slug} className="px-3 py-1 text-sm">
                  {tag.name}
                </Card>
              ))}
            </div>
          )}
          {post.category && (
            <p className="text-sm text-muted-foreground">
              Posted in {post.category.name}
            </p>
          )}
        </footer>
      </article>
    );
  } catch (error) {
    console.error('Error fetching blog post:', error);
    notFound();
  }
}
