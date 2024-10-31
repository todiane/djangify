// src/components/blog/NewsletterForm.tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function NewsletterForm() {
  return (
    <form className="max-w-md mx-auto flex gap-2">
      <Input
        type="email"
        placeholder="Enter your email"
        className="flex-1"
      />
      <Button type="submit">Subscribe</Button>
    </form>
  );
}
