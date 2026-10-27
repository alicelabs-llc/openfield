import type { NextConfig } from "next";

const isGithubPages = process.env.GITHUB_ACTIONS === "true";
const repoName = "openfield";
const basePath = isGithubPages ? `/${repoName}` : "";

const nextConfig: NextConfig = {
  // Static export for GitHub Pages / Cloudflare Pages static
  output: "export",
  // GitHub Pages serves at user.github.io/openfield/, so all assets need a basePath
  basePath,
  assetPrefix: basePath,
  images: {
    unoptimized: true,
  },
  experimental: {},
};

export default nextConfig;
