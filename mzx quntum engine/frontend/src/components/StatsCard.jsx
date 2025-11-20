# src/components/StatsCard.jsx
import React from 'react'

export default function StatsCard({ title, value, color }){
  return (
    <div className={`p-4 rounded-xl bg-black/40 border border-${color}-500/40 shadow-lg`}> 
      <div className="text-lg text-gray-300 mb-1">{title}</div>
      <div className={`text-3xl font-bold text-${color}-400`}>{value}</div>
    </div>
  )
}