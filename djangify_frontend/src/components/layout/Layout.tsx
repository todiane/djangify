'use client';

import React, { useState, ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import {
  Menu,
  X,
  Home,
  Briefcase,
  BookOpen,
  User,
  Mail,
  Search,
  Settings,
  PenSquare,
  Github,
  Linkedin
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  isAdmin?: boolean;
}

const Layout = ({ children, isAdmin = false }: LayoutProps) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPath, setCurrentPath] = useState('/');

  const publicNavItems = [
    { label: 'Home', icon: Home, href: '/' },
    { label: 'Projects', icon: Briefcase, href: '/projects' },
    { label: 'Blog', icon: BookOpen, href: '/blog' },
    { label: 'About', icon: User, href: '/about' },
    { label: 'Contact', icon: Mail, href: '/contact' }
  ];

  const adminNavItems = [
    { label: 'New Post', icon: PenSquare, href: '/admin/new-post' },
    { label: 'Settings', icon: Settings, href: '/admin/settings' }
  ];

  const navigationItems = isAdmin
    ? [...publicNavItems, ...adminNavItems]
    : publicNavItems;

  const footerLinks = [
    { label: 'Blog', href: '/blog' },
    { label: 'Projects', href: '/projects' },
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background">
      {/* Top Navigation Bar */}
      <header className="fixed top-0 right-0 left-0 h-16 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b z-50">
        <div className="container mx-auto px-4 h-full">
          <div className="flex items-center justify-between h-full">
            {/* Left section */}
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="lg:hidden"
              >
                {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
              </Button>

              <div className="hidden lg:flex items-center space-x-6">
                {navigationItems.map((item) => (
                  <a
                    key={item.href}
                    href={item.href}
                    className="flex items-center space-x-2 text-sm font-medium hover:text-primary transition-colors"
                  >
                    <item.icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </a>
                ))}
              </div>
            </div>

            {/* Center section - Search */}
            <div className="flex-1 max-w-xl mx-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={() => setIsSearchOpen(true)}
                  className="w-full px-4 py-2 border rounded-md pl-10 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                />
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
              </div>
            </div>

            {/* Right section */}
            <div className="flex items-center space-x-4">
              <span className="text-foreground font-semibold hidden sm:inline-block">Your Name</span>
              <img
                src="/api/placeholder/40/40"
                alt="Profile"
                className="w-10 h-10 rounded-full"
              />
            </div>
          </div>
        </div>
      </header>

      {/* Sidebar - Mobile */}
      <aside
        className={`
          fixed top-16 left-0 h-[calc(100vh-4rem)] bg-background border-r z-40
          transition-transform duration-300 ease-in-out lg:hidden
          ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          w-64
        `}
      >
        <nav className="p-4">
          {navigationItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className={`
                flex items-center space-x-2 px-4 py-3 rounded-md
                hover:bg-muted transition-colors duration-200
                ${currentPath === item.href ? 'bg-muted text-primary' : 'text-foreground'}
              `}
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </a>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 mt-16 px-4 lg:px-8">
        <div className="max-w-7xl mx-auto py-8">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t bg-background">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded flex items-center justify-center">
                <span className="text-primary-foreground font-bold">D</span>
              </div>
              <span className="text-lg font-semibold text-foreground">Djangify</span>
            </div>

            <nav className="flex flex-wrap justify-center md:justify-end gap-6">
              {footerLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  {link.label}
                </a>
              ))}
            </nav>

            <div className="flex items-center space-x-4">
              <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </footer>

      {/* Search overlay */}
      {isSearchOpen && (
        <div
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
          onClick={() => setIsSearchOpen(false)}
        />
      )}
    </div>
  );
};

export default Layout;
