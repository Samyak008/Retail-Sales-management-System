/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          900: "#0b132b",
          700: "#1c2541",
          500: "#3a506b",
          300: "#5bc0be",
          100: "#e0fbfc",
        },
        sand: {
          50: "#f9f7f3",
          100: "#f2eee5",
          200: "#e4d8c9",
        },
        accent: "#ff7f50",
      },
      fontFamily: {
        grotesk: ["Space Grotesk", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        card: "0 15px 35px rgba(0,0,0,0.08)",
      },
    },
  },
  plugins: [],
};

