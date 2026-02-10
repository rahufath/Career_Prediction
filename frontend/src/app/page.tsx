import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Video, Brain, Award } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 relative">
      <div className="max-w-3xl w-full text-center space-y-10">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-gray-200 bg-gray-50 text-xs text-gray-500 font-medium">
          <div className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
          AI-Powered Assessment
        </div>

        {/* Heading */}
        <div className="space-y-4">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-gray-900 leading-tight">
            Discover Your <br />
            <span className="text-indigo-500">Career Path</span>
          </h1>

          <p className="text-lg text-gray-500 max-w-xl mx-auto leading-relaxed">
            AI-powered career guidance through behavioral assessment and real-time emotion analysis.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-4 pt-4">
          {[
            { icon: Video, title: "Video Assessment", desc: "10 behavioral assessment questions with video recording." },
            { icon: Brain, title: "Emotion Analysis", desc: "Real-time facial emotion and sentiment tracking." },
            { icon: Award, title: "Career Report", desc: "Personalized career recommendations with insights." },
          ].map((feature, i) => (
            <div
              key={i}
              className="group p-6 rounded-xl border border-gray-200 bg-white text-left hover:border-indigo-200 hover:shadow-md transition-all duration-300"
            >
              <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-100 transition-colors">
                <feature.icon className="w-5 h-5 text-indigo-500" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900 mb-1">{feature.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="flex flex-col items-center gap-3 pt-4">
          <Link href="/setup">
            <Button
              size="lg"
              className="px-8 py-3 rounded-lg bg-indigo-500 text-white hover:bg-indigo-600 transition-colors text-base font-medium shadow-sm"
            >
              Start Assessment <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </Link>
          <p className="text-xs text-gray-400">
            Secure · Private · No data stored externally
          </p>
        </div>
      </div>
    </main>
  );
}
