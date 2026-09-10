import { useState, useEffect } from 'react';
import { getOptimizedImageUrl } from '../../utils/imageOptimizer';

/**
 * High-performance image component with:
 * - On-the-fly Cloudinary/Unsplash optimization (WebP/AVIF, resizing, compression)
 * - Shimmer skeleton loading placeholder to eliminate Cumulative Layout Shift (CLS)
 * - Smooth fade-in transition
 * - Native lazy loading & async decoding
 * - Graceful fallback on broken/missing URLs
 */
const OptimizedImage = ({
  src,
  alt = '',
  className = '',
  imgClassName = '',
  width,
  height,
  crop = 'limit',
  quality = 'auto',
  priority = false,
  fallbackText = '',
  ...props
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(!src);

  // Reset state when src changes
  useEffect(() => {
    setIsLoaded(false);
    setHasError(!src);
  }, [src]);

  const optimizedSrc = getOptimizedImageUrl(src, {
    width,
    height,
    crop,
    quality,
  });

  if (hasError || !src) {
    return (
      <div 
        className={`flex flex-col items-center justify-center bg-slate-100 text-slate-400 p-4 select-none ${className}`}
        style={{ width: width ? `${width}px` : undefined, height: height ? `${height}px` : undefined }}
      >
        <svg 
          className="w-8 h-8 mb-1 opacity-50" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth="1.5" 
            d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" 
          />
        </svg>
        <span className="text-xs text-slate-400 font-medium truncate max-w-full">
          {fallbackText || alt || 'RG Win Product'}
        </span>
      </div>
    );
  }

  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Shimmer skeleton while loading */}
      {!isLoaded && (
        <div 
          className="absolute inset-0 bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100 animate-pulse z-0" 
          aria-hidden="true"
        />
      )}

      <img
        src={optimizedSrc}
        alt={alt}
        loading={priority ? 'eager' : 'lazy'}
        decoding="async"
        fetchPriority={priority ? 'high' : 'low'}
        onLoad={() => setIsLoaded(true)}
        onError={() => setHasError(true)}
        className={`w-full h-full transition-opacity duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        } ${imgClassName}`}
        {...props}
      />
    </div>
  );
};

export default OptimizedImage;
