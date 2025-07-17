import React from "react";
import { motion } from "framer-motion";
import { FaPiggyBank, FaChartPie, FaWallet, FaBullseye, FaArrowUp, FaArrowDown } from "react-icons/fa";

// Animation variants
const fadeInUp = {
  hidden: { opacity: 0, y: 40 },
  visible: (i = 1) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.15, duration: 0.7, type: "spring" as const },
  }),
};

const cards = [
  {
    icon: <FaWallet className="text-indigo-600 text-3xl mb-2" />, 
    label: "Account Balance",
    value: "$12,450.00",
    change: "+$250",
    changeType: "up",
  },
  {
    icon: <FaChartPie className="text-green-500 text-3xl mb-2" />, 
    label: "Investments",
    value: "$8,200.00",
    change: "+3.2%",
    changeType: "up",
  },
  {
    icon: <FaBullseye className="text-pink-500 text-3xl mb-2" />, 
    label: "Goals Progress",
    value: "72%",
    change: "+5%",
    changeType: "up",
  },
];

const recentTransactions = [
  { id: 1, desc: "Grocery Store", amount: "-$54.20", date: "2024-06-01" },
  { id: 2, desc: "Salary", amount: "+$2,500.00", date: "2024-05-30" },
  { id: 3, desc: "Electricity Bill", amount: "-$120.00", date: "2024-05-28" },
  { id: 4, desc: "Coffee Shop", amount: "-$8.50", date: "2024-05-27" },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-50 via-white to-blue-50 font-sans">
      {/* Navbar */}
      <motion.nav
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="w-full flex items-center justify-between px-8 py-6 bg-white/80 shadow-sm"
      >
        <div className="flex items-center gap-2">
          <FaPiggyBank className="text-indigo-600 text-2xl" />
          <span className="font-bold text-xl tracking-tight">FinFlow</span>
        </div>
        <div className="hidden md:flex gap-8 text-gray-700 font-medium">
          <a href="/dashboard" className="hover:text-indigo-600 transition">Dashboard</a>
          <a href="/goal" className="hover:text-indigo-600 transition">Goals</a>
          <a href="/invest" className="hover:text-indigo-600 transition">Investments</a>
          <a href="/income" className="hover:text-indigo-600 transition">Income/Expense</a>
        </div>
      </motion.nav>

      {/* Welcome Section */}
      <section className="max-w-6xl mx-auto px-8 py-12 w-full">
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.7 }}
          className="text-3xl md:text-5xl font-extrabold text-gray-900 mb-4"
        >
          Welcome Back, User!
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.7 }}
          className="text-lg md:text-xl text-gray-600 mb-8"
        >
          Here's a quick overview of your financial health and recent activity.
        </motion.p>
      </section>

      {/* Cards Section */}
      <section className="max-w-6xl mx-auto px-8 w-full">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {cards.map((card, i) => (
            <motion.div
              key={card.label}
              variants={fadeInUp}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              custom={i}
              className="bg-white rounded-2xl p-8 shadow hover:shadow-2xl border border-gray-100 flex flex-col items-center text-center transition"
              whileHover={{ scale: 1.05, boxShadow: "0 8px 32px rgba(99,102,241,0.15)" }}
            >
              {card.icon}
              <div className="font-semibold text-lg mb-1">{card.label}</div>
              <div className="text-2xl font-bold mb-2">{card.value}</div>
              <div className={`flex items-center gap-1 text-sm font-medium ${card.changeType === "up" ? "text-green-500" : "text-red-500"}`}>
                {card.changeType === "up" ? <FaArrowUp /> : <FaArrowDown />} {card.change}
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Recent Transactions & Graphs */}
      <section className="max-w-6xl mx-auto px-8 w-full flex flex-col md:flex-row gap-8 mb-16">
        {/* Recent Transactions */}
        <motion.div
          variants={fadeInUp}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          custom={1}
          className="flex-1 bg-white rounded-2xl shadow p-8 border border-gray-100"
        >
          <div className="font-bold text-xl mb-4">Recent Transactions</div>
          <ul>
            {recentTransactions.map((tx) => (
              <li key={tx.id} className="flex justify-between items-center py-2 border-b last:border-b-0">
                <span className="text-gray-700">{tx.desc}</span>
                <span className={`font-mono ${tx.amount.startsWith("-") ? "text-red-500" : "text-green-500"}`}>{tx.amount}</span>
                <span className="text-xs text-gray-400">{tx.date}</span>
              </li>
            ))}
          </ul>
        </motion.div>
        {/* Placeholder for Graphs */}
        <motion.div
          variants={fadeInUp}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          custom={2}
          className="flex-1 bg-white rounded-2xl shadow p-8 border border-gray-100 flex flex-col items-center justify-center"
        >
          <div className="font-bold text-xl mb-4">Investment Performance</div>
          {/* Placeholder for a chart/graph - replace with real chart later */}
          <div className="w-full h-48 flex items-center justify-center">
            <div className="w-40 h-40 rounded-full bg-gradient-to-tr from-indigo-200 to-green-200 flex items-center justify-center">
              <span className="text-3xl font-bold text-indigo-700">+8.5%</span>
            </div>
          </div>
          <div className="text-gray-500 mt-4">This month's growth</div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-200 py-8 px-4 mt-auto">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <FaPiggyBank className="text-indigo-400 text-2xl" />
            <span className="font-bold text-lg">FinFlow</span>
          </div>
          <div className="flex gap-6 text-sm">
            <a href="/dashboard" className="hover:underline">Dashboard</a>
            <a href="/goal" className="hover:underline">Goals</a>
            <a href="/invest" className="hover:underline">Investments</a>
            <a href="/income" className="hover:underline">Income/Expense</a>
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
