import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, MessageSquare, Shield, Activity } from 'lucide-react';
import { useState, useEffect } from 'react';
import { productService } from '../services/api';

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const products = await productService.getProducts();
        const found = products.find(p => p.id === parseInt(id));
        setProduct(found);
      } catch (error) {
        console.error("Error fetching product details", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="py-20 text-center">Loading product details...</div>
    );
  }

  if (!product) {
    return (
      <div className="py-20 text-center">
        <h2 className="text-2xl font-bold mb-4">Product not found</h2>
        <Link to="/products" className="text-[var(--color-primary)] hover:underline">
          Return to Products
        </Link>
      </div>
    );
  }

  // API now returns these as JSON arrays directly
  const benefits = product.benefits || [];
  const ingredients = product.ingredients || [];

  return (
    <div className="py-12 bg-white min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link to="/products" className="inline-flex items-center text-[var(--color-text-muted)] hover:text-[var(--color-primary)] mb-8 transition-colors">
          <ArrowLeft className="h-4 w-4 mr-2" /> Back to Products
        </Link>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="rounded-2xl overflow-hidden shadow-lg border border-[var(--color-border)] bg-gray-50 h-96 md:h-[500px]">
              <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex flex-col justify-center"
          >
            <span className="inline-block px-3 py-1 bg-[var(--color-primary-light)] text-[var(--color-primary)] rounded-full text-sm font-semibold mb-4 w-fit uppercase tracking-wider">
              {product.category?.name || 'Uncategorized'}
            </span>
            <h1 className="text-4xl font-bold text-[var(--color-text-main)] mb-2">{product.name}</h1>
            <div className="mb-6">
              {product.mrp && <p className="text-3xl font-black text-[var(--color-primaryDark)]">MRP {product.mrp}</p>}
            </div>
            
            <p className="text-lg text-[var(--color-text-muted)] mb-8 leading-relaxed">
              {product.description}
            </p>

            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[var(--color-primary-light)] flex items-center justify-center text-[var(--color-primary)]">
                  <Shield className="h-5 w-5" />
                </div>
                <span className="text-sm font-medium text-[var(--color-text-main)]">Clinically Tested</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[var(--color-primary-light)] flex items-center justify-center text-[var(--color-primary)]">
                  <Activity className="h-5 w-5" />
                </div>
                <span className="text-sm font-medium text-[var(--color-text-main)]">High Efficacy</span>
              </div>
            </div>

            {/* Clinical Overview (For Doctors) */}
            {ingredients.length > 0 && (
              <div className="mb-8 bg-gray-50/80 border border-gray-200 rounded-2xl p-6 shadow-inner">
                <h3 className="text-sm font-bold text-gray-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                  Clinical Composition
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {ingredients.map((ing, idx) => (
                    <div key={idx} className="flex items-start gap-3 bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
                      <div className="w-2 h-2 mt-2 rounded-full bg-[var(--color-primary)]"></div>
                      <span className="text-[var(--color-text-main)] font-semibold text-sm leading-snug">{ing}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Key Benefits (For Customers/Patients) */}
            {benefits.length > 0 && (
              <div className="mb-10">
                <h3 className="text-xl font-bold text-[var(--color-text-main)] mb-6 flex items-center gap-2">
                  <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.514"></path></svg>
                  Why choose this?
                </h3>
                <div className="space-y-4">
                  {benefits.map((ben, idx) => (
                    <div key={idx} className="flex items-center gap-4 bg-green-50/50 p-4 rounded-xl border border-green-100/50 hover:bg-green-50 transition-colors">
                      <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-green-100 rounded-full text-green-600">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                      </div>
                      <span className="text-[var(--color-text-main)] font-medium text-[15px]">{ben}</span>
                    </div>
                  ))}
                </div>
              </div>
            )} 
            
            <Link to={`/contact?product=${encodeURIComponent(product.name)}`} className="btn-primary flex items-center justify-center gap-2 w-full md:w-auto py-3 text-lg">
              <MessageSquare className="h-5 w-5" /> Enquire Now
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
