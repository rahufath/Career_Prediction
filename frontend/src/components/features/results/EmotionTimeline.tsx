'use client';

import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface EmotionTimelineProps {
    data: any[];
}

export default function EmotionTimeline({ data }: EmotionTimelineProps) {
    const formattedData = data.map(item => ({
        time: item.time,
        ...item.emotions
    }));

    const emotions = [
        { key: 'happy', color: '#6366f1' },
        { key: 'neutral', color: '#94a3b8' },
        { key: 'surprise', color: '#f59e0b' },
        { key: 'fear', color: '#64748b' },
        { key: 'sad', color: '#a1a1aa' },
        { key: 'angry', color: '#ef4444' },
        { key: 'disgust', color: '#10b981' }
    ];

    return (
        <div className="w-full h-[400px] p-6">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={formattedData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                        {emotions.map(e => (
                            <linearGradient key={e.key} id={`grad-${e.key}`} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={e.color} stopOpacity={0.12} />
                                <stop offset="95%" stopColor={e.color} stopOpacity={0} />
                            </linearGradient>
                        ))}
                    </defs>
                    <CartesianGrid vertical={false} strokeDasharray="4 4" stroke="#f1f5f9" />
                    <XAxis
                        dataKey="time"
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 600 }}
                        dy={10}
                    />
                    <YAxis hide domain={[0, 1]} />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: 'rgba(255, 255, 255, 0.98)',
                            backdropFilter: 'blur(8px)',
                            border: '1px solid #e2e8f0',
                            borderRadius: '12px',
                            fontSize: '11px',
                            fontWeight: '700',
                            boxShadow: '0 10px 15px -3px rgba(0,0,0,0.05)',
                        }}
                    />
                    <Legend
                        iconType="circle"
                        verticalAlign="top"
                        align="right"
                        wrapperStyle={{
                            paddingBottom: '30px',
                            fontSize: '10px',
                            fontWeight: '700',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em',
                            opacity: 0.6
                        }}
                    />
                    {emotions.map(e => (
                        <Area
                            key={e.key}
                            type="monotone"
                            dataKey={e.key}
                            stroke={e.color}
                            fillOpacity={1}
                            fill={`url(#grad-${e.key})`}
                            strokeWidth={2}
                            stackId="1"
                            dot={false}
                            activeDot={{ r: 4, strokeWidth: 0, fill: e.color }}
                            animationDuration={1500}
                        />
                    ))}
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}

EmotionTimeline.displayName = 'EmotionTimeline';
