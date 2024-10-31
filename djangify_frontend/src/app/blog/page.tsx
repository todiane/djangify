import { Suspense } from "react";
import { FeaturedPost } from "@/components/blog/FeaturedPost";
import { SecondaryPost } from "@/components/blog/SecondaryPost";
import { NewsletterForm } from "@/components/blog/NewsletterForm";
import { PostGrid } from "@/components/blog/PostGrid";
import { Loading } from "@/components/ui/Loading";
import { blogApi } from "@/lib/api/blog";

export const revalidate = 3600; // Revalidate every hour

export default async function BlogPage() {
  const [featuredPosts, recentPosts] = await Promise.all([
    blogApi.getFeaturedPosts(),
    blogApi.getRecentPosts(12)
  ]);

  const mainFeature = featuredPosts[0];
  const secondaryFeatures = featuredPosts.slice(1, 3);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Suspense fallback={<Loading />}>
        {/* Featured Posts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-12">
          <div className="lg:col-span-7">
            {mainFeature && (
              <FeaturedPost
                title={mainFeature.title}
                excerpt={mainFeature.excerpt}
                image={mainFeature.featured_image}
                slug={mainFeature.slug}
                date={new Date(mainFeature.published_date).toLocaleDateString()}
              />
            )}
          </div>

          <div className="lg:col-span-5 space-y-6">
            {secondaryFeatures.map((post) => (
              <SecondaryPost
                key={post.id}
                title={post.title}
                image={post.featured_image}
                slug={post.slug}
                date={new Date(post.published_date).toLocaleDateString()}
              />
            ))}
          </div>
        </div>

        {/* Newsletter Section */}
        <div className="bg-slate-50 rounded-lg p-8 mb-12">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4">Stay Updated</h2>
            <p className="text-slate-600 mb-6">
              Subscribe to our newsletter for the latest articles, tutorials, and insights
              about web development, React, and Next.js.
            </p>
            <NewsletterForm />
          </div>
        </div>

        {/* Recent Posts Grid */}
        <div className="space-y-8">
          <h2 className="text-2xl font-bold">Recent Posts</h2>
          <PostGrid initialPosts={recentPosts} />
        </div>
      </Suspense>
    </div>
  );
}
// Compare this snippet from djangify_frontend/src/components/blog/SecondaryPost.tsx: