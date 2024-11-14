// tailwind.config.js

module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}', // Adjust paths as needed
    './public/index.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6a0dad', // Example primary color
        'primary-dark': '#5a0cad', // Darker shade for hover
        secondary: '#FF00B6', // Example secondary color
        'secondary-dark': '#E500A1', // Darker shade for hover
        // Add more custom colors if needed
      },
      keyframes: {
        pulseSlow: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        },
        pulseGlow: { // Define the pulseGlow keyframes
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(255, 0, 182, 0.7)' },
          '50%': { boxShadow: '0 0 10px 10px rgba(255, 0, 182, 0)' },
        },
        fadeIn: { // Define fadeIn keyframes
          '0%': { opacity: 0, transform: 'translateY(-20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      animation: {
        pulseSlow: 'pulseSlow 6s ease-in-out infinite',
        pulseGlow: 'pulseGlow 2s infinite', // Define the pulseGlow animation
        fadeIn: 'fadeIn 1s ease-out forwards', // Define the fadeIn animation
      },
      transitionDelay: {
        '2s': '2000ms',
      },
    },
  },
  variants: {
    extend: {
      animation: ['responsive', 'hover', 'focus'],
      transitionDelay: ['responsive', 'hover', 'focus'],
    },
  },
  plugins: [],
};
