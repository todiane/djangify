import { cn } from "@/lib/utils";

interface BlogContentProps {
  content: string;
  className?: string;
}

export function BlogContent({ content, className }: BlogContentProps) {
  return (
    <div className={cn(
      "prose prose-slate max-w-none",
      "prose-headings:font-semibold prose-headings:tracking-tight",
      "prose-a:text-primary prose-a:no-underline hover:prose-a:underline",
      "prose-img:rounded-lg",
      className
    )}>
      {/* If using markdown or a rich text editor, you'll need to parse the content */}
      <div dangerouslySetInnerHTML={{ __html: content }} />
    </div>
  );
}
