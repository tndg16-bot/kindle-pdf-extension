'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';

const navItems = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/philosophy', label: 'Philosophy' },
    { href: '/sessions', label: 'Sessions' },
    { href: '/contact', label: 'Contact' },
];

const externalLinks = [
    { href: 'https://ai-diagnosis-six.vercel.app', label: '🤖 診断' },
];

export default function Header() {
    const pathname = usePathname();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-black/50 backdrop-blur-xl border-b border-white/10">
            <nav className="max-w-6xl mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <Link href="/" className="text-xl font-bold bg-gradient-to-r from-teal-400 to-purple-400 bg-clip-text text-transparent">
                        Takahiro Motoyama
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center gap-6">
                        {navItems.map((item) => (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={`relative py-2 text-sm font-medium transition-colors ${pathname === item.href
                                    ? 'text-teal-400'
                                    : 'text-zinc-400 hover:text-white'
                                    }`}
                            >
                                {item.label}
                                {pathname === item.href && (
                                    <motion.div
                                        layoutId="activeNav"
                                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-teal-400 to-purple-400"
                                    />
                                )}
                            </Link>
                        ))}
                        {externalLinks.map((item) => (
                            <a
                                key={item.href}
                                href={item.href}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="py-2 px-3 text-sm font-medium bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full hover:brightness-110 transition-all"
                            >
                                {item.label}
                            </a>
                        ))}
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        className="md:hidden p-2 text-zinc-400 hover:text-white"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </div>

                {/* Mobile Navigation */}
                {isMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="md:hidden mt-4 pb-4 border-t border-white/10 pt-4"
                    >
                        <div className="flex flex-col gap-3">
                            {navItems.map((item) => (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    onClick={() => setIsMenuOpen(false)}
                                    className={`py-2 text-sm font-medium transition-colors ${pathname === item.href
                                        ? 'text-teal-400'
                                        : 'text-zinc-400 hover:text-white'
                                        }`}
                                >
                                    {item.label}
                                </Link>
                            ))}
                            {externalLinks.map((item) => (
                                <a
                                    key={item.href}
                                    href={item.href}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    onClick={() => setIsMenuOpen(false)}
                                    className="py-2 px-3 text-sm font-medium bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full text-center hover:brightness-110 transition-all"
                                >
                                    {item.label}
                                </a>
                            ))}
                        </div>
                    </motion.div>
                )}
            </nav>
        </header>
    );
}
