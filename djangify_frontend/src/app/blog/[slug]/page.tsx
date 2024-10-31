import { notFound } from "next/navigation";
import { BlogHeader } from "@/components/blog/BlogHeader";
import { BlogContent } from "@/components/blog/BlogContent";
import { RelatedPosts } from "@/components/blog/RelatedPosts";
import { CommentSection } from "@/components/blog/CommentSection";
import { blogApi } from "@/lib/api/blog";

interface BlogDetailPageProps {
  params: {
    slug: string;
  };
}

export default async function BlogDetailPage({ params }: BlogDetailPageProps) {
  try {
    const post = await blogApi.getPost(params.slug);
    const relatedPosts = await blogApi.getPosts({
      category: post.category.slug,
      page_size: 3,
    });

    return (
      <article className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <BlogHeader
          title={post.title}
          image={post.featured_image}
          category={post.category}
          publishedDate={post.published_date}
          commentCount={post.comments?.length ?? 0}
        />

        <BlogContent content={post.content} />

        <hr className="my-12 border-t border-gray-200" />

        <RelatedPosts posts={relatedPosts.results} />

        <hr className="my-12 border-t border-gray-200" />

        <CommentSection
          postId={post.id}
          postSlug={post.slug}
          initialComments={post.comments ?? []}
        />
      </article>
    );
  } catch (error) {
    notFound();
  }
}
