import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowRight, Shield, Activity, Heart } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useRef } from 'react';

const Home = () => {
  const heroRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"]
  });

  const yBg = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);
  const opacityText = useTransform(scrollYProgress, [0, 0.8], [1, 0]);
  const yText = useTransform(scrollYProgress, [0, 1], ["0%", "30%"]);

  return (
    <div className="overflow-hidden">
      {/* Hero Section with Parallax */}
      <section ref={heroRef} className="relative bg-[var(--color-primary-light)] h-[90vh] flex items-center overflow-hidden">
        <motion.div 
          className="absolute inset-0 z-0"
          style={{ y: yBg }}
        >
          <div className="w-full h-full bg-gradient-to-br from-[var(--color-primary-light)] to-[#dceaf7]"></div>
          {/* Abstract floating circles for parallax background */}
          <div className="absolute top-20 right-[10%] w-64 h-64 bg-[var(--color-primary)] rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
          <div className="absolute bottom-20 left-[10%] w-72 h-72 bg-teal-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        </motion.div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <motion.div 
              style={{ opacity: opacityText, y: yText }}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-[var(--color-text-main)] leading-tight mb-6 tracking-tight">
                Advancing Women's <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-primary)] to-teal-500">Health Innovation</span>
              </h1>
              <p className="text-lg md:text-xl text-[var(--color-text-muted)] mb-8 max-w-lg leading-relaxed">
                Discover our specialized range of gynecological pharmaceutical products designed for modern healthcare needs.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/products" className="btn-primary text-center flex items-center justify-center gap-2 group shadow-lg shadow-teal-500/30 hover:shadow-teal-500/50 transition-all">
                  View Products 
                  <ArrowRight className="h-5 w-5 transform group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link to="/contact" className="btn-secondary text-center hover:bg-white transition-colors">
                  Contact Us
                </Link>
              </div>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, scale: 0.8, rotate: -5 }}
              animate={{ opacity: 1, scale: 1, rotate: 0 }}
              transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
              style={{ y: useTransform(scrollYProgress, [0, 1], ["0%", "15%"]) }}
              className="relative hidden md:block"
            >
              <div className="w-full h-[500px] bg-gradient-to-tr from-[var(--color-primary)] to-teal-300 rounded-3xl opacity-20 absolute -top-4 -left-4 transform -rotate-3"></div>
              <img 
                src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
                alt="Medical professional holding a pill bottle" 
                className="w-full h-[500px] object-cover rounded-3xl shadow-2xl relative z-10"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white relative z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
            className="text-center mb-20"
          >
            <h2 className="text-4xl font-bold text-[var(--color-text-main)] mb-6">Why Choose Healix</h2>
            <p className="text-lg text-[var(--color-text-muted)] max-w-2xl mx-auto">We are committed to delivering high-quality, safe, and effective healthcare solutions specifically tailored for women.</p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            {[
              { icon: Shield, title: "Clinically Proven", desc: "All our products undergo rigorous clinical testing to ensure maximum efficacy and safety." },
              { icon: Activity, title: "Modern Research", desc: "Developed using the latest advancements in gynecological and pharmaceutical sciences." },
              { icon: Heart, title: "Patient Centric", desc: "Designed with the comfort, well-being, and specific needs of women in mind." }
            ].map((feature, idx) => (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: idx * 0.2 }}
                whileHover={{ y: -10, scale: 1.02 }}
                className="card text-center p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300"
              >
                <div className="mx-auto w-20 h-20 bg-gradient-to-br from-[var(--color-primary-light)] to-blue-50 rounded-2xl flex items-center justify-center mb-8 text-[var(--color-primary)] shadow-inner transform rotate-3">
                  <feature.icon className="h-10 w-10 transform -rotate-3" />
                </div>
                <h3 className="text-2xl font-bold mb-4 text-[var(--color-text-main)]">{feature.title}</h3>
                <p className="text-[var(--color-text-muted)] leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
