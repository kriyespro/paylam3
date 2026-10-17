/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#000F36',
        secondary: '#14378A',
        accent: '#FCD148',
      },
    },
  },
  plugins: [],
};
