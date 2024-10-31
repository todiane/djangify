import { useState } from "react";
import { Button } from "@/components/ui/button";
import ThemeToggle from "@/components/theme-toggle";
import { Menu, X, Home, Briefcase, BookOpen, User, Mail, Search } from "lucide-react";

import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  const mainNavItems = [
    { label: "Home", icon: Home, href: "/" },
    { label: "Projects", icon: Briefcase, href: "/projects" },
    { label: "Blog", icon: BookOpen, href: "/blog" },
    { label: "About", icon: User, href: "/about" },
    { label: "Contact", icon: Mail, href: "/contact" }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <Button
            className="mr-2 px-2 hover:bg-transparent lg:hidden"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            {isSidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </Button>

          <div className="mr-4 hidden md:flex">
            <a href="/" className="mr-6 flex items-center space-x-2">
              <span className="hidden font-bold sm:inline-block">Djangify</span>
            </a>
            <nav className="flex items-center space-x-6">
              {mainNavItems.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="flex items-center px-4 py-2 text-sm font-medium hover:text-primary"
                >
                  <item.icon className="mr-2 h-4 w-4" />
                  {item.label}
                </a>
              ))}
            </nav>
          </div>

          <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
            <div className="w-full flex-1 md:w-auto md:flex-none">
              <Button
                className="relative w-full justify-start text-sm text-muted-foreground sm:pr-12 md:w-40 lg:w-64"
                onClick={() => setIsSearchOpen(true)}
              >
                <Search className="mr-2 h-4 w-4" />
                Search...
              </Button>
            </div>
            <ThemeToggle>{children}</ThemeToggle>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container flex-1 items-start md:grid md:grid-cols-[220px_minmax(0,1fr)] md:gap-6 lg:grid-cols-[240px_minmax(0,1fr)] lg:gap-10">
        {/* Sidebar */}
        <aside className={`fixed top-14 z-30 -ml-2 hidden h-[calc(100vh-3.5rem)] w-full shrink-0 overflow-y-auto border-r md:sticky md:block ${isSidebarOpen ? "lg:block" : "lg:hidden"
          }`}>
          <nav className="relative px-4 py-6 lg:px-6">
            {mainNavItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="flex items-center px-2 py-2 text-sm font-medium hover:text-primary"
              >
                <item.icon className="mr-2 h-4 w-4" />
                {item.label}
              </a>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex w-full flex-col overflow-hidden">{children}</main>
      </div>

      {/* Footer */}
      <footer className="border-t py-6 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
          <div className="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
            <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
              Built with Next.js, Django, and shadcn/ui.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
