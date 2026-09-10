/**
 * Utility for on-the-fly image URL optimization.
 * Dynamically transforms Cloudinary and Unsplash URLs into lightweight, modern formats (WebP/AVIF)
 * with optimal quality and dimensions, drastically improving initial page load time.
 */

/**
 * Generates an optimized image URL.
 * 
 * @param {string} url - Original image URL
 * @param {object} options - Optimization options
 * @param {number} [options.width] - Target width in pixels
 * @param {number} [options.height] - Target height in pixels
 * @param {string} [options.quality='auto'] - Compression quality ('auto', 'eco', 'good', or number)
 * @param {string} [options.format='auto'] - Delivery format ('auto' for WebP/AVIF detection)
 * @param {string} [options.crop='limit'] - Crop/resize mode ('limit', 'fill', 'scale', 'fit')
 * @returns {string} Optimized image URL
 */
export function getOptimizedImageUrl(url, options = {}) {
  if (!url || typeof url !== 'string') {
    return '';
  }

  const {
    width,
    height,
    quality = 'auto',
    format = 'auto',
    crop = 'limit'
  } = options;

  // 1. Cloudinary optimization
  if (url.includes('res.cloudinary.com')) {
    // Cloudinary transformation params
    const transforms = [`f_${format}`, `q_${quality}`];
    if (width) transforms.push(`w_${Math.round(width)}`);
    if (height) transforms.push(`h_${Math.round(height)}`);
    if (crop) transforms.push(`c_${crop}`);
    const transformStr = transforms.join(',');

    // Match Cloudinary upload path structure:
    // .../image/upload/[optional existing transformations/]v12345/public_id.ext
    // or .../image/upload/[optional existing transformations/]public_id.ext
    const uploadIndex = url.indexOf('/image/upload/');
    if (uploadIndex !== -1) {
      const prefix = url.slice(0, uploadIndex + '/image/upload/'.length);
      const rest = url.slice(uploadIndex + '/image/upload/'.length);

      // Check if rest already has transformations before version or path
      // Pattern: starts with transformations (letters, numbers, commas, underscores, colons) followed by /
      // e.g. "c_limit,w_500/v12345/img.png" or "v12345/img.png"
      const versionMatch = rest.match(/^(?:([a-z0-9_,:]+)\/)?(v\d+\/.*|[^\/]+$)/i);
      
      if (versionMatch) {
        const pathPart = versionMatch[2];
        return `${prefix}${transformStr}/${pathPart}`;
      }

      return `${prefix}${transformStr}/${rest}`;
    }

    return url;
  }

  // 2. Unsplash optimization
  if (url.includes('images.unsplash.com')) {
    try {
      const urlObj = new URL(url);
      urlObj.searchParams.set('auto', 'format');
      urlObj.searchParams.set('fit', 'crop');
      if (width) {
        urlObj.searchParams.set('w', Math.round(width).toString());
      }
      if (quality === 'auto') {
        urlObj.searchParams.set('q', '75');
      } else {
        urlObj.searchParams.set('q', quality.toString());
      }
      return urlObj.toString();
    } catch {
      return url;
    }
  }

  // 3. SVG or local/other URLs return as-is
  return url;
}

/**
 * Helper to generate srcSet for responsive retina / high-DPI displays.
 */
export function getOptimizedSrcSet(url, baseWidth, options = {}) {
  if (!url || !baseWidth) return undefined;

  const url1x = getOptimizedImageUrl(url, { ...options, width: baseWidth });
  const url2x = getOptimizedImageUrl(url, { ...options, width: baseWidth * 2 });

  return `${url1x} 1x, ${url2x} 2x`;
}
