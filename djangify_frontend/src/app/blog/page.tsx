import { FeaturedPost } from "@/components/blog/FeaturedPost";
import { SecondaryPost } from "@/components/blog/SecondaryPost";
import { NewsletterForm } from "@/components/blog/NewsletterForm";
import { PostGrid } from "@/components/blog/PostGrid";

export default async function BlogPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Top Section with Featured Posts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-12">
        {/* Featured Post */}
        <div className="lg:col-span-7">
          <FeaturedPost
            title="5 Lessons For Next.js Performance Optimization"
            excerpt="Introduction to Next.js Performance Optimization. At Pagepro, we've spent years developing and optimizing high-traffic Next.js websites and apps for our clients..."
            image="/api/placeholder/800/600"
            slug="nextjs-performance-optimization"
            date="Oct 31, 2024"
          />
        </div>

        {/* Secondary Posts */}
        <div className="lg:col-span-5 space-y-6">
          <SecondaryPost
            title="React Native Pros and Cons"
            image="/api/placeholder/400/300"
            slug="react-native-pros-cons"
            date="Oct 30, 2024"
          />
          <SecondaryPost
            title="Next.js Middleware - What Is It and When to Use It"
            image="/api/placeholder/400/300"
            slug="nextjs-middleware-guide"
            date="Oct 29, 2024"
          />
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
        <PostGrid />
      </div>
    </div>
  );
}
