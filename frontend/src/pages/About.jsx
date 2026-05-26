import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';

const About = () => {
  const headerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: headerRef,
    offset: ["start start", "end start"]
  });

  const yBg = useTransform(scrollYProgress, [0, 1], ["0%", "40%"]);
  const opacityText = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

  return (
    <div className="bg-white overflow-hidden">
      {/* Parallax Header */}
      <section ref={headerRef} className="relative h-[60vh] flex items-center justify-center overflow-hidden bg-[var(--color-primary-light)]">
        <motion.div 
          className="absolute inset-0 z-0 opacity-20"
          style={{ y: yBg }}
        >
          <img 
            src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80" 
            alt="Medical background" 
            className="w-full h-full object-cover"
          />
        </motion.div>
        
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-white/90 z-10"></div>
        
        <motion.div 
          style={{ opacity: opacityText }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-20 text-center px-4 max-w-4xl mx-auto mt-20"
        >
          <h1 className="text-5xl md:text-6xl font-extrabold text-[var(--color-text-main)] mb-6 tracking-tight">About RG WIN HEALTHCARE</h1>
          <p className="text-xl md:text-2xl text-[var(--color-text-muted)] font-light leading-relaxed">
            Pioneering advancements in women's health through innovative gynecological solutions.
          </p>
        </motion.div>
      </section>

      {/* Main Content */}
      <section className="py-24 relative z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="relative group"
            >
              <div className="absolute -inset-4 bg-gradient-to-tr from-[var(--color-primary-light)] to-teal-100 rounded-3xl opacity-50 transform group-hover:rotate-2 transition-transform duration-500"></div>
              <img 
                src="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
                alt="Laboratory research" 
                className="relative rounded-2xl shadow-2xl w-full h-[500px] object-cover transform group-hover:-translate-y-2 transition-transform duration-500"
              />
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.8, ease: "easeOut", delay: 0.2 }}
            >
              <h2 className="text-3xl font-bold text-[var(--color-text-main)] mb-6 flex items-center gap-3">
                <span className="w-12 h-1 bg-[var(--color-primary)] inline-block rounded-full"></span>
                Our Vision
              </h2>
              <p className="text-lg text-[var(--color-text-muted)] mb-10 leading-relaxed">
                We envision a world where women have access to the highest standard of specialized healthcare. 
                Through rigorous research and clinical excellence, Healix stands at the forefront of gynecological medicine, empowering women at every stage of their lives.
              </p>
              
              <h2 className="text-3xl font-bold text-[var(--color-text-main)] mb-6 flex items-center gap-3">
                <span className="w-12 h-1 bg-teal-400 inline-block rounded-full"></span>
                Commitment to Quality
              </h2>
              <ul className="space-y-4">
                {[
                  "Stringent clinical testing protocols.",
                  "State-of-the-art manufacturing facilities.",
                  "Continuous investment in research and development.",
                  "Collaboration with leading medical professionals."
                ].map((item, idx) => (
                  <motion.li 
                    key={idx}
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: 0.4 + (idx * 0.1) }}
                    className="flex items-center gap-3 text-lg text-[var(--color-text-muted)] bg-gray-50 p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
                  >
                    <div className="w-2 h-2 rounded-full bg-[var(--color-primary)] shrink-0"></div>
                    {item}
                  </motion.li>
                ))}
              </ul>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
