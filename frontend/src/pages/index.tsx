import React from "react";
import { motion } from "framer-motion";
import { FaPiggyBank, FaMobileAlt, FaChartLine, FaLock } from "react-icons/fa";

const features = [
  {
    icon: <FaMobileAlt className="text-indigo-600 text-3xl mb-4" />,
    title: "Mobile Banking",
    desc: "Bank anywhere, anytime with our secure mobile app.",
  },
  {
    icon: <FaChartLine className="text-green-500 text-3xl mb-4" />,
    title: "Smart Analytics",
    desc: "Track spending, savings, and investments in real time.",
  },
  {
    icon: <FaLock className="text-blue-500 text-3xl mb-4" />,
    title: "Top-Notch Security",
    desc: "Your data and money are protected with industry-leading security.",
  },
];

const steps = [
  {
    number: 1,
    title: "Sign Up Instantly",
    desc: "Create your account in minutes with just a few details.",
  },
  {
    number: 2,
    title: "Connect Your Bank",
    desc: "Securely link your existing accounts and cards.",
  },
  {
    number: 3,
    title: "Start Managing",
    desc: "Enjoy smart insights and full control over your finances.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-50 via-white to-blue-50 font-sans">
      {/* Navbar */}
      <nav className="w-full flex items-center justify-between px-8 py-6 bg-white/80 shadow-sm">
        <div className="flex items-center gap-2">
          <FaPiggyBank className="text-indigo-600 text-2xl" />
          <span className="font-bold text-xl tracking-tight">FinFlow</span>
        </div>
        <div className="hidden md:flex gap-8 text-gray-700 font-medium">
          <a href="#features" className="hover:text-indigo-600 transition">Features</a>
          <a href="#how" className="hover:text-indigo-600 transition">How it Works</a>
          <a href="#contact" className="hover:text-indigo-600 transition">Contact</a>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="flex flex-col md:flex-row items-center justify-between max-w-6xl mx-auto px-8 py-20 gap-12 w-full"
      >
        {/* Left: Text */}
        <div className="flex-1 flex flex-col items-start justify-center">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.7 }}
            className="text-4xl md:text-6xl font-extrabold text-gray-900 mb-6 leading-tight"
          >
            Smarter Banking for Modern Life
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.7 }}
            className="text-lg md:text-2xl text-gray-600 mb-8 max-w-xl"
          >
            Manage your money, track your goals, and get AI-powered insights—all in one beautiful dashboard.
          </motion.p>
          <motion.a
            href="#"
            className="px-8 py-4 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 transition font-bold text-lg"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.97 }}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
          >
            Get Started Free
          </motion.a>
        </div>
        {/* Right: Illustration */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.7 }}
          className="flex-1 flex items-center justify-center"
        >
          <div className="w-80 h-80 bg-gradient-to-br from-indigo-100 to-blue-100 rounded-3xl shadow-lg flex items-center justify-center relative">
            {/* Placeholder for dashboard/phone illustration */}
            <FaMobileAlt className="text-indigo-400 text-[7rem]" />
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-white rounded-full px-6 py-2 shadow text-indigo-600 font-semibold text-lg">
              Digital Banking
            </div>
          </div>
        </motion.div>
      </motion.section>

      {/* Features Section */}
      <section id="features" className="py-16 px-4 bg-white">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Powerful Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15, duration: 0.7 }}
                className="bg-gradient-to-br from-indigo-50 to-white rounded-2xl p-8 shadow hover:shadow-2xl hover:scale-105 border border-gray-100 flex flex-col items-center text-center transition"
                whileHover={{ scale: 1.05, boxShadow: "0 8px 32px rgba(99,102,241,0.15)" }}
              >
                {f.icon}
                <h3 className="font-semibold text-xl mb-2">{f.title}</h3>
                <p className="text-gray-600">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how" className="py-16 px-4 bg-gradient-to-r from-blue-50 via-white to-indigo-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">How It Works</h2>
          <div className="flex flex-col md:flex-row items-center justify-center gap-8">
            {steps.map((step, i) => (
              <motion.div
                key={step.number}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2, duration: 0.7 }}
                className="flex flex-col items-center text-center bg-white rounded-2xl shadow p-8 w-64 hover:shadow-2xl hover:scale-105 transition"
                whileHover={{ scale: 1.05, boxShadow: "0 8px 32px rgba(99,102,241,0.15)" }}
              >
                <div className="w-12 h-12 flex items-center justify-center bg-indigo-100 text-indigo-600 rounded-full text-2xl font-bold mb-4">
                  {step.number}
                </div>
                <h4 className="font-semibold text-lg mb-2">{step.title}</h4>
                <p className="text-gray-600">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-200 py-8 px-4 mt-auto">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <FaPiggyBank className="text-indigo-400 text-2xl" />
            <span className="font-bold text-lg">FinFlow</span>
          </div>
          <div className="flex gap-6 text-sm">
            <a href="#features" className="hover:underline">Features</a>
            <a href="#how" className="hover:underline">How it Works</a>
            <a href="#contact" className="hover:underline">Contact</a>
          </div>
          <div className="flex gap-4">
            {/* Social icons or links can go here */}
          </div>
        </div>
        <div className="text-center text-xs text-gray-500 mt-4">
          &copy; {new Date().getFullYear()} FinFlow. All rights reserved.
        </div>
      </footer>
    </div>
  );
}