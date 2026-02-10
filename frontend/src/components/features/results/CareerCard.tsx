import React from 'react';
import {
    Database, Shield, Cloud, Code, LineChart,
    Layers, Cpu, Globe, Search, BookOpen,
    CheckCircle2, Settings, PenTool, Layout, Activity
} from 'lucide-react';
import { cn } from "@/lib/utils";

interface CareerCardProps {
    career: string;
    confidence: number;
    description: string;
    skills: string[];
    growth_path?: string;
    justification?: string;
    variant?: 'default' | 'compact';
    isPrimary?: boolean;
}

const getCareerIcon = (career: string) => {
    const c = career.toLowerCase();
    if (c.includes('scientist')) return <LineChart className="w-5 h-5" />;
    if (c.includes('developer') || c.includes('engineer')) return <Code className="w-5 h-5" />;
    if (c.includes('devops')) return <Settings className="w-5 h-5" />;
    if (c.includes('designer') || c.includes('creative')) return <PenTool className="w-5 h-5" />;
    if (c.includes('security')) return <Shield className="w-5 h-5" />;
    if (c.includes('architect')) return <Cloud className="w-5 h-5" />;
    if (c.includes('stack')) return <Layers className="w-5 h-5" />;
    if (c.includes('database')) return <Database className="w-5 h-5" />;
    if (c.includes('network')) return <Globe className="w-5 h-5" />;
    if (c.includes('manager')) return <CheckCircle2 className="w-5 h-5" />;
    if (c.includes('writer')) return <BookOpen className="w-5 h-5" />;
    if (c.includes('analyst')) return <Search className="w-5 h-5" />;
    return <Activity className="w-5 h-5" />;
};

export default function CareerCard({
    career,
    confidence,
    description,
    skills,
    growth_path,
    variant = 'default',
    isPrimary = false
}: CareerCardProps) {
    if (variant === 'compact') {
        return (
            <div className="flex items-center gap-3 p-3 rounded-xl border border-gray-100 bg-white hover:border-indigo-200 transition-colors shadow-sm">
                <div className="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center text-gray-400">
                    {getCareerIcon(career)}
                </div>
                <div className="flex-1 min-w-0">
                    <h4 className="text-xs font-bold text-gray-900 truncate">{career}</h4>
                    <p className="text-[10px] text-indigo-500 font-bold">{Math.round(confidence * 100)}% Match</p>
                </div>
            </div>
        );
    }

    return (
        <div className={cn(
            "rounded-xl border bg-white p-4 transition-all duration-300 hover:shadow-md shadow-sm overflow-hidden relative",
            isPrimary ? "border-indigo-200 ring-1 ring-indigo-50" : "border-gray-100"
        )}>
            {isPrimary && (
                <div className="absolute top-0 right-0">
                    <div className="bg-indigo-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-bl-lg uppercase tracking-wider">
                        Best Fit
                    </div>
                </div>
            )}

            <div className="flex items-start gap-3 mb-3">
                <div className={cn(
                    "w-10 h-10 rounded-lg flex items-center justify-center shrink-0 shadow-sm",
                    isPrimary ? "bg-indigo-600 text-white" : "bg-indigo-50 text-indigo-600"
                )}>
                    {getCareerIcon(career)}
                </div>
                <div className="min-w-0 pt-0.5">
                    <h3 className="text-sm font-bold text-gray-900 truncate leading-tight mb-1">{career}</h3>
                    <div className="flex items-center gap-2">
                        <div className="w-16 h-1 bg-gray-100 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-indigo-500 transition-all duration-1000"
                                style={{ width: `${confidence * 100}%` }}
                            />
                        </div>
                        <span className="text-[10px] font-bold text-indigo-500">
                            {Math.round(confidence * 100)}%
                        </span>
                    </div>
                </div>
            </div>

            <div className="space-y-3">
                <p className="text-[11px] text-gray-500 leading-relaxed line-clamp-2">
                    {description}
                </p>

                <div className="flex flex-wrap gap-1">
                    {(skills || []).slice(0, 3).map(skill => (
                        <span key={skill} className="px-1.5 py-0.5 rounded-md bg-gray-50 border border-gray-100 text-[9px] font-bold text-gray-500">
                            {skill}
                        </span>
                    ))}
                    {(skills || []).length > 3 && (
                        <span className="text-[9px] font-bold text-gray-400 self-center">
                            +{skills.length - 3}
                        </span>
                    )}
                </div>

                {growth_path && (
                    <div className="pt-1 border-t border-gray-50 pt-2">
                        <span className="text-[9px] font-bold text-gray-400 uppercase tracking-widest block mb-0.5">Growth Path</span>
                        <p className="text-[10px] font-bold text-indigo-600 truncate">
                            {growth_path}
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
