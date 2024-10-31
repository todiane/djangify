// src/components/ui/ErrorMessage.tsx
import { AlertCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

interface ErrorMessageProps {
  title?: string;
  message: string;
  retry?: () => void;
}

export function ErrorMessage({
  title = "Error",
  message,
  retry
}: ErrorMessageProps) {
  return (
    <Alert variant="destructive" className="mx-auto max-w-2xl">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription className="mt-2">
        <p>{message}</p>
        {retry && (
          <Button
            variant="outline"
            onClick={retry}
            className="mt-4"
          >
            Try Again
          </Button>
        )}
      </AlertDescription>
    </Alert>
  );
}
// src/components/ui/ErrorMessage.tsx