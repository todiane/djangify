import { Loading } from "@/components/ui/Loading";

export default function BlogLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="min-h-[600px] flex items-center justify-center">
        <Loading />
      </div>
    </div>
  );
}
// Compare this snippet from djangify_frontend/src/components/blog/FeaturedPost.tsx: