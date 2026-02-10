'use client';

import React from 'react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Tooltip } from 'recharts';
import { PersonalityTraits } from '@/types';

interface PersonalityRadarProps {
    data: PersonalityTraits;
}

export default function PersonalityRadar({ data }: PersonalityRadarProps) {
    const chartData = [
        { subject: 'Openness', A: data.openness * 100, fullMark: 100 },
        { subject: 'Conscientious', A: data.conscientiousness * 100, fullMark: 100 },
        { subject: 'Extraversion', A: data.extraversion * 100, fullMark: 100 },
        { subject: 'Agreeable', A: data.agreeableness * 100, fullMark: 100 },
        { subject: 'Neuroticism', A: data.neuroticism * 100, fullMark: 100 },
    ];

    return (
        <div className="p-4 h-[320px] flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                    <PolarGrid stroke="#e5e7eb" />
                    <PolarAngleAxis
                        dataKey="subject"
                        tick={{ fill: '#6b7280', fontSize: 11, fontWeight: 500 }}
                    />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#ffffff',
                            border: '1px solid #e5e7eb',
                            borderRadius: '12px',
                            fontSize: '11px',
                            fontWeight: '600',
                            boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)',
                            padding: '8px 12px'
                        }}
                        itemStyle={{ color: '#6366f1' }}
                        formatter={(value: any) => [`${Math.round(Number(value) || 0)}%`, 'Score']}
                    />
                    <Radar
                        name="Personality"
                        dataKey="A"
                        stroke="#6366f1"
                        fill="#6366f1"
                        fillOpacity={0.2}
                        animationBegin={0}
                        animationDuration={800}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
}

PersonalityRadar.displayName = 'PersonalityRadar';
