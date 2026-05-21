import type { NextConfig } from "next";

// const isProd = process.env.NODE_ENV === 'production';

// const tauriHost = process.env.TAURI_DEV_HOST;

const nextConfig: NextConfig = {
  reactCompiler: true,
  output: "export", 

  images: {
    unoptimized: true,
  },

  // allowedDevOrigins: tauriHost ? [tauriHost, "localhost", "tauri.localhost"] : undefined,

  // assetPrefix: isProd ? undefined : tauriHost ? `http://${tauriHost}:3000` : undefined,
};

export default nextConfig;