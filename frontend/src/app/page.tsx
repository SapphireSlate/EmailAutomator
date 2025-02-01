'use client';

import { motion } from 'framer-motion';
import { 
  Mail, 
  Users, 
  FileText, 
  BarChart2, 
  Plus, 
  Upload, 
  PenTool,
  Menu,
  Moon,
  Sun
} from 'lucide-react';
import { useState } from 'react';

export default function Home() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex justify-center">
      <div className="w-full max-w-[1400px] relative flex">
        {/* Sidebar */}
        <motion.aside 
          initial={{ width: isSidebarOpen ? 280 : 0 }}
          animate={{ width: isSidebarOpen ? 280 : 0 }}
          className={`fixed h-full bg-white dark:bg-gray-800 shadow-lg z-20 overflow-hidden
            ${isSidebarOpen ? 'w-70' : 'w-0'}`}
          style={{ left: 'max((100vw - 1400px) / 2, 0px)' }}
        >
          <div className="flex flex-col h-full">
            {/* Logo Section */}
            <div className="flex items-center justify-center p-6 border-b border-gray-200 dark:border-gray-700">
              <Mail className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
              <span className="ml-3 text-xl font-bold text-gray-900 dark:text-white">
                Email Automator
              </span>
            </div>

            {/* Navigation Links */}
            <nav className="flex-1 px-6 py-4">
              <div className="space-y-2">
                {[
                  { name: 'Total Campaigns', icon: BarChart2, count: '12' },
                  { name: 'Active Contacts', icon: Users, count: '2,100' },
                  { name: 'Emails Sent', icon: Mail, count: '24,550' },
                  { name: 'Templates', icon: FileText, count: '15' },
                ].map((item) => (
                  <motion.a
                    key={item.name}
                    whileHover={{ x: 5 }}
                    className="flex items-center p-4 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl cursor-pointer group"
                  >
                    <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-700 group-hover:bg-indigo-100 dark:group-hover:bg-indigo-900">
                      <item.icon className="h-5 w-5 text-gray-500 dark:text-gray-400 group-hover:text-indigo-600 dark:group-hover:text-indigo-400" />
                    </div>
                    <div className="ml-4 flex-1">
                      <p className="text-sm font-medium">{item.name}</p>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{item.count}</p>
                    </div>
                  </motion.a>
                ))}
              </div>
            </nav>

            {/* Bottom Section */}
            <div className="p-6 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="flex items-center justify-center p-4 w-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl"
              >
                {isDarkMode ? (
                  <Sun className="h-5 w-5 mr-3" />
                ) : (
                  <Moon className="h-5 w-5 mr-3" />
                )}
                <span>Toggle Theme</span>
              </button>
            </div>
          </div>
        </motion.aside>

        {/* Main Content */}
        <div className={`flex-1 ${isSidebarOpen ? 'ml-[280px]' : 'ml-0'}`}>
          {/* Top Navigation */}
          <nav className="bg-white dark:bg-gray-800 shadow-sm h-16 fixed w-full z-10" 
               style={{ maxWidth: isSidebarOpen ? 'calc(1400px - 280px)' : '1400px', right: 'max((100vw - 1400px) / 2, 0px)' }}>
            <div className="h-full flex items-center px-6">
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <Menu className="h-6 w-6 text-gray-600 dark:text-gray-300" />
              </button>
            </div>
          </nav>

          {/* Main Content Area */}
          <main className="pt-24 pb-12 px-8">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
              {[
                { name: 'Total Campaigns', stat: '12', icon: BarChart2, color: 'bg-pink-500 shadow-pink-500/30' },
                { name: 'Active Contacts', stat: '2,100', icon: Users, color: 'bg-blue-500 shadow-blue-500/30' },
                { name: 'Emails Sent', stat: '24,550', icon: Mail, color: 'bg-green-500 shadow-green-500/30' },
                { name: 'Templates', stat: '15', icon: FileText, color: 'bg-purple-500 shadow-purple-500/30' },
              ].map((item, index) => (
                <motion.div
                  key={item.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-white dark:bg-gray-800 shadow-lg rounded-2xl hover:shadow-xl transition-all duration-300"
                  whileHover={{ scale: 1.02, y: -5 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="p-6">
                    <div className="flex items-center">
                      <div className={`flex items-center justify-center w-14 h-14 ${item.color} rounded-2xl shadow-lg`}>
                        <item.icon className="h-7 w-7 text-white" />
                      </div>
                      <div className="ml-5 flex-1">
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                          {item.name}
                        </p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                          {item.stat}
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Quick Actions */}
            <motion.div 
              className="bg-white dark:bg-gray-800 shadow-lg rounded-2xl overflow-hidden"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <div className="p-8">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-8 text-center">
                  Quick Actions
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl mx-auto">
                  {[
                    { name: 'New Campaign', icon: Plus, color: 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-500/30' },
                    { name: 'Import Contacts', icon: Upload, color: 'bg-green-600 hover:bg-green-700 shadow-green-500/30' },
                    { name: 'Create Template', icon: PenTool, color: 'bg-purple-600 hover:bg-purple-700 shadow-purple-500/30' },
                  ].map((action) => (
                    <motion.button
                      key={action.name}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className={`inline-flex items-center justify-center px-8 py-4 border border-transparent
                        text-base font-medium rounded-xl text-white ${action.color}
                        shadow-lg transition-all duration-200 w-full`}
                    >
                      <action.icon className="w-5 h-5 mr-3" />
                      {action.name}
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          </main>
        </div>
      </div>
    </div>
  );
}
