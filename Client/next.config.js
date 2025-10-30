// next.config.js
const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack(config) {
    // Алиас @ указывает на папку src
    config.resolve.alias['@'] = path.resolve(__dirname, 'src');
    return config;
  },
};

module.exports = nextConfig;