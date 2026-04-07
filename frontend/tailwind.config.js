/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#18181b',
        mist: '#f7f4ee',
        sand: '#e7dcc8',
        gold: '#b58a3c',
        pine: '#24352f',
      },
      boxShadow: {
        premium: '0 24px 60px -30px rgba(24, 24, 27, 0.35)',
      },
      backgroundImage: {
        grain: 'radial-gradient(circle at top, rgba(181, 138, 60, 0.12), transparent 30%), radial-gradient(circle at bottom right, rgba(36, 53, 47, 0.08), transparent 24%)',
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Manrope', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
