# src/components/ErrorBox.jsx
import React from 'react'

export default function ErrorBox({ message }){
  return (
    <div className="p-4 bg-red-900/40 border border-red-500 rounded-xl text-red-300 text-center">
      ⚠️ {message}
    </div>
  )
