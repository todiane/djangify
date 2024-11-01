/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  serverRuntimeConfig: {
    timeZone: 'Europe/London',
  },
  images: {
    remotePatterns: [
      {
        protocol: process.env.NODE_ENV === 'development' ? 'http' : 'https',
        hostname: process.env.NEXT_PUBLIC_BACKEND_HOST || 'localhost',
        port: process.env.NEXT_PUBLIC_BACKEND_PORT || '8000',
        pathname: '/media/**',
      },
    ],
  },
}


module.exports = nextConfig
