"use client";

import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const backgrounds = {
    hero: "/images/back.png",
    philosophy: "/images/sea.png",
    future: "/images/indoor.png",
};

export const SectionBackground = () => {
    const [activeSection, setActiveSection] = useState<keyof typeof backgrounds>("hero");

    useEffect(() => {
        const sections = ["section-hero", "section-philosophy", "section-future"];
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const id = entry.target.id.replace("section-", "");
                        if (id in backgrounds) {
                            setActiveSection(id as keyof typeof backgrounds);
                        }
                    }
                });
            },
            { threshold: 0.4 }
        );

        sections.forEach((id) => {
            const el = document.getElementById(id);
            if (el) observer.observe(el);
        });

        return () => observer.disconnect();
    }, []);

    return (
        <div className="fixed inset-0 z-[-1] overflow-hidden bg-black">
            <AnimatePresence mode="wait">
                <motion.div
                    key={activeSection}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 0.8 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 1.5, ease: "easeInOut" }}
                    className="absolute inset-0 bg-cover bg-center"
                    style={{ backgroundImage: `url(${backgrounds[activeSection]})` }}
                />
            </AnimatePresence>
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/10 to-black/30 pointer-events-none" />
        </div>
    );
};
