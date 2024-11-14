// components/Loading.jsx
import React from 'react';

function Loading() {
  return (
    <div className="flex flex-col items-center space-y-2">
      <div className="w-16 h-16 border-4 border-purple-600 border-dashed rounded-full animate-spin"></div>
      <div className="text-purple-600 font-medium">Uploading...</div>
    </div>
  );
}

export default Loading;
