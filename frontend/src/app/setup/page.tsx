'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { User, ArrowRight, Zap, BarChart3, ShieldCheck, AlertCircle } from "lucide-react";

export default function SetupPage() {
    const [name, setName] = useState('');
    const [touched, setTouched] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();

    const validateName = (val: string) => {
        if (val.length < 2) return "Name must be at least 2 characters";
        if (val.length > 50) return "Name must be less than 50 characters";
        if (!/^[a-zA-Z\s,.'-]+$/.test(val)) return "Name contains invalid characters";
        return "";
    };

    const handleStart = (e: React.FormEvent) => {
        e.preventDefault();
        const validationError = validateName(name.trim());
        if (validationError) {
            setError(validationError);
            return;
        }

        sessionStorage.setItem('userName', name.trim());
        router.push('/interview');
    };

    const features = [
        { icon: <Zap className="w-4 h-4" />, title: "Real-time AI", desc: "Advanced emotion tracking" },
        { icon: <BarChart3 className="w-4 h-4" />, title: "Psychometrics", desc: "Big Five personality mapping" },
        { icon: <ShieldCheck className="w-4 h-4" />, title: "Unbiased Matching", desc: "Fair career recommendations" }
    ];

    return (
        <main className="min-h-screen flex flex-col items-center justify-center p-6 relative">
            <div className="w-full max-w-5xl flex flex-col lg:flex-row gap-16 items-center">
                {/* Left Side: Info */}
                <div className="flex-1 space-y-8 text-center lg:text-left">
                    <div className="space-y-4">
                        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-gray-900 leading-tight">
                            Let&apos;s get to <br />
                            <span className="text-indigo-500">know you.</span>
                        </h1>
                        <p className="text-base text-gray-500 max-w-md leading-relaxed">
                            Enter your name to begin a personalized AI-powered career assessment session.
                        </p>
                    </div>

                    <div className="space-y-3 max-w-sm mx-auto lg:mx-0">
                        {features.map((f, i) => (
                            <div key={i} className="flex items-center gap-4 p-4 rounded-xl border border-gray-200 bg-white hover:border-indigo-200 transition-colors">
                                <div className="p-2 rounded-lg bg-indigo-50 text-indigo-500">
                                    {f.icon}
                                </div>
                                <div>
                                    <h4 className="text-sm font-semibold text-gray-900">{f.title}</h4>
                                    <p className="text-xs text-gray-500">{f.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Right Side: Form Card */}
                <div className="w-full max-w-md">
                    <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                        <div className="space-y-1 mb-8">
                            <h2 className="text-2xl font-bold text-gray-900">Enter your name</h2>
                            <p className="text-sm text-gray-500">This will be used to personalize your assessment.</p>
                        </div>

                        <form onSubmit={handleStart} className="space-y-6">
                            <div className="space-y-2">
                                <label
                                    htmlFor="name-input"
                                    className="text-xs font-medium text-gray-700 flex items-center gap-2"
                                >
                                    <User className="w-3.5 h-3.5" />
                                    Your Name
                                </label>
                                <div className="relative">
                                    <Input
                                        id="name-input"
                                        placeholder="Enter your name"
                                        value={name}
                                        onChange={(e) => {
                                            setName(e.target.value);
                                            if (touched) validateName(e.target.value);
                                        }}
                                        onBlur={() => {
                                            setTouched(true);
                                            validateName(name);
                                        }}
                                        className={cn(
                                            "h-12 rounded-lg border bg-gray-50 text-base px-4 transition-colors placeholder:text-gray-400 pr-10",
                                            error ? "border-red-300 focus:border-red-500 bg-red-50/10" :
                                                (touched && !error && name.length >= 2) ? "border-green-300 focus:border-green-500 bg-green-50/10" :
                                                    "border-gray-200 focus:border-indigo-500"
                                        )}
                                        aria-invalid={!!error}
                                        aria-describedby={error ? "name-error" : undefined}
                                        required
                                    />
                                    {touched && !error && name.length >= 2 && (
                                        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500 pointer-events-none animate-in fade-in zoom-in">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        </div>
                                    )}
                                </div>
                                {error && (
                                    <p id="name-error" className="text-xs text-red-500 mt-1 flex items-center gap-1 animate-in slide-in-from-top-1">
                                        <AlertCircle className="w-3 h-3" />
                                        {error}
                                    </p>
                                )}
                            </div>

                            <Button
                                type="submit"
                                disabled={!!error || name.length < 2}
                                className={cn(
                                    "w-full h-12 rounded-lg text-base font-medium transition-all shadow-sm",
                                    !!error || name.length < 2
                                        ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                                        : "bg-indigo-500 hover:bg-indigo-600 text-white"
                                )}
                            >
                                Continue <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>

                            <p className="text-center text-xs text-gray-400 pt-2">
                                Your data is processed locally and not stored within backend DB.
                            </p>
                        </form>
                    </div>
                </div>
            </div>
        </main>
    );
}
